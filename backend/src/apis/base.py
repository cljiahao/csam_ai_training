from fastapi import APIRouter

from apis.routes import CDA_routes
from apis.routes import CMT_routes


api_router = APIRouter()

api_router.include_router(CDA_routes.router, prefix="/CDA", tags=["routes"])
api_router.include_router(CMT_routes.router, prefix="/CMT/dataset", tags=["Train_Routes"])




