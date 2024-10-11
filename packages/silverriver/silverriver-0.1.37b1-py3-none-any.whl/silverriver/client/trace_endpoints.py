from typing import Any

import pydantic
from pydantic import field_validator

from silverriver.client.endpoint import Endpoint

MAX_FILE_SIZE = 1024 ** 2 * 50  # 50mb


class TraceResponseModel(pydantic.BaseModel):
    success: bool


class TraceRequestModel(pydantic.BaseModel):
    filename: str
    content: bytes

    @field_validator("content")
    @classmethod
    def check_content_size(cls, content: bytes) -> Any:
        check_content_size(content)
        return content

    def model_dump(self, **kwargs) -> dict[str, Any]:
        return {"trace": (self.filename, self.content)}


def check_content_size(file: bytes) -> None:
    if len(file) > MAX_FILE_SIZE:
        max_size_mb = MAX_FILE_SIZE // (1024 ** 2)
        raise ValueError(f"Content is too large, must be less than {max_size_mb} MB")


class TraceEndpoints:
    PREFIX = "/api/v1/trace"
    UPLOAD = Endpoint(prefix=PREFIX, path="/upload", method="POST", response_model=TraceResponseModel,
                      request_model=TraceRequestModel)
