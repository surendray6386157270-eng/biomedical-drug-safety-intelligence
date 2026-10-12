from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.routes_analysis import router as analysis_router
from app.api.routes_health import router as health_router
from app.api.routes_ingestion import router as ingestion_router
from app.api.routes_search import router as search_router


app = FastAPI(
    title="Biomedical Drug Safety Evidence Intelligence System",
    version="0.1.0",
    description=(
        "Research prototype for retrieving, normalizing, searching, "
        "and analyzing biomedical drug-safety evidence."
    ),
)


app.include_router(health_router)
app.include_router(search_router)
app.include_router(analysis_router)
app.include_router(ingestion_router)


UI_PATH = Path(__file__).parent / "ui" / "index.html"


@app.get("/", include_in_schema=False)
def researcher_interface():
    return FileResponse(UI_PATH)