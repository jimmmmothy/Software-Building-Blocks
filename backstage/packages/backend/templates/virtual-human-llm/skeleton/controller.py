import logging
import time

from flask import Flask, request, jsonify
from Service.LLMFactory import LLMFactory
import os

app = Flask(__name__)
llm_factory = LLMFactory()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = os.getenv("LLM_API_KEY", "my-secret-key")


def list_available_models():
    llm_factory.list_of_all_models()


@app.route("/v1/chat/completions", methods=["POST"])
def chat_completions():
    """
    OpenAI-compatible endpoint for MCP.
    Expected input:
    {
        "model": "Qwen/Qwen2.5-1.5B-Instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello DeepSeek, how are you?"}
        ]
    }
    """

    # auth_header = request.headers.get("Authorization", "")
    # if not auth_header.startswith("Bearer ") or auth_header.split(" ")[1] != API_KEY:
    #     return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    logger.info(f"received data: {data}")

    model_version = data.get("model", "")
    messages = data.get("messages", [])
    max_tokens = data.get("max_tokens", 512)
    tools = data.get("tools", [])

    if not messages:
        return jsonify({"error": "No messages provided"}), 400

    response_text = llm_factory.get_response(messages, max_tokens, tools, model_version)

    content = response_text["content"]
    tool_calls = response_text["tool_calls"]

    return jsonify({
        "id": "chatcmpl-local-001",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model_version,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content,
                    "tool_calls": tool_calls,
                },
                "finish_reason": "stop"
            }
        ]
    })


if __name__ == "__main__":
    print("Please view the list of available models:")
    list_available_models()
    print()
    app.run(host="0.0.0.0", port=5000, debug=False)
