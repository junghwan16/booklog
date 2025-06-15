from abc import ABC, abstractmethod
from typing import BinaryIO


class FileStoragePort(ABC):
    @abstractmethod
    def save(self, file: BinaryIO, *, content_type: str) -> str: ...
    @abstractmethod
    def generate_public_url(self, file_id: str) -> str: ...
