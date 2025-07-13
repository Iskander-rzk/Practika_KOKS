from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from app.core.templates import templates
from app.controller import controller
from app.models import models

router = APIRouter()

error_messages = {
            models.Errors.Invalid: "Invalid IP address",
            models.Errors.Exist: "IP address exists",
            models.Errors.DBError: "Database error"
        }

@router.post("/add")
def add_ip_address(request: Request, ip: str = Form(...)):
    input = models.IPAddressRequest(ip_address=ip)
    result = controller.add_ip(input)
    if result.error:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": error_messages[result.error],
                "ip_addresses": result.ip_addresses
            }
        )

    return RedirectResponse(url="/", status_code=303)


@router.get("/search")
async def search_ips(request: Request, q: str):
    response = controller.search_ip(q)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "ip_addresses": response.ip_addresses,
            "search_term": q
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
                "error": "Database error",
                "ip_addresses": response.ip_addresses
            }
        )
    return RedirectResponse(url="/?message=IP deleted", status_code=303)



# @router.get("/search")
# async def search_ips(request: Request, q: str):
#     response = search_ip(q)
#     if response.status:
#         return templates.TemplateResponse(
#             "index.html",
#             {
#                 "request": request,
#                 "ip_addresses": response.ip_addresses,
#                 "search_term": q,
#                 "error": response.error or "Search failed"
#             }
#         )
#     return templates.TemplateResponse(
#         "index.html",
#         {
#             "request": request,
#             "ip_addresses": response.ip_addresses,
#             "search_term": q
#         }
#     )

# @router.post("/delete/{ip_address}")
# async def remove_ip_address(request: Request, ip_address: str):
#     response = remove_ip(ip_address)
#     if response.status:
#         return RedirectResponse(url=f"/?error={response.error}", status_code=303)
#     return RedirectResponse(url=f"/?message={response.message}", status_code=303)
