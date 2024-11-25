import spacy

# This class takes care of initial processing of raw text by tokenizing, normalizing and lemmatizing it
class TextPreprocessor:
    def __init__(self, model = "en_core_web_sm"):
        self.nlp = spacy.load(model)

    def preprocess(self, text : str) -> str:
        # tokenizing
        doc = self.nlp(text.lower())
        # normalizing and lemmatizing
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        return " ".join(tokens)
