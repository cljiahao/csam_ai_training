from fastapi import APIRouter

from apis.v2.constants.common import APITags
from apis.v2.routers import csam_image, data_summary, deep_learning, image_settings

router = APIRouter()


@router.get(
    "/health",
    tags=["health"],
    summary="Health Check",
    description="A simple health check returning a OK status.",
)
def v2_health():
    return {"status": "OK"}


def include_tagged_router(sub_router, tag: APITags) -> None:
    """Includes a sub-router with a tag and a prefix derived from the tag's value."""
    router.include_router(sub_router, tags=[tag], prefix=f"/{tag.value}")


include_tagged_router(csam_image.router, APITags.CSAM_IMAGE)
include_tagged_router(data_summary.router, APITags.DATA_SUMMARY)
include_tagged_router(deep_learning.router, APITags.DEEP_LEARNING)
include_tagged_router(image_settings.router, APITags.IMAGE_SETTINGS)
