from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.crud import get_all_ip_addresses
from app.api.router import router as api_router
from app.templates import templates

app = FastAPI()
app.include_router(api_router)

BASE_DIR = Path(__file__).resolve().parent
static_dir = Path(BASE_DIR, 'static')
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

@app.get("/")
async def read_root(request: Request):
    ip_addresses = get_all_ip_addresses()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "ip_addresses": ip_addresses}
    )