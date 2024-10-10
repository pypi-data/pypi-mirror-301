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
import re


def format_choices(elements):

    converted_elements = [
                    f'<{element["tag_with_role"]}>'
                    + (
                        element["description"]
                    )
                    + f"</{element['tag']}>"
                    for i, element in enumerate(elements)
                ]

    return converted_elements

def postprocess_action_lmm(text):
    text = text.strip()
    text = text.replace(
        "The uppercase letter of your choice. Choose one of the following elements if it matches the target element based on your analysis:\n\n",
        "")
    text = text.replace(
        "The uppercase letter of your choice. Choose one of the following elements if it matches the target element based on your analysis:\n",
        "")
    text = text.replace(
        "The uppercase letter of your choice. Choose one of the following elements if it matches the target element based on your analysis:",
        "")
    text = text.replace("The uppercase letter of your choice based on your analysis is:\n\n", "")
    text = text.replace("The uppercase letter of your choice based on your analysis is:\n", "")
    text = text.replace("The uppercase letter of your choice based on your analysis is:", "")
    text = text.replace("The uppercase letter of my choice is \n\n", "")
    text = text.replace("The uppercase letter of my choice is \n", "")
    text = text.replace("The uppercase letter of my choice is ", "")
    text = text.replace("The uppercase letter of your choice is \n\n", "")
    text = text.replace("The uppercase letter of your choice is \n", "")
    text = text.replace("The uppercase letter of your choice is ", "")
    text = text.replace("The uppercase letter of your choice.\n\n", "")
    text = text.replace("The uppercase letter of your choice.\n", "")
    text = text.replace("The uppercase letter of your choice.", "")
    text = text.replace("The uppercase letter of your choice based on my analysis is:\n\n", "")
    text = text.replace("The uppercase letter of your choice based on my analysis is:\n", "")
    text = text.replace("The uppercase letter of your choice based on my analysis is:", "")
    text = text.replace("The correct choice based on the analysis would be:\n\n", "")
    text = text.replace("The correct choice based on the analysis would be:\n", "")
    text = text.replace("The correct choice based on the analysis would be :", "")
    text = text.replace("The correct choice based on the analysis would be ", "")
    text = text.replace(
        "The uppercase letter of your choice. Choose one of the following elements if it matches the target element based on your analysis:\n\n",
        "")
    text = text.replace(
        "The uppercase letter of your choice. Choose one of the following elements if it matches the target element based on your analysis:\n",
        "")
    text = text.replace(
        "The uppercase letter of your choice. Choose one of the following elements if it matches the target element based on your analysis:",
        "")
    text = text.replace("The uppercase letter of your choice.\n\n", "")
    text = text.replace("The uppercase letter of your choice.\n", "")
    text = text.replace("The uppercase letter of your choice based on the analysis is:\n\n", "")
    text = text.replace("The uppercase letter of your choice based on the analysis is:\n", "")
    text = text.replace("The uppercase letter of your choice based on the analysis is:", "")
    text = text.replace("The uppercase letter of your choice based on the analysis is ", "")
    text = text.replace("The uppercase letter of my choice based on the analysis is:\n\n", "")
    text = text.replace("The uppercase letter of my choice based on the analysis is:\n", "")
    text = text.replace("The uppercase letter of my choice based on the analysis is:", "")
    text = text.replace("The uppercase letter of my choice based on the analysis is ", "")
    text = text.replace("The correct element to select would be:\n\n", "")
    text = text.replace("The correct element to select would be:\n", "")
    text = text.replace("The correct element to select would be:", "")
    text = text.replace("The correct element to select would be ", "")
    text = text.replace("The uppercase letter of my choice is:\n\n", "")
    text = text.replace("The uppercase letter of my choice is:\n", "")
    text = text.replace("The uppercase letter of my choice is:", "")
    text = text.replace("The uppercase letter of my choice is ", "")
    text = text.replace("Choose an action from {CLICK, TYPE, SELECT}.\n\n", "")
    text = text.replace("Choose an action from {CLICK, TYPE, SELECT}.\n", "")
    text = text.replace("Choose an action from {CLICK, TYPE, SELECT}.", "")
    text = text.replace("Provide additional input based on ACTION.\n\n", "")
    text = text.replace("Provide additional input based on ACTION.\n", "")
    text = text.replace("Provide additional input based on ACTION.", "")

    def extract_element_description(text):
        pattern = r'ELEMENT:\s*(.*?)\s*ACTION:'
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return None

    description = extract_element_description(text)
    action = re.search(
        r"ACTION: (CLICK|SELECT|TYPE|HOVER|PRESS ENTER|SCROLL UP|SCROLL DOWN|PRESS HOME|PRESS END|PRESS PAGEUP|PRESS PAGEDOWN|NEW TAB|CLOSE TAB|GO BACK|GO FORWARD|TERMINATE|NONE|GOTO|SAY|MEMORIZE)",
        text
    )


    if action:
        action = action.group(1)
    else:
        action = "None"

    value = re.search(r"VALUE: (.*)$", text, re.MULTILINE)
    value = value.group(1) if value is not None else ""
    return description, action.strip(), process_string(process_string(value.strip()))

def process_string(input_string):
    if input_string.startswith('"') and input_string.endswith('"'):
        input_string = input_string[1:-1]
    if input_string.endswith('.'):
        input_string = input_string[:-1]
    return input_string









