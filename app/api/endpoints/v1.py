from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from app.core.templates import templates
from app.controller import controller
from app.models import models

router = APIRouter()



@router.post("/add")
def add_ip_address(request: Request, ip: str = Form(...)):
    input = models.IPAddressRequest(ip_address=ip)
    result = controller.add_ip(input)

    if result.error:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": result.error.string(),
                "ip_addresses": result.ip_addresses
            }
        )

    return RedirectResponse(url="/", status_code=303)


@router.get("/search")
async def search_ips(request: Request, ip: str = ""):
    response = controller.search_ip(ip)

    if response.error:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "ip_addresses": response.ip_addresses,
                "search_term": ip,
                "error": response.error.string()
            }
        )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "ip_addresses": response.ip_addresses,
            "search_term": ip
        }
    )


@router.post("/delete/{ip_address}")
async def remove_ip_address(request: Request, ip_address: str):
    response = controller.remove_ip(ip_address)
    if response.error:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": response.error.string(),
                "ip_addresses": response.ip_addresses
            }
        )
    return RedirectResponse(url="/?message=IP deleted", status_code=303)