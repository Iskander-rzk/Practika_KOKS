from app.crud import crud
from app.models import models
from fastapi import UploadFile

IP_FILE_PATH = "ip_addresses.txt"

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


def export_ips() -> models.OperationResponse:
    ip_addresses = crud.get_all_ip_addresses()
    try:
        with open(IP_FILE_PATH, "w") as f:
            for ip in ip_addresses:
                f.write(f"{ip.ip_address}\n")
        return models.OperationResponse(message="Export successful")
    except Exception:
        return models.OperationResponse(error=models.Errors.DBError)


def import_ips() -> models.OperationResponse:
    try:
        with open(IP_FILE_PATH, "r") as f:
            ips = [line.strip() for line in f.readlines()]

        for ip in ips:
            if not crud.select(ip):
                crud.create_ip_address(ip)
        return models.OperationResponse(message="Import successful")
    except Exception:
        return models.OperationResponse(error=models.Errors.Invalid)


async def upload_and_import(file: UploadFile) -> models.OperationResponse:
    content = await file.read()
    try:
        ips = content.decode().splitlines()
        valid_ips = []
        for ip in ips:
            req = models.IPAddressRequest(ip_address=ip)
            if req.is_valid():
                valid_ips.append(ip)

        for ip in valid_ips:
            if not crud.select(ip):
                crud.create_ip_address(ip)
        return models.OperationResponse(message="Upload successful")
    except Exception:
        return models.OperationResponse(error=models.Errors.Invalid)