from .base import Base


class AuthInRequest(Base):
    user_id: int
    service_id: int
