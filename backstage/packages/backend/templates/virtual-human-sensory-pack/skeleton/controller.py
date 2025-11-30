import logging
import time

from flask import Flask, request, jsonify

from sensory_handler import start_sensory_handler
from services.extract_emotion import ExtractEmotion

app = Flask(__name__)
extract_emotion = ExtractEmotion()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/api/emotion", methods=["POST"])
def emotion():
    try:
        data = request.get_json(force=True, silent=False)
        logger.info(f"Received data: {data}")
    except Exception as e:
        logger.error(f"Invalid JSON: {e}", exc_info=True)
        return jsonify({"error": "Invalid JSON payload"}), 400

    user_query = data.get("query", [])

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    try:
        emotion_response = extract_emotion.get_emotion(user_query)
    except Exception as e:
        logger.exception(f"LLM processing error: {e}")
        return jsonify({"error": f"LLM processing error: {e}"}), 500

    response_payload = {
        "emotion": emotion_response,
        "query": user_query,
    }

    logger.info(f"Returning successful emotion response")
    return jsonify(response_payload), 200


if __name__ == "__main__":
    try:
        start_sensory_handler()
        logger.info("Successfully launched sensory handler (kafka consumer and producer)")
    except Exception as e:
        logger.error(f"Failed to launch sensory handler: {e}", exc_info=True)

    app.run(host="0.0.0.0", port=5000, debug=False)
