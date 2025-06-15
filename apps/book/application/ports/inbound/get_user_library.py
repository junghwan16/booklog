from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from apps.book.domain.entities import UserBook


@dataclass(frozen=True, slots=True)
class GetUserLibraryQuery:
    """Query to get user's library."""
    
    user_id: str


class GetUserLibraryUseCase(ABC):
    """Interface for getting user's library."""
    
    @abstractmethod
    def execute(self, query: GetUserLibraryQuery) -> List[UserBook]:
        """Execute get user library use case."""
        ... 