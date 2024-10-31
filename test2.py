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

async def fetch_template(timestamps, start_time, prompt_name="Test"):
    log_time(timestamps, start_time, "get_template", start=True)
    template = await async_pl.templates.get(prompt_name)
    log_time(timestamps, start_time, "get_template", start=False)
    return template

async def track_metadata(timestamps, start_time, pl_request_id):
    log_time(timestamps, start_time, "track_metadata", start=True)
    await async_pl.track.metadata(pl_request_id, {"test": "test"})
    log_time(timestamps, start_time, "track_metadata", start=False)

async def track_score(timestamps, start_time, pl_request_id):
    log_time(timestamps, start_time, "track_score", start=True)
    await async_pl.track.score(pl_request_id, 100)
    log_time(timestamps, start_time, "track_score", start=False)

async def track_prompt(timestamps, start_time, pl_request_id):
    log_time(timestamps, start_time, "track_prompt", start=True)
    await async_pl.track.prompt(pl_request_id, "Test", {})
    log_time(timestamps, start_time, "track_prompt", start=False)

async def log_request(timestamps, start_time, pl_request_id, template):
    log_time(timestamps, start_time, "track_request", start=True)
    await async_pl.log_request(
        provider="openai",
        model="gpt-4o-mini",
        input=template["prompt_template"],
        output=template["prompt_template"],
        request_start_time=time.time(),
        request_end_time=time.time(),
    )
    log_time(timestamps, start_time, "track_request", start=False)

async def main_func():
    timestamps = []
    start_time = time.time()

    # First async operation to fetch the template
    template = await fetch_template(timestamps, start_time, "Test")

    # Simulate an OpenAI request
    log_time(timestamps, start_time, "openai_request", start=True)
    OpenAI = pl.openai.OpenAI
    response, pl_request_id = OpenAI().chat.completions.create(
        **template["llm_kwargs"], return_pl_id=True
    )
    log_time(timestamps, start_time, "openai_request", start=False)

    # Run tracking operations in parallel, logging time for each
    await asyncio.gather(
        track_metadata(timestamps, start_time, pl_request_id),
        track_score(timestamps, start_time, pl_request_id),
        track_prompt(timestamps, start_time, pl_request_id),
        log_request(timestamps, start_time, pl_request_id, template)
    )

    return timestamps

async def main():
    start_time = time.time()
    print("Start")
    timestamps = await main_func()
    print("End")
    print("latency: ", time.time() - start_time)

    # Create a plot to visualize the timings
    create_plot(timestamps=timestamps, title="Parallel Execution of Async Tasks (Time in ms)")

# Run the main function
asyncio.run(main())
