from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import RedirectResponse
from app.core.templates import templates
from app.controller import controller

from app.crud import crud

router = APIRouter()


@router.post("/export")
def export_ips(request: Request):
    response = controller.export_ips()
    if response.error:
        ip_addresses = crud.get_all_ip_addresses()
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": response.error.string(),
                "ip_addresses": ip_addresses
            }
        )
    return RedirectResponse(url="/?message=IPs exported successfully", status_code=303)

@router.post("/import")
def import_ips(request: Request):
    response = controller.import_ips()
    if response.error:
        ip_addresses = crud.get_all_ip_addresses()
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": response.error.string(),
                "ip_addresses": ip_addresses
            }
        )
    return RedirectResponse(url="/?message=IPs imported successfully", status_code=303)

@router.post("/upload")
def upload_file(request: Request, file: UploadFile = File(...)):
    response = controller.upload_and_import(file)
    if response.error:
        all_ips = controller.search_ip("").ip_addresses
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": response.error.string(),
                "ip_addresses": all_ips
            }
        )
    return RedirectResponse(url="/?message=File uploaded and IPs imported", status_code=303)
