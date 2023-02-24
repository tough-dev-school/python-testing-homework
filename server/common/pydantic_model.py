import pydantic


class BaseModel(pydantic.BaseModel):
    """Base immutable model for our internal use."""

    class Config(object):
        allow_mutation = False
