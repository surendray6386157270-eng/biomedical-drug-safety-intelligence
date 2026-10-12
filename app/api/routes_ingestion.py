from fastapi import APIRouter, HTTPException, Query

from app.services.pipeline import run_pipeline

router = APIRouter(prefix="/api", tags=["ingestion"])


@router.post("/drugs/{drug_name}/ingest")
def ingest_drug(
    drug_name: str,
    limit: int = Query(default=10, ge=1, le=100),
):
    try:
        result = run_pipeline(drug_name, limit=limit)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Source ingestion failed: {exc}",
        ) from exc

    return result