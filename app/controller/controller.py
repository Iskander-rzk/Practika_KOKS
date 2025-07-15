from app.crud import crud
from app.models import models
from fastapi import UploadFile
import os
import codecs
from pathlib import Path
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
    temp_request = models.IPAddressRequest(ip_address=q)
    if not temp_request.is_valid():
        all_ips = crud.get_all_ip_addresses()
        return models.IPAddressResponse(
            error=models.Errors.Invalid,
            ip_addresses=all_ips
        )

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

    file_path = Path(IP_FILE_PATH)
    if not file_path.parent.exists():
        return models.OperationResponse(error=models.Errors.DBError)

    if not os.access(file_path.parent, os.W_OK):
        return models.OperationResponse(error=models.Errors.DBError)

    fd = os.open(IP_FILE_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    if fd == -1:
        return models.OperationResponse(error=models.Errors.DBError)

    success = True
    for ip in ip_addresses:
        data = f"{ip.ip_address}\n".encode()
        bytes_written = os.write(fd, data)
        if bytes_written != len(data):
            success = False
            break

    os.close(fd)

    return models.OperationResponse(
        message="Export successful" if success else None,
        error=models.Errors.DBError if not success else None
    )




def import_ips() -> models.OperationResponse:
    if not os.path.exists(IP_FILE_PATH):
        return models.OperationResponse(error=models.Errors.Invalid)

    if not os.access(IP_FILE_PATH, os.R_OK):
        return models.OperationResponse(error=models.Errors.Invalid)

    with open(IP_FILE_PATH, 'rb') as file:
        content = file.read()

    if not content:
        return models.OperationResponse(error=models.Errors.Invalid)

    decoded = content.decode('utf-8', errors='replace')  # или 'ignore'

    ips = [line.strip() for line in decoded.splitlines() if line.strip()]

    success = True
    for ip in ips:
        req = models.IPAddressRequest(ip_address=ip)
        if req.is_valid() and not crud.select(ip):
            if not crud.create_ip_address(ip):
                success = False

    return models.OperationResponse(
        message="Import successful" if success else None,
        error=models.Errors.DBError if not success else None
    )


def upload_and_import(file: UploadFile) -> models.OperationResponse:
    content = file.file.read()
    if not content:
        return models.OperationResponse(error=models.Errors.Invalid)

    decoder = codecs.getincrementaldecoder('utf-8')(errors='replace')
    decoded = decoder.decode(content) + decoder.decode(b'', True)

    if not decoded:
        return models.OperationResponse(error=models.Errors.Invalid)

    ips = [line.strip() for line in decoded.splitlines() if line.strip()]

    success = True
    for ip in ips:
        req = models.IPAddressRequest(ip_address=ip)
        if req.is_valid() and not crud.select(ip):
            if not crud.create_ip_address(ip):
                success = False

    return models.OperationResponse(
        message="Upload successful" if success else None,
        error=models.Errors.DBError if not success else None
    )