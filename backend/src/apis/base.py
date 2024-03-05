from fastapi import APIRouter

from apis.routes import CDA_random
from apis.routes import CDA_trackbar
from apis.routes import CDA_process
from apis.routes import CDA_count
from apis.routes import CMT_train
from apis.routes import CMT_folder_file
from apis.routes import CMT_evaluation

api_router = APIRouter()

api_router.include_router(CDA_random.router, prefix="/CDA", tags=["random"])
api_router.include_router(CDA_trackbar.router, prefix="/CDA", tags=["routes"])
api_router.include_router(CDA_process.router, prefix="/CDA", tags=["process"])
api_router.include_router(CDA_count.router, prefix="/CDA", tags=["count"])

api_router.include_router(CMT_train.router, prefix="/CMT", tags=["train"])
api_router.include_router(CMT_folder_file.router, prefix="/CMT", tags=["names"])
api_router.include_router(CMT_evaluation.router, prefix="/CMT", tags=["evaluate"])
