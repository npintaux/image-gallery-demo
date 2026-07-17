"""Integration tests for LayoutEngine and general constraints."""

import pytest
from gallery.core.models import Request
from gallery.core.engine import LayoutEngine

def test_engine_evaluates_mobile_first():
    """Engine should evaluate R1 first and return RENDER_SINGLE_COLUMN for mobile widths."""
    engine = LayoutEngine()
    request = Request(viewport_width=500, photo_count=6)
    decision = engine.evaluate(request)

    assert decision.outcome == "RENDER_SINGLE_COLUMN"
    assert decision.rule_ids == ["R1"]
    assert decision.evaluated_at is not None

def test_engine_evaluates_desktop_catch_all():
    """Engine should evaluate R2 and return RENDER_GRID for desktop widths."""
    engine = LayoutEngine()
    request = Request(viewport_width=1024, photo_count=6)
    decision = engine.evaluate(request)

    assert decision.outcome == "RENDER_GRID"
    assert decision.rule_ids == ["R2"]
    assert decision.evaluated_at is not None

def test_invalid_request_raises_value_error():
    """Request construction should raise ValueError on violation of positive value constraints."""
    with pytest.raises(ValueError, match="viewport_width must be a positive integer"):
        Request(viewport_width=0, photo_count=6)

    with pytest.raises(ValueError, match="photo_count must be a positive integer"):
        Request(viewport_width=1024, photo_count=-1)

def test_engine_raises_error_if_no_rule_applies():
    """Engine should raise ValueError if no registered rules fire (catch-all fallback)."""
    engine = LayoutEngine()
    engine._rules = []  # pylint: disable=protected-access
    request = Request(viewport_width=1024, photo_count=6)
    with pytest.raises(ValueError, match="No rule fired for layout request"):
        engine.evaluate(request)
