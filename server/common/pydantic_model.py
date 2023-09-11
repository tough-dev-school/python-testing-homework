import pydantic


class BaseModel(pydantic.BaseModel):
    """Base immutable model for our internal use."""

    model_config = pydantic.ConfigDict(frozen=True)
