# Specification

> **Source of truth.** GitHub Issues are intake; this file is the contract the
> agent obeys. When the two disagree, this file (and its owners) decide.

## Overview

Given a gallery layout `Request` (comprising viewport characteristics and asset count), the engine returns a `Decision` indicating the target display layout (`outcome` plus the list of `rule_ids` that fired), evaluating rules in precedence order.

## Domain model

- **Request** — the input. Fields:
  - `viewport_width: int` — client browser window width in pixels.
  - `photo_count: int` — total number of photos in the gallery.
- **Decision** — the output. Fields:
  - `outcome: str` — one of `RENDER_GRID` (multi-column responsive layout) or `RENDER_SINGLE_COLUMN` (mobile-friendly stack).
  - `rule_ids: list[str]` — the rules that determined the outcome.
  - `evaluated_at: str` — ISO 8601 timestamp.

## Global constraints

- Viewport width must be a positive integer greater than zero (`viewport_width > 0`).
- Photo count must be a positive integer greater than zero (`photo_count > 0`).
- Evaluation is deterministic: same `Request` → same `Decision`.
- Every `Request` yields exactly one outcome; the last rule is a catch-all.

## Rules

### R1: Mobile Layout Rule

- **Behavior:** When the client browser's viewport width is less than 768 pixels, the grid collapses to a single-column display layout.
- **Example:** `evaluate(viewport_width=375, photo_count=6)` → `RENDER_SINGLE_COLUMN`, `["R1"]`
- **Precedence:** Highest priority. Overrides default grid rendering on small viewports.
- **Source:** issue #1

### R2: Desktop Layout Rule (Catch-All)

- **Behavior:** When the viewport width is 768 pixels or greater, a responsive multi-column CSS grid is displayed.
- **Example:** `evaluate(viewport_width=1200, photo_count=6)` → `RENDER_GRID`, `["R2"]`
- **Precedence:** Lower priority. Acts as the catch-all baseline layout for all larger viewports.
- **Source:** issue #1

## Precedence order

Rules are evaluated as an **ordered list**; earlier entries win on conflict.

1. R1 — Mobile Layout Rule
2. R2 — Desktop Layout Rule (Catch-All)

## Glossary

- **Grid** — A responsive CSS multi-column display structure containing photo cards.
- **Single-column layout** — A vertical stack layout tailored for smaller mobile screens.
- **Viewport width** — The horizontal width of the active browser window.
