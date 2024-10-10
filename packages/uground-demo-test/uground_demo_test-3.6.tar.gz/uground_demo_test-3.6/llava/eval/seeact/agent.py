# -*- coding: utf-8 -*-
# Copyright (c) 2024 OSU Natural Language Processing Group
#
# Licensed under the OpenRAIL-S License;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.licenses.ai/ai-pubs-open-rails-vz1
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import traceback
from datetime import datetime
import json
import toml
import torch
from playwright.async_api import async_playwright,Locator

from .data_utils.format_prompt_utils import get_index_from_option_name, generate_new_query_prompt, \
    generate_new_referring_prompt, format_options
from .demo_utils.browser_helper import normal_launch_async, normal_new_context_async, \
    get_interactive_elements_with_playwright, select_option, saveconfig, get_select_elements_with_playwright
from .demo_utils.format_prompt import format_choices, postprocess_action_lmm
from .demo_utils.inference_engine import engine_factory



from llava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN
from llava.conversation import conv_templates
from llava.model.builder import load_pretrained_model
from llava.utils import disable_torch_init
from llava.mm_utils import tokenizer_image_token, process_images, get_model_name_from_path

from PIL import Image, ImageDraw,ImageFont

import numpy as np

import asyncio


def average_color(image, bbox):
    """计算指定区域的平均颜色。"""
    region = image.crop(bbox)
    numpy_image = np.array(region)
    avg_color = np.mean(numpy_image, axis=(0, 1))
    return tuple(avg_color)


def color_contrast(color1, color2):
    """计算两种颜色之间的对比度。"""
    l1 = 0.2126 * pow(color1[0]/255, 2.2) + \
         0.7152 * pow(color1[1]/255, 2.2) + \
         0.0722 * pow(color1[2]/255, 2.2)
    l2 = 0.2126 * pow(color2[0]/255, 2.2) + \
         0.7152 * pow(color2[1]/255, 2.2) + \
         0.0722 * pow(color2[2]/255, 2.2)
    if l1 > l2:
        return (l1 + 0.05) / (l2 + 0.05)
    else:
        return (l2 + 0.05) / (l1 + 0.05)

def text_color_for_background(background_color):
    """选择最佳的文本颜色基于背景颜色。"""
    red = (255, 0, 0)
    blue = (0, 0, 255)
    contrast_red = color_contrast(background_color, red)
    contrast_blue = color_contrast(background_color, blue)
    if contrast_red > contrast_blue:
        return red
    else:
        return blue


def draw_text(draw, text, position, font, max_width, image):
    """在图像上绘制自动换行的文本，并根据背景色调整文本颜色。"""
    x, y = position
    words = text.split()
    current_line = ""

    # 使用一个空字符串来获取单行文字的高度
    line_height = 40

    for word in words:
        test_line = f"{current_line} {word}".strip()
        width, _ = 40,40  # 正确调用font对象的getsize方法
        if width <= max_width:
            current_line = test_line
        else:
            bbox = (x, y, x + width, y + line_height)
            bg_color = average_color(image, bbox)
            color = text_color_for_background(bg_color)
            draw.text((x, y), current_line, font=font, fill=color)
            y += line_height
            current_line = word
    if current_line:
        bbox = (x, y, x + width, y + line_height)
        bg_color = average_color(image, bbox)
        color = text_color_for_background(bg_color)
        draw.text((x, y), current_line, font=font, fill=color)


class SeeActAgent:
    def __init__(self,
                 config_path=None,
                 save_file_dir="seeact_agent_files",
                 save_task_id=None,
                 default_task='Search for the flight status for the flight AA 3942 leaving on Jun. 10"',
                 default_website="https://www.aa.com/homePage.do",
                 input_info=["screenshot"],
                 grounding_strategy="text_choice",
                 max_auto_op=50,
                 max_continuous_no_op=5,
                 highlight=False,
                 headless=False,
                 args=[],
                 browser_app="chrome",
                 persistant=False,
                 persistant_user_path="",
                 save_video=False,
                 viewport={
                     "width": 1280,
                     "height": 960
                 },
                 tracing=False,
                 trace={
                     "screenshots": True,
                     "snapshots": True,
                     "sources": True
                 },
                 rate_limit=-1,
                 model="gpt-4-turbo",
                 temperature=0.9

                 ):

        try:
            if config_path is not None:
                with open(config_path,
                          'r') as config:
                    print(f"Configuration File Loaded - {config_path}")
                    config = toml.load(config)
            else:
                config = {
                    "basic": {
                        "save_file_dir": save_file_dir,
                        "default_task": default_task,
                        "default_website": default_website
                    },
                    "agent": {
                        "input_info": input_info,
                        "grounding_strategy": grounding_strategy,
                        "max_auto_op": max_auto_op,
                        "max_continuous_no_op": max_continuous_no_op,
                        "highlight": highlight
                    },
                    "openai": {
                        "rate_limit": rate_limit,
                        "model": model,
                        "temperature": temperature
                    }
                }
            config.update({
                "browser": {
                    "headless": headless,
                    "args": args,
                    "browser_app": browser_app,
                    "persistant": persistant,
                    "persistant_user_path": persistant_user_path,
                    "save_video": save_video,
                    "viewport": viewport,
                    "tracing": tracing,
                    "trace": trace
                }
            })

        except FileNotFoundError:
            print(f"Error: File '{os.path.abspath(config_path)}' not found.")
        except toml.TomlDecodeError:
            print(f"Error: File '{os.path.abspath(config_path)}' is not a valid TOML file.")

        self.config = config
        self.complete_flag = False
        self.session_control = {
            'active_page': None,
            'context': None,
            'browser': None
        }
        self.tasks = [self.config["basic"]["default_task"]]
        if save_task_id:
            self.main_path = os.path.join(self.config["basic"]["save_file_dir"],
                                          save_task_id)


        else:
            self.main_path = os.path.join(self.config["basic"]["save_file_dir"], datetime.now().strftime("%Y%m%d_%H%M%S"))
        if os.path.exists(self.main_path):
            self.complete_flag=True

        os.makedirs(self.main_path, exist_ok=True)
        self.action_space = ["CLICK", "PRESS ENTER", "HOVER", "SCROLL UP", "SCROLL DOWN", "NEW TAB", "CLOSE TAB",
                             "GO BACK", "GO FORWARD",
                             "TERMINATE", "SELECT", "TYPE", "GOTO", "MEMORIZE"]  # Define the list of actions here

        self.no_value_op = ["CLICK", "PRESS ENTER", "HOVER", "SCROLL UP", "SCROLL DOWN", "NEW TAB", "CLOSE TAB",
                            "PRESS HOME", "PRESS END", "PRESS PAGEUP", "PRESS PAGEDOWN"
                                                                       "GO BACK",
                            "GO FORWARD",
                            "TERMINATE", "NONE"]

        self.with_value_op = ["SELECT", "TYPE", "GOTO", "MEMORIZE", "SAY"]

        self.no_element_op = ["PRESS ENTER", "SCROLL UP", "SCROLL DOWN", "NEW TAB", "CLOSE TAB", "GO BACK", "GOTO",
                              "PRESS HOME", "PRESS END", "PRESS PAGEUP", "PRESS PAGEDOWN",
                              "GO FORWARD",
                              "TERMINATE", "NONE", "MEMORIZE", "SAY"]

        # Initialize the primary logger and the developer logger
        self.logger = self._setup_logger(redirect_to_dev_log=False)
        # self.dev_logger = self._setup_dev_logger()

        # # Redirect primary logger messages to dev_logger as well
        # for handler in self.logger.handlers:
        #     self.dev_logger.addHandler(handler)

        self.engine = engine_factory(**self.config['openai'])
        self.taken_actions = []
        self.prompts = self._initialize_prompts()
        self.time_step = 0
        self.valid_op = 0
        # self.error=0
        self.continuous_no_op = 0
        self.predictions=[]

        disable_torch_init()
        self.pixui_model_path = os.path.expanduser(
            "/fs/ess/PAS1576/boyu_gou/train_vlm/ui_llava_fine_tune/checkpoints/only-web/merged-llava-v1.5-vicuna-7b-16k-pad-no-fusion-web-80k")
        self.pixui_model_name = get_model_name_from_path(self.pixui_model_path)
        self.pixui_tokenizer, self.pixui_model, self.pixui_image_processor, self.pixui_context_len = load_pretrained_model(self.pixui_model_path, None, self.pixui_model_name)

    def _initialize_prompts(self):
        """Initialize prompt information including dynamic action space."""
        action_format = f""  # Dynamically generate action_format based on self.action_space

        return {
            "system_prompt": '''You are assisting humans doing web navigation tasks step by step. At each stage, you can see the webpage by a screenshot and know the previous actions before the current step decided by yourself that have been executed for this task through recorded history. You need to decide on the first following action to take.''',

            "action_space": '''
Here are the descriptions of all allowed actions:

No Value Operations:
- CLICK: Click on a webpage element using the mouse.
- PRESS ENTER: Press the Enter key, typically to submit a form or confirm an input.
- SCROLL UP: Scroll the webpage upwards by half of the window height.
- SCROLL DOWN: Scroll the webpage downwards by half of the window height.
- PRESS HOME: Scroll to the top of the webpage.
- PRESS END: Scroll to the bottom of the webpage.
- PRESS PAGEUP: Scroll up by one window height.
- PRESS PAGEDOWN: Scroll down by one window height.
- GO BACK: Navigate to the previous page in the browser history.
- GO FORWARD: Navigate to the next page in the browser history.
- TERMINATE: End the current task, typically used when the task is considered complete or requires potentially harmful actions.
- NONE: Indicates that no action is necessary at this stage. Used to skip an action or wait.

With Value Operations:
- SELECT: Choose an option from a dropdown menu or <select> element. The value indicates the option to select.
- TYPE: Enter text into a text area or text box. The value is the text to be typed.
''',

            "question_description": '''The screenshot below shows the webpage you see. Think step by step before outlining the next action step at the current stage. Clearly outline which element in the webpage users will operate with as the first next target element, its detailed location, and the corresponding operation.

To be successful, it is important to follow the following rules:
1. You should only issue a valid action given the current observation.
2. You should only issue one action at a time
3. Unlike humans, since you are using playwright APIs, for typing (e.g., in text areas, text boxes) and selecting (e.g., from dropdown menus or <select> elements), you should try directly typing the input or selecting the choice, bypassing the need for an initial click.
4. You should not attempt to create accounts, log in or do the final submission.
5. Terminate when you deem the task complete or if it requires potentially harmful actions.
6. Details of <select> elements will be provided, to help you figure out the exact choice text to be chosen if the action is a SELECT.
7. If you find there are one or more failed actions in the most recent actions, you should change the description and make your descriptions more precise and concise (and at least do not repeat the latest description.).

(Final Answer)
Finally, conclude your answer using the format below. Ensure your answer is strictly adhering to the format provided below. Please do not leave any explanation in your answers of the final standardized format part, and this final part should be clear and certain. The element choice, action, and value should be in three separate lines.

Format:

ELEMENT: The description of the target element to locate the element, if the action involves a specific element. Otherwise write "None"

ACTION: Choose an action from allowed actions.

VALUE: Provide additional input based on ACTION. (If it doesn't involve a value, write "None"''',

            "referring_description": f"""(Reiteration)
First, reiterate your next target element, its detailed location, and the corresponding operation.""",

            "element_format": '''''',

            "action_format": action_format,  # Use the dynamically generated action_format

            "value_format": ''''''
        }

    def update_action_space(self, new_actions):
        """Update the action space and regenerate the action_format prompt."""
        if isinstance(new_actions, list) and all(isinstance(item, str) for item in new_actions):
            self.action_space = new_actions
            self.prompts["action_format"] = f"ACTION: Choose an action from {{{', '.join(self.action_space)}}}."
        else:
            print("Invalid action space provided. It must be a list of strings.")

    def _setup_logger(self, redirect_to_dev_log=False):
        """Set up a logger to log to both file and console within the main_path."""
        logger_name = 'SeeActAgent'
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        if not logger.handlers:  # Avoid adding handlers multiple times
            # Create a file handler for writing logs to a file
            log_filename = 'agent.log'
            f_handler = logging.FileHandler(os.path.join(self.main_path, log_filename))
            f_handler.setLevel(logging.INFO)

            # Create a console handler for printing logs to the terminal
            c_handler = logging.StreamHandler()
            c_handler.setLevel(logging.INFO)

            # Create formatters for file and console handlers
            file_formatter = logging.Formatter('%(asctime)s - %(message)s')
            console_formatter = logging.Formatter('%(message)s')

            # Set formatters for file and console handlers
            f_handler.setFormatter(file_formatter)
            c_handler.setFormatter(console_formatter)

            # Add the handlers to the logger
            logger.addHandler(f_handler)
            if not redirect_to_dev_log:  # Only add console handler if not redirecting to dev log
                logger.addHandler(c_handler)

        return logger

    # def _setup_dev_logger(self):
    #     """Set up a developer logger to log only to a file within the main_path."""
    #     dev_logger_name = 'SeeActAgentDev'
    #     dev_logger = logging.getLogger(dev_logger_name)
    #     dev_logger.setLevel(logging.INFO)
    #     if not dev_logger.handlers:  # Avoid adding handlers multiple times
    #         # Create a file handler for writing logs to a dev log file
    #         dev_log_filename = 'dev_agent.log'
    #         f_handler = logging.FileHandler(os.path.join(self.main_path, dev_log_filename))
    #         f_handler.setLevel(logging.INFO)
    #
    #         # Create a formatter and add it to the handler
    #         formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #         f_handler.setFormatter(formatter)
    #
    #         # Add the file handler to the dev logger
    #         dev_logger.addHandler(f_handler)
    #
    #     return dev_logger

    async def page_on_close_handler(self):
        # Corrected to use 'self' for accessing class attributes
        if self.session_control['context']:
            try:
                await self.session_control['active_page'].title()
            except:
                self.logger.info(
                    "The active tab was closed. Will switch to the last page (or open a new default google page)")
                if self.session_control['context'].pages:
                    self.session_control['active_page'] = self.session_control['context'].pages[-1]
                    await self.session_control['active_page'].bring_to_front()
                    self.logger.info(f"Switched the active tab to: {self.session_control['active_page'].url}")
                else:
                    self.session_control['active_page'] = await self.session_control['context'].new_page()
                    try:
                        await self.session_control['active_page'].goto("https://www.google.com/", wait_until="load")
                    except Exception as e:
                        self.logger.info(f"Failed to navigate to Google: {e}")
                    self.logger.info(f"Switched the active tab to: {self.session_control['active_page'].url}")

    def save_action_history(self, filename="action_history.txt"):
        """Save the history of taken actions to a file in the main path."""
        history_path = os.path.join(self.main_path, filename)
        with open(history_path, 'w') as f:
            for action in self.taken_actions:
                f.write(action + '\n')
        self.logger.info(f"Action history saved to: {history_path}")

    async def page_on_navigation_handler(self, frame):
        # Corrected to use 'self' for accessing class attributes
        self.session_control['active_page'] = frame.page

    async def page_on_crash_handler(self, page):
        # Corrected logging method
        self.logger.info(f"Page crashed: {page.url}")
        self.logger.info("Try to reload")
        await page.reload()

    async def page_on_open_handler(self, page):
        # Added 'self' to the handler functions to reference the current instance of the class
        page.on("framenavigated", self.page_on_navigation_handler)
        page.on("close", self.page_on_close_handler)
        page.on("crash", self.page_on_crash_handler)
        self.session_control['active_page'] = page
        # Additional event listeners can be added here

    async def start(self, headless=None, args=None, website=None):
        self.playwright = await async_playwright().start()
        self.session_control['browser'] = await normal_launch_async(self.playwright,
                                                                    headless=self.config['browser'][
                                                                        'headless'] if headless is None else headless,
                                                                    args=self.config['browser'][
                                                                        'args'] if args is None else args)
        self.session_control['context'] = await normal_new_context_async(self.session_control['browser'],
                                                                         viewport=self.config['browser'][
                                                                             'viewport'])

        self.session_control['context'].on("page", self.page_on_open_handler)
        await self.session_control['context'].new_page()

        try:
            await self.session_control['active_page'].goto(
                self.config['basic']['default_website'] if website is None else website,
                wait_until="load")
            self.logger.info(f"Loaded website: {self.config['basic']['default_website']}")
        except Exception as e:
            self.logger.info("Failed to fully load the webpage before timeout")
            self.logger.info(e)

            # await asyncio.sleep(2)

    def update_prompt_part(self, part_name, new_text):
        """Update the specified part of the prompt information."""
        if part_name in self.prompts:
            self.prompts[part_name] = new_text
            return True
        else:
            print(f"Prompt part '{part_name}' not found.")
            return False

    def generate_prompt(self, task=None, previous=None, choices=None):

        """Generate a prompt based on the current task, previous actions, and choices."""
        # assert task is not None, "Please input the task."

        prompt_list = []

        system_prompt_input = self.prompts["system_prompt"]
        action_space_input = self.prompts["action_space"]
        question_description_input = self.prompts["question_description"]
        referring_input = self.prompts["referring_description"]
        element_format_input = self.prompts["element_format"]
        action_format_input = self.prompts["action_format"]
        value_format_input = self.prompts["value_format"]

        # print(previous)

        previous_ = self.taken_actions if self.taken_actions else None

        # print(previous_)

        prompt_list.extend(
            generate_new_query_prompt(system_prompt=system_prompt_input + "\n" + action_space_input,
                                      task=self.tasks[-1], previous_actions=previous_,
                                      question_description=question_description_input,select_elements=choices))
        prompt_list.append(
            generate_new_referring_prompt(referring_description=referring_input, element_format=element_format_input,
                                          action_format=action_format_input, value_format=value_format_input,
                                          choices=None))

        return prompt_list

    async def perform_action(self, target_element=None, action_name=None, value=None, element_repr=""):
        if target_element is not None:
            selector = target_element['selector']
            element_repr =target_element['description']
        else:
            selector = None

        page = self.session_control['active_page']



        if action_name == "CLICK" and selector:
            # await selector.click(timeout=2000)
            await self.session_control['active_page'].mouse.click(x=selector[0], y=selector[1])
            self.logger.info(f"Clicked on element: {element_repr}")
        elif action_name == "HOVER" and selector:
            # await selector.hover(timeout=2000)
            await self.session_control['active_page'].mouse.move(x=selector[0], y=selector[1])
            self.logger.info(f"Hovered over element: {element_repr}")
        elif action_name == "TYPE" and selector:
            # await selector.fill(value)
            # await selector.fill(value)
            await self.session_control['active_page'].mouse.click(x=selector[0], y=selector[1])
            await page.keyboard.type(value)

            self.logger.info(f"Typed '{value}' into element: {element_repr}")
        elif action_name == "SCROLL UP":
            await page.evaluate(f"window.scrollBy(0, -{self.config['browser']['viewport']['height'] // 2});")
            self.logger.info("Scrolled up")
        elif action_name == "SCROLL DOWN":
            await page.evaluate(f"window.scrollBy(0, {self.config['browser']['viewport']['height'] // 2});")
            self.logger.info("Scrolled down")
        elif action_name == "PRESS HOME":
            await page.keyboard.press('Home')
            self.logger.info("Pressed Home key")
        elif action_name == "PRESS END":
            await page.keyboard.press('End')
            self.logger.info("Pressed End key")
        elif action_name == "PRESS PAGEUP":
            await page.keyboard.press('PageUp')
            self.logger.info("Pressed PageUp key")
        elif action_name == "PRESS PAGEDOWN":
            await page.keyboard.press('PageDown')
            self.logger.info("Pressed PageDown key")
        elif action_name == "NEW TAB":
            new_page = await self.session_control['context'].new_page()
            # self.session_control['pages'].append(new_page)
            self.logger.info("Opened a new tab")
        elif action_name == "CLOSE TAB":
            await page.close()
            self.logger.info("Closed the current tab")
        elif action_name == "GO BACK":
            await page.go_back()
            self.logger.info("Navigated back")
        elif action_name == "GO FORWARD":
            await page.go_forward()
            self.logger.info("Navigated forward")
        elif action_name == "GOTO" and value:
            await page.goto(value, wait_until="load")
            self.logger.info(f"Navigated to {value}")
        # elif action_name == "PRESS ENTER" and selector:
        #     await selector.press('Enter')
        #     self.logger.info(f"Pressed Enter on element: {element_repr}")
        elif action_name == "PRESS ENTER":
            await page.keyboard.press('Enter')
            self.logger.info(f"Pressed Enter on element: {element_repr}")
        elif action_name == "SELECT" and selector:
            await select_option(selector, value)
            self.logger.info(f"Selected option '{value}' from element: {element_repr}")
        elif action_name == "TERMINATE":
            self.complete_flag = True
            self.logger.info("Task has been marked as complete. Terminating...")
        elif action_name in ["NONE"]:
            self.logger.info("No action necessary at this stage. Skipped")
        elif action_name in ["SAY"]:
            self.logger.info(f"Say {value} to the user")
        elif action_name in ["MEMORIZE"]:
            self.logger.info(f"Keep {value} to the action history.")
        else:
            raise Exception(f"Unsupported or improperly specified action: {action_name}")
        if action_name in self.no_element_op and target_element is None:
            new_action = action_name
        else:
            # new_action = "[" + target_element['tag_with_role'] + "]" + " "
            new_action = target_element['description'] + " -> " + action_name
        if action_name in self.with_value_op:
            new_action += ": " + value

        # self.dev_logger.info(new_action)
        return new_action

    async def predict(self):

        """
        Generate a prediction for the next action based on the webpage elements and previous actions.
        """

        self.time_step += 1

        try:
            await self.session_control["active_page"].wait_for_load_state('load')
        except Exception as e:
            pass

        # elements = await get_interactive_elements_with_playwright(self.session_control['active_page'],
        #                                                           self.config['browser']['viewport'])
        elements = None

        '''
             0: center_point =(x,y)
             1: description
             2: tag_with_role: tag_head with role and type # TODO: Consider adding more
             3. box
             4. selector
             5. tag
             '''

        # elements = sorted(elements, key=lambda el: (
        #     el["center_point"][1], el["center_point"][0]))  # Sorting by y and then x coordinate

        # Generate choices for the prompt

        # , self.config['basic']['default_task'], self.taken_actions
        # choices = format_choices(elements)

        select_elements = await get_select_elements_with_playwright(self.session_control['active_page'],
                                                                           self.config['browser']['viewport'],
                                                                           )

        select_elements_formated=format_choices(select_elements)

        # print("\n\n",choices)
        prompt = self.generate_prompt(task=self.tasks[-1], previous=self.taken_actions, choices=select_elements_formated)
        # print("\n\n",prompt)

        # Logging prompt for debugging

        # Capture a screenshot for the current state of the webpage, if required by the model
        screenshot_path = os.path.join(self.main_path, 'screenshots', f'screen_{self.time_step}.png')
        try:
            await self.session_control['active_page'].screenshot(path=screenshot_path)
        except Exception as e:
            self.logger.info(f"Failed to take screenshot: {e}")

        terminal_width = 10
        self.logger.info(f"Step - {self.time_step}\n{'-'*terminal_width}\nAction Generation ➡️")
        # for prompt_part in prompt:
        self.logger.info("TASK: "+self.tasks[-1])
        self.logger.info("Previous:")
        for action in self.taken_actions:
            self.logger.info(action)

        output0 = self.engine.generate(prompt=prompt, image_path=screenshot_path, turn_number=0)

        terminal_width = 10
        self.logger.info("-" * terminal_width)
        self.logger.info("🤖 Action Generation Output 🤖")

        for line in output0.split('\n'):
            self.logger.info(line)

        terminal_width = 10
        self.logger.info("-" * (terminal_width))

        # choice_text = f"Action Grounding ➡️" + "\n" + format_options(
        #     choices)
        # choice_text = choice_text.replace("\n\n", "")
        #
        # for line in choice_text.split('\n'):
        #     self.logger.info(line)

        # output = self.engine.generate(prompt=prompt, image_path=screenshot_path, turn_number=1,
        #                                      ouput_0=output0)

        output=""
        self.logger.info("🤖 Action Grounding Output 🤖")
        for line in output.split('\n'):
            self.logger.info(line)

        pred_element_label, pred_action, pred_value = postprocess_action_lmm(output0)

        # print(pred_element_label)
        # print(pred_action)
        # print(pred_value)
        # exit()

        # if len(pred_element_label) in [1, 2]:
        #     element_id = get_index_from_option_name(pred_element_label)
        # else:
        #     element_id = None
        pred_element = pred_element_label

        def get_scale_factor(original_size):
            original_width, original_height = original_size
            new_width = min(nearest_multiple_of_224_at_least_224(original_width, ceiling=False), 1344)
            scale_factor = new_width / original_width
            return scale_factor

        def nearest_multiple_of_224_at_least_224(num, ceiling=False):
            if num <= 224:
                return 224
            division, remainder = divmod(num, 224)
            if ceiling and remainder > 0:
                return (division + 1) * 224
            if remainder < 112:
                return division * 224
            else:
                return (division + 1) * 224



        image_file = screenshot_path

        qs = f"In the screenshot, where are the pixel coordinates (x, y) of the element corresponding to \"{pred_element}\"?"
        cur_prompt = qs
        if self.pixui_model.config.mm_use_im_start_end:
            qs = DEFAULT_IM_START_TOKEN + DEFAULT_IMAGE_TOKEN + DEFAULT_IM_END_TOKEN + '\n' + qs
        else:
            qs = DEFAULT_IMAGE_TOKEN + '\n' + qs

        conv = conv_templates["llava_v1"].copy()
        conv.append_message(conv.roles[0], qs)
        conv.append_message(conv.roles[1], None)
        prompt = conv.get_prompt()

        input_ids = tokenizer_image_token(prompt, self.pixui_tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).cuda()

        image = Image.open(os.path.join(image_file)).convert('RGB')
        # print("DEBUG",model.config)
        image_tensor, image_new_size = process_images([image], self.pixui_image_processor, self.pixui_model.config)
        # image_tensor,image_new_size = process_images([image], image_processor, model.config)[0]

        with torch.inference_mode():
            output_ids = self.pixui_model.generate(
                input_ids,
                # images=image_tensor.unsqueeze(0).half().cuda(),
                images=image_tensor.half().cuda(),
                image_sizes=[image_new_size],
                do_sample=False,
                temperature=0,
                top_p=None,
                num_beams=1,
                # no_repeat_ngram_size=3,
                max_new_tokens=16384,
                use_cache=True)

        outputs = self.pixui_tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0].strip()


        # print("predicted coordinate: ",outputs)


        grounding_image=Image.open(screenshot_path)







        scale=get_scale_factor(grounding_image.size)

        coord = eval(outputs)
        coord = tuple((i / scale for i in coord))

        elements_at_point= await get_select_elements_with_playwright(self.session_control['active_page'],self.config['browser']['viewport'])


        print(elements_at_point)

        if pred_action=="SELECT":
            import math
            def euclidean_distance(coord1, coord2):
                return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

            min_distance = float('inf')
            closest_element = None

            # 遍历所有元素，找到最近的
            for element in elements_at_point:
                distance = euclidean_distance(coord, element['center_point'])
                if distance < min_distance:
                    min_distance = distance
                    closest_element = element
            pred_element=closest_element
            pred_element['description']=pred_element_label



        # print(scale)

        # print(coord)

        annotated_screenshot_path = os.path.join(self.main_path, 'screenshots', f'screen_{self.time_step}_grounding.png')
        draw = ImageDraw.Draw(image)

        # prompt = self.generate_prompt(task=self.tasks[-1], previous=self.taken_actions,
        #                               choices=select_elements_formated)
        #
        # output = self.engine.generate(prompt=prompt, image_path=screenshot_path, turn_number=1,
        #                                      ouput_0=output0)


        # i=pred_element
        # print(i["description"])
        # print()
        # box=i['box']
        # left = box[0]
        # top = box[1]
        # right = box[0] + box[2]
        # bottom = box[1] + box[3]
        # # draw = ImageDraw.Draw(image2)
        # # 绘制红色边界框
        # draw.rectangle([left, top, right, bottom], outline="red", width=4)
        x, y = coord
        # 定义圆点的半径
        radius = 7
        # 绘制红色圆点
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill="blue")
        # 显示图片
        # image2.show()

        text = pred_element_label

        # 选择字体和字号
        font = ImageFont.truetype("/fs/ess/PAS1576/boyu_gou/train_vlm/ui_llava_fine_tune/llava/eval/Roboto-Medium.ttf", 36)

        # 计算文本的大小
        # text_width, text_height = draw.textsize(text, font=font)

        # 设置文本的位置（左上角）
        x = 0
        y = 0

        # 在图片上写入文本
        max_width = image.width

        draw_text(draw, text+str(coord), (0, 0), font, max_width, image)

        image.save(fp=annotated_screenshot_path)
        image.close()


        # exit()

        # Log the prediction result
        self.logger.debug(f"Retrieved Answer")
        self.logger.debug(f"Predicted Element: {pred_element}")
        self.logger.debug(f"Action: {pred_action}")
        self.logger.debug(f"Value: {pred_value}")

        prediction={"action_generation": output0, "action_grounding": None, "element": {"center_point":coord,"description":pred_element_label,"tag_with_role":None,"box":None,"selector":coord,"tag":None},
                "action": pred_action, "value": pred_value}

        self.predictions.append(prediction)

        return {"action_generation": output0, "action_grounding": None, "element": {"center_point":coord,"description":pred_element_label,"tag_with_role":None,"box":None,"selector":coord,"tag":None} if pred_action!="SELECT" else pred_element,
                "action": pred_action, "value": pred_value}



        # return output0,output,pred_element, pred_action, pred_value

    async def execute(self, prediction_dict):
        """
        Execute the predicted action on the webpage.
        """

        pred_element = prediction_dict["element"]
        pred_action = prediction_dict["action"]
        pred_value = prediction_dict["value"]
        try:
            if (pred_action not in self.no_element_op) and pred_element == None:
                # self.dev_logger.info
                self.logger.info("DEBUG: WHAT IS PRED ACTION???:" + pred_action)
                # self.dev_logger.info("DEBUG WHAT IS self.no_element_op???:"+ self.no_element_op)
                pred_action = "NONE"
            new_action = await self.perform_action(pred_element, pred_action, pred_value)
            self.taken_actions.append(new_action)
            if pred_action != "NONE":
                self.valid_op += 1
                self.continuous_no_op = 0
            else:
                self.continuous_no_op += 1
            await asyncio.sleep(3)
            return 0
        except Exception as e:

            new_action = f"Failed to perform {pred_action} on {pred_element['description']} with value '{pred_value}': {e}"


            traceback_info = traceback.format_exc()
            error_message = f"Error executing action {pred_action}: {str(e)}"
            print(traceback_info)
            # exit()
            error_message_with_traceback = f"{error_message}\n\nTraceback:\n{traceback_info}"

            self.logger.info(new_action)
            self.taken_actions.append(new_action)
            self.continuous_no_op += 1
            await asyncio.sleep(3)
            return 1

    async def stop(self):

        try:
            close_context = self.session_control['context']
            self.session_control['context'] = None
            await close_context.close()
            self.logger.info("Browser context closed.")
        except Exception as e:
            self.logger.info(e)

        final_json = {"task": self.tasks, "website": self.config["basic"]["default_website"],
                      "num_step": len(self.taken_actions), "action_history": self.taken_actions}

        def locator_serializer(obj):
            """Convert non-serializable objects to a serializable format."""
            if isinstance(obj, Locator):
                # Assuming Locator has attributes 'frame' and 'selector' you want to serialize
                return str(obj)
            raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

        # Using the custom default function in json.dump
        with open(os.path.join(self.main_path, 'all_predictions.json'), 'w', encoding='utf-8') as f:
            json.dump(self.predictions, f, default=locator_serializer, indent=4)


        with open(os.path.join(self.main_path, 'result.json'), 'w', encoding='utf-8') as file:
            json.dump(final_json, file, indent=4)
        self.logger.info("Agent stopped.")

        saveconfig(self.config, os.path.join(self.main_path, 'config.toml'))

    def clear_action_history(self):
        """
        Clears the history of actions taken by the agent.
        """
        self.taken_actions.clear()
        self.logger.info("Cleared action history.")

    def reset_comlete_flag(self, flag=False):
        self.complete_flag = flag

    def change_task(self, new_task, clear_history=False):
        """
        Changes the task requirement for the agent.

        Parameters:
        - new_task: The new task requirement as a string.
        """
        if new_task and isinstance(new_task, str):

            self.logger.info(f"Changed task from {self.tasks[-1]} to: {new_task}")
            self.tasks.append(new_task)
            # Optionally clear action history when changing task
            if clear_history:
                self.clear_action_history()
            else:
                self.taken_actions.append(f"Changed task from {self.tasks[-2]} to: {new_task}")

        else:
            self.logger.info("Invalid new task. It must be a non-empty string.")

        # Optionally, you can save the taken_actions to a file or database for record-keeping

    # ADD no op count and op count, add limit to op

    # decompose run to predict and execute.
