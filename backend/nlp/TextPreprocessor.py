import logging

import spacy

class TextPreprocessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.nlp = None

    async def init_async(self, model = "en_core_web_sm"):
        self.nlp = spacy.load(model)
        self.logger.info("TextPreprocessor initialized")

    def preprocess(self, text : str) -> str:
        if not self.nlp:
            raise ValueError("TextPreprocessor not initialized")
        doc = self.nlp(text.lower())
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        return " ".join(tokens)
