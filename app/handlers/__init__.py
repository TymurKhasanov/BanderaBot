from .bind import router as bind_router
from .prime import router as prime_router
from .announcement import router as announcement_router
from .admin_menu import router as admin_menu_router
from .start import router as start_router
from .help import router as help_router
from .menu import router as menu_router
from .settings import router as settings_router
from .admin_buttons import router as admin_buttons_router
from .admin_input import router as admin_input_router
from .dcp import router as dcp_router

routers = [
    start_router,
    help_router,
    menu_router,
    settings_router,

    bind_router,
    prime_router,
    announcement_router,
    dcp_router,

    admin_menu_router,
    admin_buttons_router,
    admin_input_router,
]