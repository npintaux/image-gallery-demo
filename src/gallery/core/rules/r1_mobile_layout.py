"""Rule R1: Mobile Layout Rule."""

from gallery.core.models import Request, Decision
from gallery.core.rules.base import Rule

class MobileLayoutRule(Rule):
    """Rule that collapses grid to a single column on viewports smaller than 768px."""

    def evaluate(self, request: Request) -> Decision | None:
        """Evaluate viewport width for mobile layout.

        Args:
            request: The request containing viewport characteristics.

        Returns:
            A Decision with RENDER_SINGLE_COLUMN if mobile, otherwise None.
        """
        if request.viewport_width < 768:
            return Decision(outcome="RENDER_SINGLE_COLUMN", rule_ids=["R1"])
        return None
