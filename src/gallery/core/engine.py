"""Layout decision engine."""

from gallery.core.models import Request, Decision
from gallery.core.rules.r1_mobile_layout import MobileLayoutRule
from gallery.core.rules.r2_desktop_layout import DesktopLayoutRule

class LayoutEngine:
    """The layout decision engine that evaluates rules in precedence order."""

    def __init__(self) -> None:
        """Initialize and register decision rules in precedence order."""
        self._rules = [
            MobileLayoutRule(),
            DesktopLayoutRule(),
        ]

    def evaluate(self, request: Request) -> Decision:
        """Evaluate a layout request against registered rules.

        Args:
            request: The layout request to evaluate.

        Returns:
            The Decision from the first matching rule.

        Raises:
            ValueError: If no rule fires (violates catch-all constraint).
        """
        for rule in self._rules:
            decision = rule.evaluate(request)
            if decision is not None:
                return decision
        raise ValueError("Evaluation failed: No rule fired for layout request.")
