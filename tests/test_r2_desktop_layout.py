"""Unit tests for DesktopLayoutRule (R2)."""

from gallery.core.models import Request
from gallery.core.rules.r2_desktop_layout import DesktopLayoutRule

def test_desktop_layout_fires_on_large_viewport():
    """Rule R2 should fire and return RENDER_GRID on viewports 768px or wider."""
    rule = DesktopLayoutRule()
    request = Request(viewport_width=768, photo_count=6)
    decision = rule.evaluate(request)

    assert decision is not None
    assert decision.outcome == "RENDER_GRID"
    assert decision.rule_ids == ["R2"]

def test_desktop_layout_ignores_small_viewport():
    """Rule R2 should return None for viewports smaller than 768px."""
    rule = DesktopLayoutRule()
    request = Request(viewport_width=767, photo_count=6)
    assert rule.evaluate(request) is None
