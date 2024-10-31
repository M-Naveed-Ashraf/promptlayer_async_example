import os
import time
import asyncio
from promptlayer import PromptLayer, AsyncPromptLayer
from create_plot import create_plot
from log_time import log_time
from dotenv import load_dotenv

load_dotenv()
PROMPTLAYER_API_KEY = os.getenv("PROMPTLAYER_API_KEY")

async_pl = AsyncPromptLayer(api_key=PROMPTLAYER_API_KEY)
pl = PromptLayer(api_key=PROMPTLAYER_API_KEY)

async def fetch_prompt_template(timestamps, start_time, prompt_name):
    # Log start time with the prompt name as the event name
    log_time(timestamps, start_time, prompt_name, start=True)
    template = await async_pl.templates.get(prompt_name)
    # Log end time with the same prompt name
    log_time(timestamps, start_time, prompt_name, start=False)
    return template


async def bulk_get_prompts(prompt_names):
    timestamps = []
    start_time = time.time()

    # Use asyncio.gather to fetch all prompts in parallel
    tasks = [
        fetch_prompt_template(timestamps, start_time, prompt_name)
        for prompt_name in prompt_names
    ]
    templates = await asyncio.gather(*tasks)
    
    print(timestamps)
    # Plot results
    create_plot(timestamps, title="Parallel Fetching of Prompt Templates")
    
    return templates

# Example usage
prompt_names = ["Test", "Create Large CSV", "Test Large Prompt", "test"]  # Replace with actual prompt names
asyncio.run(bulk_get_prompts(prompt_names))
