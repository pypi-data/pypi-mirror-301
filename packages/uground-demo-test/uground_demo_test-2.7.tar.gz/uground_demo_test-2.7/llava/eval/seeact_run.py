import asyncio
import os
import random

from seeact.agent import SeeActAgent

# Setup your API Key here, or pass through environment
os.environ["OPENAI_API_KEY"] = "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"
# os.environ["GEMINI_API_KEY"] = "Your API KEY Here"


async def run_agent():
    agent = SeeActAgent(model="gpt-4o")
    await agent.start()
    while not agent.complete_flag:
        prediction_dict = await agent.predict()
        await agent.execute(prediction_dict)
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(run_agent())
#
# async def run_agent():
#
#     import json
#
#     # Define the input file path
#     input_file = "tasks.json"
#
#     # Load the data from the input file
#     with open(input_file, 'r', encoding='utf-8') as infile:
#         data = json.load(infile)
#
#     # Iterate through each data point and print the required fields
#
#     data=[i for i in data]
#     random.shuffle(data)
#     for item in data:
#
#
#         website = item.get("website", "N/A")
#         task_id = item.get("task_id", "N/A")
#         confirmed_task = item.get("confirmed_task", "N/A")
#
#         agent = SeeActAgent(model="gpt-4o",default_task=confirmed_task,default_website=website,save_task_id=task_id)
#         await agent.start()
#         count = 0
#         try:
#             while not agent.complete_flag and count < 20:
#                 prediction_dict = await agent.predict()
#                 await agent.execute(prediction_dict)
#                 count += 1
#         except Exception as e:
#             print(e)
#         try:
#             await agent.stop()
#         except Exception as e:
#             print(e)
#
#
#
#
# if __name__ == "__main__":
#     asyncio.run(run_agent())







# import asyncio
# import os
# from seeact.agent import SeeActAgent
#
# # Setup your API Key here, or pass through environment
# os.environ["OPENAI_API_KEY"] = "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"
# # os.environ["GEMINI_API_KEY"] = "Your API KEY Here"
#
# async def process_task(item):
#     website = item.get("website", "N/A")
#     task_id = item.get("task_id", "N/A")
#     confirmed_task = item.get("confirmed_task", "N/A")
#
#     agent = SeeActAgent(model="gpt-4o", default_task=confirmed_task, default_website=website, save_task_id=task_id,save_file_dir="mind2web-online90")
#     await agent.start()
#     count = 0
#     while not agent.complete_flag and count < 20:
#         prediction_dict = await agent.predict()
#         await agent.execute(prediction_dict)
#         count += 1
#     await agent.stop()
#
# async def run_agent():
#     import json
#
#     # Define the input file path
#     input_file = "tasks.json"
#
#     # Load the data from the input file
#     with open(input_file, 'r', encoding='utf-8') as infile:
#         data = json.load(infile)
#
#     # Use a semaphore to limit the number of concurrent tasks
#     semaphore = asyncio.Semaphore(1)
#
#     async def sem_task(item):
#         async with semaphore:
#             await process_task(item)
#
#     # Schedule all the tasks
#     tasks = [sem_task(item) for item in data]
#     await asyncio.gather(*tasks)
#
# if __name__ == "__main__":
#     asyncio.run(run_agent())


