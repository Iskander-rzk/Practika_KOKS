from fastapi import APIRouter, Request
from app.crud import crud
from app.core.templates import templates

router = APIRouter()


@router.get("/")
async def read_root(request: Request):
    ip_addresses = crud.get_all_ip_addresses()
    message = request.query_params.get("message", "")
    error = request.query_params.get("error", "")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "ip_addresses": ip_addresses,
            "message": message,
            "error": error
        }
    )