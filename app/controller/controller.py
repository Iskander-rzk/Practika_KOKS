from app.crud import crud
from app.models import models
from fastapi import UploadFile
import os

IP_FILE_PATH = "ip_addresses.txt"


def add_ip(input: models.IPAddressRequest) -> models.IPAddressResponse:
    if not input.is_valid():
        return models.IPAddressResponse(error=models.Errors.Invalid)
    if crud.select(input.ip_address):
        return models.IPAddressResponse(error=models.Errors.Exist)
    if not crud.create_ip_address(input.ip_address):
        return models.IPAddressResponse(error=models.Errors.DBError)
    return models.IPAddressResponse()


def add_ip_for_handler(input: models.IPAddressRequest) -> models.IPAddressResponse:
    result = add_ip(input)
    if not result.error:
        result.ip_addresses = crud.get_all_ip_addresses()
    return result


def search_ip(ip: str) -> models.IPAddressResponse:
    temp_request = models.IPAddressRequest(ip_address=ip)
    if not temp_request.is_valid():
        all_ips = crud.get_all_ip_addresses()
        return models.IPAddressResponse(
            error=models.Errors.Invalid,
            ip_addresses=all_ips
        )
    results = crud.search_ip_addresses(ip)
    return models.IPAddressResponse(ip_addresses=results)


def remove_ip(ip_address: str) -> models.IPAddressResponse:
    success = crud.delete_ip_address(ip_address)
    if not success:
        return models.IPAddressResponse(error=models.Errors.DBError)
    ip_addresses = crud.get_all_ip_addresses()
    return models.IPAddressResponse(ip_addresses=ip_addresses)


def export_ips() -> models.OperationResponse:
    ip_addresses = crud.get_all_ip_addresses()
    with open(IP_FILE_PATH, "w") as f:
        for ip in ip_addresses:
            f.write(f"{ip.ip_address}\n")
    return models.OperationResponse(message="Export successful")


def import_ips() -> models.OperationResponse:
    if not os.path.exists(IP_FILE_PATH):
        return models.OperationResponse(error=models.Errors.Invalid)

    ip_addresses=crud.get_all_ip_addresses()
    with open(IP_FILE_PATH, 'r') as f:
        for line in f:
            ip = line.strip()
            if ip:
                add_ip_for_handler(models.IPAddressRequest(ip_address=ip))
    return models.OperationResponse(message="Import successful", ip_addresses=ip_addresses)


def upload_and_import(file: UploadFile) -> models.OperationResponse:
    content = file.file.read()
    ip_addresses=crud.get_all_ip_addresses()

    for line in content.decode('utf-8').splitlines():
        ip = line.strip()
        if ip:
            add_ip_for_handler(models.IPAddressRequest(ip_address=ip))

    return models.OperationResponse(message="Upload completed", ip_addresses=ip_addresses)