import pydantic

from silverriver.client.endpoint import Endpoint


class TraceResponseModel(pydantic.BaseModel):
    success: bool


class TraceRequestModel(pydantic.BaseModel):
    trace: tuple[str, bytes]  # filename, content


class TraceEndpoints:
    PREFIX = "/api/v1/trace"
    UPLOAD = Endpoint(prefix=PREFIX, path="/upload", method="POST", response_model=TraceResponseModel,
                      request_model=TraceRequestModel)
