from fastapi import APIRouter

from apis.routes import misc
from apis.routes import CDA_folder_file
from apis.routes import CDA_process
from apis.routes import CDA_trackbar
from apis.routes import CMT_evaluation
from apis.routes import CMT_folder_file
from apis.routes import CMT_train
from apis.routes import CMT_zip_file
from apis.routes import Settings_save

api_router = APIRouter()

api_router.include_router(misc.router, tags=["misc"])

api_router.include_router(CDA_folder_file.router, prefix="/CDA", tags=["names"])
api_router.include_router(CDA_process.router, prefix="/CDA", tags=["process"])
api_router.include_router(CDA_trackbar.router, prefix="/CDA", tags=["routes"])

api_router.include_router(CMT_evaluation.router, prefix="/CMT", tags=["evaluate"])
api_router.include_router(CMT_folder_file.router, prefix="/CMT", tags=["names"])
api_router.include_router(CMT_train.router, prefix="/CMT", tags=["train"])
api_router.include_router(CMT_zip_file.router, prefix="/CMT", tags=["zip"])

api_router.include_router(Settings_save.router, prefix="/Settings", tags=["settings"])
