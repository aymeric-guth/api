from pathlib import PurePath

from .base import Base


class FileEntry(Base):
    path: str
    filename: str
    extension: str

    def __str__(self) -> str:
        return f'{self.path}{self.filename}{self.extension}'


class TCEntry(FileEntry):
    tc: float
