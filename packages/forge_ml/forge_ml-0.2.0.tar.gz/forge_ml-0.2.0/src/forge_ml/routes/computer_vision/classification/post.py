from litestar import Router, post
from pydantic import BaseModel


class CVClassification(BaseModel):
    project_id: str
    project_name: str
    project_type: str


@post("/statistics")
async def statistics(data: CVClassification) -> dict:
    return {
        "project_id": data.project_id,
        "project_name": data.project_name,
        "project_type": data.project_type,
    }


cv_post_router = Router(
    path="/api/v1/computer_vision/classification", route_handlers=[statistics]
)
