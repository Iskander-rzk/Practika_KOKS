import enum
import ipaddress
from pydantic import BaseModel
from typing import List, Optional

class IPAddressDB(BaseModel):
    id: Optional[int] = None
    ip_address: str


class IPAddressRequest(BaseModel):
    ip_address: str

    def is_valid(self) -> bool:
        try:
            # Remove port if exists
            if ']:' in self.ip_address:
                ip_part = self.ip_address.split(']:', 1)[0] + ']'
                ipaddress.ip_address(ip_part[1:])
            elif ':' in self.ip_address:
                ip_part = self.ip_address.rsplit(':', 1)[0]
                ipaddress.ip_address(ip_part)
            else:
                ipaddress.ip_address(self.ip_address)
            return True
        except ValueError:
            return False

class Errors(enum.Enum):
    Invalid = 1
    Exist = 2
    DBError = 3

class IPAddressResponse(BaseModel):
    error: Optional[Errors] = None
    ip_addresses: List[IPAddressDB] = []