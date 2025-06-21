from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
from tqdm import tqdm
from enum import Enum, auto
import asyncio
import json
import re
from concurrent.futures import ThreadPoolExecutor


load_dotenv()
llm_thread_pool = ThreadPoolExecutor(max_workers=16)
gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


class MODEL(Enum):
    GEMINI_PRO = auto()
    GEMINI_FLASH = auto()
    GEMINI_FLASH_LIGHT = auto()

    def model_name(self) -> str:
        if self == MODEL.GEMINI_PRO:
            return "gemini-2.5-pro"
        elif self == MODEL.GEMINI_FLASH:
            return "gemini-2.5-flash"
        elif self == MODEL.GEMINI_FLASH_LIGHT:
            return "gemini-2.5-flash-lite-preview-06-17"
        else:
            raise ValueError(f"Unknown model: {self}")

    def __str__(self) -> str:
        return self.name


def call_llm(prompt: str, model: MODEL) -> str:
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=-1, include_thoughts=True),
        response_mime_type="text/plain",
    )

    response_text = ""
    stream = gemini_client.models.generate_content_stream(
        model=model.model_name(),
        contents=contents,
        config=generate_content_config,
    )

    with tqdm(desc=f"Calling {model}", leave=False) as pbar:
        for chunk in stream:
            if chunk.text:
                response_text += chunk.text
            pbar.update(1)

    return response_text


def call_llm_json(prompt: str, model: MODEL):
    response = call_llm(prompt, model)
    # Try to extract JSON from markdown code block
    match = re.search(r"```json\s*(.*?)\s*```", response, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        json_str = response
    try:
        return json.loads(json_str)
    except Exception:
        print("Failed to parse JSON. json_str was:")
        print(json_str)
        raise


async def call_llm_async(prompt: str, model: MODEL) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: call_llm(prompt, model))
