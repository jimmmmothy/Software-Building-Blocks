import json
import re
from typing import Tuple, Any
import time
import logging

from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch


class LocalLLM:
    def __init__(self):
        self.ALLOWED_LOCAL_MODELS = [
            "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
            "Qwen/Qwen2.5-1.5B-Instruct",
            "meta-llama/Llama-3.2-1B"
        ]
        self.logger = logging.getLogger(__name__)

    def load_model(self, model_name: str) -> Tuple:
        if model_name not in self.ALLOWED_LOCAL_MODELS:
            raise AttributeError("Error: this model is not allowed")

        self.logger.info(f"Loading model: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        quantization_config = BitsAndBytesConfig(
            load_in_8bit=True,
            llm_int8_threshold=6.0,
        )

        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="cuda:0",
            quantization_config=quantization_config,
        )

        self.logger.info(f"Model ({model_name}) loaded.")

        return tokenizer, model

    def get_response(self, current_model, messages: list, max_tokens: int, tools: list) -> dict:
        tokenizer = current_model[0]
        model = current_model[1]

        formatted_input = tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
            padding=True,
            tools=tools,
        )

        input_ids = formatted_input.to(model.device)

        attention_mask = getattr(formatted_input, "attention_mask", None)
        if attention_mask is None:
            attention_mask = torch.ones_like(input_ids, device=model.device)
        else:
            attention_mask = attention_mask.to(model.device)

        start_time = time.time()
        with torch.no_grad():
            outputs = model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_new_tokens=max_tokens,
                do_sample=True,
                temperature=0.7,
                top_k=50,
                top_p=0.9,
                pad_token_id=tokenizer.eos_token_id,
            )

        gen_tokens = outputs[0][input_ids.shape[-1]:]
        final_answer = tokenizer.decode(gen_tokens, skip_special_tokens=True).strip()
        final_answer = self._convert_answer_for_MCP(final_answer)

        elapsed_time = time.time() - start_time
        self.logger.info(f"Generated response in {elapsed_time:.2f}s")

        return final_answer

    def _convert_answer_for_MCP(self, answer: str) -> dict:
        tool_call_matches = re.findall(r"<tool_call>\s*(\{.*?})\s*</tool_call>", answer, re.DOTALL)
        tool_calls = []

        if tool_call_matches:
            for idx, match in enumerate(tool_call_matches, start=1):
                try:
                    tool_json = json.loads(match)
                    tool_calls.append({
                        "id": f"call_{idx}",
                        "function": {
                            "name": tool_json["name"],
                            "arguments": json.dumps(tool_json["arguments"])
                        }
                    })
                except Exception as e:
                    self.logger.error(f"Failed to parse tool_call JSON: {e}")
                    continue

            return {"tool_calls": tool_calls, "content": None}
        else:
            # no tool calls, just return content
            return {"tool_calls": None, "content": answer}
