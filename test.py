import os
import time
import asyncio
from promptlayer import PromptLayer, AsyncPromptLayer
from log_time import log_time
from create_plot import create_plot
from dotenv import load_dotenv


load_dotenv()
# values are taken from the environment when the class is created
PROMPTLAYER_API_KEY = os.getenv("PROMPTLAYER_API_KEY")

async_pl = AsyncPromptLayer(
    api_key=PROMPTLAYER_API_KEY
)

pl = PromptLayer(
    api_key=PROMPTLAYER_API_KEY
)


async def main_func():
    timestamps = []

    start_time = time.time()

    # First async operation
    get_template_start = log_time(timestamps, start_time, "get_template")
    template = await async_pl.templates.get("Test")
    log_time(timestamps, start_time, "get_template", start=False)

    # Start async calls that can be parallelized
    openai_request_start = log_time(timestamps, start_time, "openai_request")
    OpenAI = pl.openai.OpenAI
    response, pl_request_id = OpenAI().chat.completions.create(
        **template["llm_kwargs"], return_pl_id=True
    )
    log_time(timestamps, start_time, "openai_request", start=False)

    track_metadata_start = log_time(timestamps, start_time, "track_metadata")
    await async_pl.track.metadata(pl_request_id, {"test": "test"})    
    log_time(timestamps, start_time, "track_metadata", start=False)


    track_score_start = log_time(timestamps, start_time, "track_score")
    await async_pl.track.score(pl_request_id, 100)
    log_time(timestamps, start_time, "track_score", start=False)

    
    track_prompt_start = log_time(timestamps, start_time, "track_prompt")
    await async_pl.track.prompt(pl_request_id, "Test", {})
    log_time(timestamps, start_time, "track_prompt", start=False)

    track_request_start = log_time(timestamps, start_time, "track_request")
    await async_pl.log_request(
        provider="openai",
        model="gpt-4o-mini",
        input=template["prompt_template"],
        output=template["prompt_template"],
        request_start_time=time.time(),
        request_end_time=time.time(),
    )
    log_time(timestamps, start_time, "track_request", start=False)

    return timestamps


async def main():
    start_time = time.time()
    print("Start")
    timestamps = await main_func()
    print("End")
    print("latency: ", time.time() - start_time)

    create_plot(timestamps=timestamps)

# Run the main function
asyncio.run(main())
