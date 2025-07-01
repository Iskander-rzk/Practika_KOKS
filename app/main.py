from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pathlib import Path
import os

# Убедитесь, что все импорты начинаются с app.
from app.crud import (
    create_ip_address,
    get_all_ip_addresses,
    delete_ip_address,
    search_ip_addresses,
    import_from_file,
    export_to_file
)

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))
static_dir = Path(BASE_DIR, 'static')
static_dir.mkdir(exist_ok=True)  # Создаем папку static, если её нет
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

IP_FILE_PATH = "ip_addresses.txt"


@app.get("/")
async def read_root(request: Request):
    ip_addresses = get_all_ip_addresses()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "ip_addresses": ip_addresses}
    )

@app.post("/add")
async def add_ip_address(ip: str = Form(...), description: str = Form("")):
    create_ip_address(ip, description)
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete/{ip_address}")
async def remove_ip_address(ip_address: str):
    delete_ip_address(ip_address)
    return RedirectResponse(url="/", status_code=303)

@app.get("/search")
async def search_ips(request: Request, q: str):
    results = search_ip_addresses(q)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "ip_addresses": results, "search_term": q}
    )

@app.post("/import")
async def import_ips():
    import_from_file(IP_FILE_PATH)
    return RedirectResponse(url="/", status_code=303)

@app.post("/export")
async def export_ips():
    export_to_file(IP_FILE_PATH)
    return RedirectResponse(url="/", status_code=303)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        with open(IP_FILE_PATH, 'wb') as f:
            f.write(contents)
        import_from_file(IP_FILE_PATH)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        return {"error": str(e)}
    finally:
        await file.close()