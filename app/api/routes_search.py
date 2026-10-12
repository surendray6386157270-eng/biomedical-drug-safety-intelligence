from fastapi import APIRouter, HTTPException, Query

from app.services.search import search_drug_evidence

router = APIRouter(prefix="/api", tags=["search"])


@router.get("/drugs/{drug_name}/evidence")
def search_evidence(
    drug_name: str,
    limit: int = Query(default=20, ge=1, le=100),
):
    try:
        evidence = search_drug_evidence(drug_name, limit=limit)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "drug_name": drug_name,
        "count": len(evidence),
        "evidence": evidence,
    }