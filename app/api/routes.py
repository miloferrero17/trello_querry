from fastapi import APIRouter, HTTPException
from app.api.schemas import SearchRequest, SearchResponse, SearchHit
from app.core.config import settings
from app.connections.pinecone_store import PineconeStore
from app.services.search_orchestrator import SearchOrchestrator

router = APIRouter(prefix="/v1", tags=["search"])


@router.get("/health")
def health():
    return {"ok": True, "service": settings.app_name}


@router.post("/search", response_model=SearchResponse)
def search(req: SearchRequest):
    try:
        namespace = req.namespace or settings.pinecone_namespace

        store = PineconeStore()
        orchestrator = SearchOrchestrator(store=store)

        mode, rows = orchestrator.search(
            filters=req.filters,
            namespace=namespace,
            query_text=req.query_text,
            top_k=req.top_k,
        )

        results = [
            SearchHit(
                id=r["id"],
                score=r.get("score"),
                metadata=r.get("metadata") or {},
                chunk=r.get("chunk"),
            )
            for r in rows
        ]

        return SearchResponse(
            mode=mode,
            namespace=namespace,
            returned=len(results),
            results=results,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")
