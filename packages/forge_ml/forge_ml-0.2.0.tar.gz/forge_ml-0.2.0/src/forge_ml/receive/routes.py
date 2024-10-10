from typing import Annotated

from litestar import MediaType, get, post
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.params import Body


@post("/receive/config")
async def post_config(config: dict) -> None:
    pass


@post("/receive/model", media_type=MediaType.MESSAGEPACK)
async def post_model(
    data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)],
) -> str:
    file_contents = await data.read()
    filename = data.filename
    return f"Received file {filename} with {len(file_contents)} bytes"
