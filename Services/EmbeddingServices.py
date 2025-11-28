import random

class EmbeddingServices:
    def __init__(self):
        pass

    def fake_embed(self, text: str):
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(128)]