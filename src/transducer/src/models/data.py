from .base import Base
import datetime


class Transducer(Base):
    transducer_id: int
    created_at: datetime.datetime
    status: int
    cause: int
    mode: int
    frequency: int
    pe: int
    ps: int
    minutes: int
    vah: int
    temperature: int
