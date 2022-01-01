from .base import Base


class FileEntry(Base):
    path: str
    filename: str
    extension: str


class TCEntry(FileEntry):
    tc: float
