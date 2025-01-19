import logging
from concurrent.futures import ThreadPoolExecutor

import spacy

class TextPreprocessor:
    __DEFAULT_MODEL = "en_core_web_sm"

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.nlp = None

    def init(self, model = __DEFAULT_MODEL):
        self.nlp = spacy.load(model)
        self.logger.info("TextPreprocessor initialized")

    def tokenize(self, text: str) -> list:
        if not self.nlp:
            raise ValueError("TextPreprocessor not initialized")
        doc = self.nlp(text.lower())
        return [token.orth_ for token in doc]

    def preprocess(self, text : str) -> str:
        if not self.nlp:
            raise ValueError("TextPreprocessor not initialized")
        doc = self.nlp(text.lower())
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        return " ".join(tokens)

    def preprocess_multiple(self, texts: list[str]) -> list[str]:
        with ThreadPoolExecutor() as executor:
            preprocessed = list(executor.map(self.preprocess, texts))
        return preprocessed
