import os
import time
import asyncio
from promptlayer import PromptLayer, AsyncPromptLayer
from create_plot import create_plot
from log_time import log_time
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

    # Run tracking metadata, score, prompt, and request in parallel
    track_metadata_start = log_time(timestamps, start_time, "track_metadata")
    track_score_start = log_time(timestamps, start_time, "track_score")
    track_prompt_start = log_time(timestamps, start_time, "track_prompt")
    track_request_start = log_time(timestamps, start_time, "track_request")

    await asyncio.gather(
        async_pl.track.metadata(pl_request_id, {"test": "test"}),  # Metadata tracking
        async_pl.track.score(pl_request_id, 100),  # Score tracking
        async_pl.track.prompt(pl_request_id, "Test", {}),  # Prompt tracking
        async_pl.log_request(  # Request logging
            provider="openai",
            model="gpt-4o-mini",
            input=template["prompt_template"],
            output=template["prompt_template"],
            request_start_time=time.time(),
            request_end_time=time.time(),
        )
    )

    log_time(timestamps, start_time, "track_metadata", start=False)
    log_time(timestamps, start_time, "track_score", start=False)
    log_time(timestamps, start_time, "track_prompt", start=False)
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
