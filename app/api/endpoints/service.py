from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import RedirectResponse
from app.core.templates import templates
from app.controller import controller


router = APIRouter()


@router.post("/export")
def export_ips(request: Request):
    response = controller.export_ips()
    if response.error:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": response.error.string(),
                "ip_addresses": response.ip_addresses
            }
        )
    return RedirectResponse(url="/?message=IPs exported successfully", status_code=303)


@router.post("/import")
def import_ips(request: Request):
    response = controller.import_ips()
    if response.error:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": response.error.string(),
                "ip_addresses": response.ip_addresses
            }
        )
    return RedirectResponse(url="/?message=IPs imported successfully", status_code=303)


@router.post("/upload")
def upload_file(request: Request, file: UploadFile = File(...)):
    response = controller.upload_and_import(file)
    if response.error:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": response.error.string(),
                "ip_addresses": response.ip_addresses
            }
        )
    return RedirectResponse(url="/?message=IPs upload successfully", status_code=303)
