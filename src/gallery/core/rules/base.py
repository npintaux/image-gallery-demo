"""Abstract base class for decision core rules."""

from abc import ABC, abstractmethod
from gallery.core.models import Request, Decision

class Rule(ABC):
    """Abstract base class representing a decision core rule."""

    @abstractmethod
    def evaluate(self, request: Request) -> Decision | None:
        """Evaluate the request against this rule's criteria.

        Args:
            request: The request containing client state.

        Returns:
            A Decision if this rule fires, otherwise None.
        """
