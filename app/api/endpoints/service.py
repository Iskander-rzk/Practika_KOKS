from fastapi import APIRouter, UploadFile, File, Request
from app.core.templates import templates
from app.controller import controller
from app.models.models import Errors
from app.crud import crud
from fastapi.responses import RedirectResponse

router = APIRouter()

ERROR_MESSAGES = {
    Errors.DBError: "Database operation failed",
    Errors.Invalid: "Invalid file format",
}

@router.post("/export")
def export_ips(request: Request):
    response = controller.export_ips()
    if response.error:
        error_msg = ERROR_MESSAGES.get(response.error, "Export failed")
        ip_addresses = crud.get_all_ip_addresses()
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": error_msg,
                "ip_addresses": ip_addresses
            }
        )
    return RedirectResponse(url="/?message=IPs exported successfully", status_code=303)

@router.post("/import")
def import_ips(request: Request):
    response = controller.import_ips()
    if response.error:
        error_msg = ERROR_MESSAGES.get(response.error, "Import failed")
        ip_addresses = crud.get_all_ip_addresses()
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": error_msg,
                "ip_addresses": ip_addresses
            }
        )
    return RedirectResponse(url="/?message=IPs imported successfully", status_code=303)

@router.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    response = await controller.upload_and_import(file)
    if response.error:
        error_msg = ERROR_MESSAGES.get(response.error, "File processing failed")
        ip_addresses = crud.get_all_ip_addresses()
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": error_msg,
                "ip_addresses": ip_addresses
            }
        )
    return RedirectResponse(url="/?message=File uploaded and IPs imported", status_code=303)