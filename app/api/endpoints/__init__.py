from .v1 import router as v1_router
from .service import router as service_router
from .main import router as main_router


__all__ = [
    'v1_router',
    'service_router',
    'main_router'
]