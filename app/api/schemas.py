from pydantic import BaseModel, Field
from typing import Any


class SearchRequest(BaseModel):
    # Filters-only is the default mode (required)
    filters: dict[str, Any] = Field(..., description="Pinecone metadata filter object")

    # Optional: semantic ranking within the filtered subset
    query_text: str | None = Field(default=None, description="Optional text for semantic search (embedding)")

    # Optional overrides
    namespace: str | None = Field(default=None, description="Override Pinecone namespace for this request")

    # Optional: number of results
    # If omitted -> "all matches" for filters-only mode (via fetch_by_metadata pagination)
    # If query_text provided and top_k omitted -> uses DEFAULT_QUERY_TOP_K
    top_k: int | None = Field(default=None, ge=1, le=1000)


class SearchHit(BaseModel):
    id: str
    score: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    chunk: str | None = None


class SearchResponse(BaseModel):
    mode: str
    namespace: str
    returned: int
    results: list[SearchHit]
