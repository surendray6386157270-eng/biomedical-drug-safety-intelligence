from fastapi import APIRouter, HTTPException, Query

from app.services.analysis import analyze_drug

router = APIRouter(prefix="/api", tags=["analysis"])


@router.get("/drugs/{drug_name}/analysis")
def drug_analysis(
    drug_name: str,
    limit: int = Query(default=100, ge=1, le=100),
):
    try:
        result = analyze_drug(drug_name, limit=limit)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return result