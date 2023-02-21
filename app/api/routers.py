from fastapi import APIRouter

from app.api.endpoints import (
    google,
    charity_project,
    donation,
    user,
)

main_router = APIRouter()


for router in (
    google.router,
    charity_project.router,
    donation.router,
    user.router,
):
    main_router.include_router(router)
