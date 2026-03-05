from typing import Any

from app.core.config import settings
from app.connections.pinecone_store import PineconeStore
from app.services.embedder import Embedder


def extract_chunk(metadata: dict[str, Any]) -> str | None:
    return (
        metadata.get("chunk")
        or metadata.get("text")
        or metadata.get("content")
        or metadata.get("body")
        or metadata.get("description")
    )


class SearchOrchestrator:
    def __init__(self, store: PineconeStore) -> None:
        self.store = store

    def search(
        self,
        *,
        filters: dict[str, Any],
        namespace: str,
        query_text: str | None,
        top_k: int | None,
    ) -> tuple[str, list[dict[str, Any]]]:
        if query_text:
            k = top_k or settings.default_query_top_k
            vector = Embedder().embed(query_text)
            hits = self.store.semantic_query(vector=vector, top_k=k, namespace=namespace, filters=filters)
            out = []
            for h in hits:
                md = h.get("metadata") or {}
                out.append(
                    {
                        "id": str(h.get("id")),
                        "score": float(h.get("score") or 0.0),
                        "metadata": md,
                        "chunk": extract_chunk(md),
                    }
                )
            return "semantic", out

        limit = top_k if top_k is not None else settings.max_results
        out = []
        for row in self.store.fetch_all_by_metadata(
            namespace=namespace,
            filters=filters,
            page_size=settings.page_size,
            max_results=limit,
        ):
            md = row.get("metadata") or {}
            out.append(
                {
                    "id": str(row.get("id")),
                    "score": None,
                    "metadata": md,
                    "chunk": extract_chunk(md),
                }
            )
        return "filters_only", out
