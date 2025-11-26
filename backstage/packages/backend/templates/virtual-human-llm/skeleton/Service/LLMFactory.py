from typing import Any

from Service.loadModule.APILLM import APILLM
from Service.loadModule.LocalLLM import LocalLLM


class LLMFactory:
    def __init__(self):
        self.model_name = None
        self.current_model = None
        self.localLLM = LocalLLM()
        self.apiLLM = APILLM()

    def _is_model_allowed(self, model_name: str) -> bool:
        allowed_names = self.localLLM.ALLOWED_LOCAL_MODELS + self.apiLLM.ALLOWED_LOCAL_MODELS
        return model_name in allowed_names

    def list_of_all_models(self) -> None:
        print("--- LOCAL ---")
        for model_name in self.localLLM.ALLOWED_LOCAL_MODELS:
            print(f"- {model_name}")
        print("--- OPEN API ---")
        for model_name in self.apiLLM.ALLOWED_LOCAL_MODELS:
            print(f"- {model_name}")

    def _get_model(self, model_name: str) -> Any:
        if not self._is_model_allowed(model_name):
            raise AttributeError("Error: this model is not allowed")

        self.model_name = model_name
        if model_name in self.localLLM.ALLOWED_LOCAL_MODELS:
            self.current_model = self.localLLM.load_model(model_name)
        else:
            self.current_model = self.apiLLM.load_model(model_name)

    def get_response(self, messages: list, max_tokens: int, tools: list, model_name: str = "gpt-5-mini") -> dict:
        if not self.current_model or self.model_name != model_name:
            self._get_model(model_name)

        if self.model_name in self.localLLM.ALLOWED_LOCAL_MODELS:
            return self.localLLM.get_response(self.current_model, messages, max_tokens, tools)
        else:
            return self.apiLLM.get_response(self.current_model, messages, max_tokens, tools)
