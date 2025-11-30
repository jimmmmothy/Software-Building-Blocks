import logging
from threading import Lock

from transformers import pipeline


class ExtractEmotion:
    _instance = None
    _lock = Lock()  # for thread safety

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self.classifier = None
        self.MODEL = "michellejieli/emotion_text_classifier"
        self.logger = logging.getLogger(__name__)

    def _load_model(self) -> None:
        try:
            if not self.classifier:
                self.logger.info("Loading emotion model")
                self.classifier = pipeline("sentiment-analysis", model=self.MODEL)
                self.logger.info("Loaded emotion model successfully")
            else:
                self.logger.info("Model is already loaded")
        except Exception as e:
            self.logger.error(f"Failed to load emotion model: {e}", exc_info=True)
            self.classifier = None

    def get_emotion(self, user_query: str) -> None | list:
        self._load_model()
        if not self.classifier:
            self.logger.error("No model loaded")
            return None

        try:
            result = self.classifier(user_query)
            return result
        except Exception as e:
            self.logger.error(f"Error during emotion prediction: {e}", exc_info=True)
            return None
