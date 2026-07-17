"""Rule R2: Desktop Layout Rule (Catch-All)."""

from gallery.core.models import Request, Decision
from gallery.core.rules.base import Rule

class DesktopLayoutRule(Rule):
    """Catch-all rule that returns RENDER_GRID for viewports 768px or wider."""

    def evaluate(self, request: Request) -> Decision | None:
        """Evaluate viewport width for desktop grid layout.

        Args:
            request: The request containing viewport characteristics.

        Returns:
            A Decision with RENDER_GRID if desktop, otherwise None.
        """
        if request.viewport_width >= 768:
            return Decision(outcome="RENDER_GRID", rule_ids=["R2"])
        return None
