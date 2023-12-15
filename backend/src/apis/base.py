from fastapi import APIRouter

from apis.routes import CDA_routes

api_router = APIRouter()

api_router.include_router(CDA_routes.router, prefix="/CDA", tags=["routes"])
