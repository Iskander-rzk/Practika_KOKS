from app.crud import crud
from app.models import models


def add_ip(input: models.IPAddressRequest) -> models.IPAddressResponse:
    if not input.is_valid():
        return models.IPAddressResponse(error=models.Errors.Invalid)

    existing = crud.select(input.ip_address)
    if existing:
        return models.IPAddressResponse(error=models.Errors.Exist)

    success = crud.create_ip_address(input.ip_address)
    if not success:
        return models.IPAddressResponse(error=models.Errors.DBError)

    ip_addresses = crud.get_all_ip_addresses()
    return models.IPAddressResponse(ip_addresses=ip_addresses)



def search_ip(q: str) -> models.IPAddressResponse:
    results = crud.search_ip_addresses(q)
    return models.IPAddressResponse(ip_addresses=results)


def remove_ip(ip_address: str) -> models.IPAddressResponse:
    success = crud.delete_ip_address(ip_address)
    if not success:
        return models.IPAddressResponse(error=models.Errors.DBError)

    ip_addresses = crud.get_all_ip_addresses()
    return models.IPAddressResponse(ip_addresses=ip_addresses)

#def search_ip(input: models.IPAddressRequest):
#    results = search_ip_addresses(q)
#    return templates.TemplateResponse(
#        "index.html",
#        {
#            "request": request,
#            "ip_addresses": results,
#            "search_term": q
#        }
#    )

#def remove_ip(ip_address: str):
#    success = delete_ip_address(ip_address)
#    if not success:
#        return RedirectResponse(url="/?error=Failed to delete IP", status_code=303)
#    return RedirectResponse(url="/?message=IP deleted successfully", status_code=303)
