from dataclasses import dataclass
from pprint import pprint
from typing import Annotated

from litestar import Router, post
from litestar.params import Body


@dataclass
class ModelConfig:
    model_config: dict


@post("/upload_config")
async def config_handler(
    data: Annotated[
        ModelConfig,
        Body(
            title="Receive Model Config",
            description="Route handler for uploading a model configuration file.",
        ),
    ],
) -> None:
    """
    Model configuration upload data.

    Args:
        data: Payload

    Returns:
        None
    """
    pprint(data)


@post("/upload_msgpack")
async def msgpack_handler(
    data: Annotated[
        ModelConfig,
        Body(
            title="Receive Msgpack Model",
            description="Route handler for uploading a model in the msgpack format.",
        ),
    ],
) -> None:
    print(data)


model_upload_router = Router(
    path="/api/v1/model_curation/", route_handlers=[config_handler, msgpack_handler]
)
