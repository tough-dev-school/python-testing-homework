from datetime import datetime
from typing import Optional, TypedDict


class UserDict(TypedDict):
    """User factory data output."""

    email: str

    first_name: str
    last_name: str
    date_of_birth: datetime
    address: str
    job_title: str

    phone: str

    lead_id: Optional[int]

    # Security:
    is_staff: bool
    is_active: bool

    password: str

    password1: Optional[str]
    password2: Optional[str]
