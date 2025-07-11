from .start import router as start_router
from .admin import router as admin_router
from .moderation import router as mod_router
from .user import router as user_router

def register_all_handlers(dp):
    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.include_router(mod_router)
    dp.include_router(user_router)
