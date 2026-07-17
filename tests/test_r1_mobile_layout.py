"""Unit tests for MobileLayoutRule (R1)."""

from gallery.core.models import Request
from gallery.core.rules.r1_mobile_layout import MobileLayoutRule

def test_mobile_layout_fires_on_small_viewport():
    """Rule R1 should fire and return RENDER_SINGLE_COLUMN on small viewports."""
    rule = MobileLayoutRule()
    request = Request(viewport_width=375, photo_count=6)
    decision = rule.evaluate(request)

    assert decision is not None
    assert decision.outcome == "RENDER_SINGLE_COLUMN"
    assert decision.rule_ids == ["R1"]

def test_mobile_layout_ignores_large_viewport():
    """Rule R1 should return None for viewports 768px or wider."""
    rule = MobileLayoutRule()
    request = Request(viewport_width=768, photo_count=6)
    assert rule.evaluate(request) is None
