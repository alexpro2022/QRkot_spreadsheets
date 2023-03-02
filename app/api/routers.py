from fastapi import APIRouter

from app.api.endpoints import charity_project, donation, user
from app.google_package import router as google_router

main_router = APIRouter()


for router in (
    google_router,
    charity_project.router,
    donation.router,
    user.router,
):
    main_router.include_router(router)
