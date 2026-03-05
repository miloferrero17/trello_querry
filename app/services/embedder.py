from openai import OpenAI
from app.core.config import settings


class Embedder:
    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is required when query_text is provided.")
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_embed_model

    def embed(self, text: str) -> list[float]:
        text = text.strip()
        if not text:
            raise ValueError("query_text is empty.")
        res = self.client.embeddings.create(model=self.model, input=text)
        return list(res.data[0].embedding)
