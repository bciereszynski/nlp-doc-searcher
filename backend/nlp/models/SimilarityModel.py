class SimilarityModel:
    async def init_async(self, documents: list[str]) -> None:
        pass

    async def reinit_async(self, documents: list[str]) -> None:
        pass

    def get_cosine_similarity(self, query: str) -> list[float]:
        pass
