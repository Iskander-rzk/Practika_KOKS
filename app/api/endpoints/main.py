from fastapi import APIRouter, Request
from app.crud.crud import get_all_ip_addresses
from app.core.templates import templates

router = APIRouter()

@router.get("/")
async def read_root(request: Request):
    ip_addresses = get_all_ip_addresses()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "ip_addresses": ip_addresses}
    )