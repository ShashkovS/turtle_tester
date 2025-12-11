# Turtle Tester

Turtle Tester is a drop-in replacement for the Python `turtle` module that prints every drawn segment instead of opening a GUI window. The goal is to let automated checkers (for example, ejudge) compare turtle drawings programmatically. A reference checker (`check_turtle_en.py`) is provided to compare student output against the expected drawing.

## Installation

- `pip install git+https://github.com/ShashkovS/turtle_tester.git`

## Quick start

```python
import turtle_tester as turtle

T = turtle.Turtle()
T.pendown()
T.forward(50)
T.left(90)
T.forward(50)
T.left(90)
T.forward(50)
T.left(90)
T.forward(50)
T.penup()
T.forward(100)
T.hideturtle()
turtle.mainloop()
```

This produces text output describing each drawn segment:

```
(  +0.00,   +0.00) -> ( +50.00,   +0.00)
( +50.00,   +0.00) -> ( +50.00,  +50.00)
( +50.00,  +50.00) -> (  +0.00,  +50.00)
(  +0.00,  +50.00) -> (  -0.00,   +0.00)
```

## How the checker works

- Both the reference solution and the submitted program emit a list of segments in the `(<from>) -> (<to>)` format. Any extra output causes immediate failure.
- `check_turtle_en.py` normalizes the segment lists: it ensures the smallest segment has length 1, orients segments consistently, merges overlapping collinear segments, moves the center of mass to the origin, and scales so the furthest point is at distance 1000.
- A set of candidate rotation angles is derived from points lying on the same radius; each candidate is tested to see if the normalized segment sets match within absolute tolerance.
- Similarity transformations (shift, rotation, homothety) are allowed by default so drawings that are geometrically identical pass even if they are offset, rotated, or scaled.

## Environment toggles

- `DISABLE_SHIFT`: require the drawing to be in the same position as the reference (no translation allowed).
- `DISABLE_ROTATION`: require identical orientation (no rotation allowed).
- `DISABLE_HOMOTHETY`: require the same size (no scaling allowed).
- `EPS`: precision used by `turtle_tester` when formatting coordinates; defaults to `1e-8` (set it higher to reduce output precision).

Example:

```bash
export DISABLE_ROTATION=1
export DISABLE_HOMOTHETY=1
python3 check_turtle_en.py test.txt student.out correct.out
```

Use `check_turtle_en.py` in your judge configuration as the checker, and import `turtle_tester` instead of `turtle` in solutions so their drawings can be compared.
