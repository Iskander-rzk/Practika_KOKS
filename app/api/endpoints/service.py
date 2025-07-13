from fastapi import APIRouter, UploadFile, File
from fastapi.responses import RedirectResponse
from app.crud import crud

router = APIRouter()
IP_FILE_PATH = "ip_addresses.txt"


@router.post("/export")
async def export_ips():
    if crud.export_to_file(IP_FILE_PATH):
        return RedirectResponse(url="/?message=IPs exported", status_code=303)
    return RedirectResponse(url="/?error=Export failed", status_code=303)


@router.post("/import")
async def import_ips():
    if crud.import_from_file(IP_FILE_PATH):
        return RedirectResponse(url="/?message=IPs imported", status_code=303)
    return RedirectResponse(url="/?error=Import failed", status_code=303)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.txt'):
        return RedirectResponse(url="/?error=Invalid file type", status_code=303)

    try:
        contents = await file.read()
        with open(IP_FILE_PATH, 'wb') as f:
            f.write(contents)

        if crud.import_from_file(IP_FILE_PATH):
            return RedirectResponse(url="/?message=File imported", status_code=303)
        return RedirectResponse(url="/?error=Import failed", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/?error={str(e)}", status_code=303)