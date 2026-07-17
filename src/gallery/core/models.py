"""Domain models for the decision core."""

from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass(frozen=True)
class Request:
    """The input request for layout evaluation.

    Attributes:
        viewport_width: The client browser window width in pixels.
        photo_count: The total number of photos in the gallery.
    """
    viewport_width: int
    photo_count: int

    def __post_init__(self) -> None:
        """Validate request constraints."""
        if self.viewport_width <= 0:
            raise ValueError("viewport_width must be a positive integer greater than zero")
        if self.photo_count <= 0:
            raise ValueError("photo_count must be a positive integer greater than zero")


@dataclass(frozen=True)
class Decision:
    """The outcome of layout evaluation.

    Attributes:
        outcome: Target display layout ('RENDER_GRID' or 'RENDER_SINGLE_COLUMN').
        rule_ids: The sequence of rules that fired.
        evaluated_at: ISO 8601 UTC timestamp of evaluation.
    """
    outcome: str
    rule_ids: list[str]
    evaluated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
