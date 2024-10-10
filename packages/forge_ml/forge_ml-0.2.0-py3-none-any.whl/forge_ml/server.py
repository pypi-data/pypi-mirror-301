r"""This module defines the middleware server that collects episode information
and sends it to the frontend for rendering.
"""

import datetime
import os
import sys
import yaml
from pathlib import Path
from litestar.openapi import OpenAPIConfig

import numpy as np
import requests
import uvicorn
from dotenv import load_dotenv
from litestar import Litestar, Router, get, post
from loguru import logger
from pydantic import BaseModel

from mithril_python_server.routes.model_curation.upload import model_upload_router
# from supabase import Client, create_client

env_path = Path(".staging.env")

load_dotenv(dotenv_path=env_path)


TIMEOUT = 100

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
# supabase: Client = create_client(url, key)


# @post("/api/v1/project/create")
# async def create_project(project_id: str) -> None:
#     data = await project_id.json()
#     logger.info(f"Creating project: {data}")


# @post("/api/v1/project/read")
# async def read_project(project_id: str) -> None:
#     data = await project_id.json()
#     logger.info(f"Read project: {data}")


# @post("/api/v1/project/update")
# async def update_project(project_id: str) -> None:
#     data = await project_id.json()

#     table = supabase.table("projects")

#     n_projects = table.select("*").execute()
#     n_projects = len(n_projects.data)

#     if "project_name" in data.keys():
#         project_name = data["project_name"]
#     else:
#         logger.error(f"Project name is missing")
#         sys.exit(1)

#     if "project_type" in data.keys():
#         project_type = data["project_type"]
#     else:
#         logger.error(f"Project type is missing")
#         sys.exit(1)

#     logger.info(f"Project name: {project_name}")
#     logger.info(f"Project type: {project_type}")

#     _ = table.insert(
#         {
#             "id": n_projects + 1,
#             "project_name": project_name,
#             "project_type": project_type,
#         }
#     ).execute()

#     logger.info(f"Update project: {data}")


# @post("/api/v1/project/delete")
# async def delete_project(project_id: str) -> None:
#     data = await project_id.json()
#     logger.info(f"Delete project: {data}")


app = Litestar(route_handlers=[model_upload_router], openapi_config=OpenAPIConfig(title="Server API", version="1.0.0"))

if __name__ == "__main__":
    schema_dict = app.openapi_schema.to_schema()
    schema_yaml_str = yaml.dump(schema_dict, sort_keys=False)
    with open('docs/source/server-api.yaml', 'w') as file:
        file.write(schema_yaml_str)
    logger.info("OpenAPI YAML schema saved to openapi.yaml")
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)