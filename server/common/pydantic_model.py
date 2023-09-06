import pydantic


class BaseModel(pydantic.BaseModel):
    """Base immutable model for our internal use."""

    class Config(object):
        frozen = True
