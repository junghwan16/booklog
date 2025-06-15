from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(slots=True)
class UpdateProfileCommand:
    user_id: int
    nickname: str | None = None
    avatar_file_id: str | None = None  # 파일 스토리지 키


class UpdateProfileUseCase(ABC):
    @abstractmethod
    def execute(self, cmd: UpdateProfileCommand) -> None: ...
