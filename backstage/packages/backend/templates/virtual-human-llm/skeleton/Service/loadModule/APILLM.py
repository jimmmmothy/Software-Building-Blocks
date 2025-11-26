import logging
import os
from typing import Any

from openai import OpenAI


class APILLM:
    def __init__(self):
        self.ALLOWED_LOCAL_MODELS = [
            "gpt-5",
            "gpt-5-mini",
            "gpt-4",
            "gpt-4-mini"
        ]
        self.logger = logging.getLogger(__name__)

    def load_model(self, model_name: str) -> Any:
        if model_name not in self.ALLOWED_LOCAL_MODELS:
            raise AttributeError("Error: this model is not allowed")

        if not os.getenv("OPEN_AI_KEY"):
            raise EnvironmentError("Error: open ai key is not set")

        client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))
        return model_name, client

    def get_response(self, current_model, messages: list, max_tokens: int, tools: list) -> dict:
        model_name = current_model[0]
        client = current_model[1]

        gpt_response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=max_tokens,
            tools=tools
        )

        return gpt_response
