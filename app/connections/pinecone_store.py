from typing import Any, Iterable
from pinecone import Pinecone

from app.core.config import settings


class PineconeStore:
    def __init__(self) -> None:
        pc = Pinecone(api_key=settings.pinecone_api_key)
        self.index = pc.Index(settings.pinecone_index)

    def semantic_query(
        self,
        vector: list[float],
        top_k: int,
        namespace: str,
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        res = self.index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True,
            namespace=namespace,
            filter=filters or None,
        )

        hits: list[dict[str, Any]] = []
        for m in (res.get("matches") or []):
            hits.append(
                {
                    "id": m.get("id"),
                    "score": float(m.get("score") or 0.0),
                    "metadata": m.get("metadata") or {},
                }
            )
        return hits

    def fetch_all_by_metadata(
        self,
        namespace: str,
        filters: dict[str, Any],
        page_size: int,
        max_results: int,
    ) -> Iterable[dict[str, Any]]:
        """
        Uses Pinecone bulk operation fetch_by_metadata (paginated) to retrieve vectors matching a filter.
        Returns id + metadata only.
        """
        pagination_token: str | None = None
        yielded = 0

        while True:
            resp = self.index.fetch_by_metadata(
                filter=filters or {},
                namespace=namespace,
                limit=page_size,
                pagination_token=pagination_token,
            )

            vectors = getattr(resp, "vectors", None) or {}
            for vid, v in vectors.items():
                if yielded >= max_results:
                    return
                md = getattr(v, "metadata", None) or {}
                yield {"id": str(vid), "metadata": md}
                yielded += 1

            pagination = getattr(resp, "pagination", None)
            next_token = getattr(pagination, "next", None) if pagination else None
            if not next_token:
                return
            pagination_token = next_token
