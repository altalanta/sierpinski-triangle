# Sierpinski Triangle (SVG)

Generate a crisp, resolution‑independent Sierpinski triangle as an SVG using pure Python (no external dependencies).

## Quick Start

- Requires Python 3.8+
- Run:

```
python3 sierpinski.py --depth 6 --size 800 --output sierpinski.svg
```

Then open `sierpinski.svg` in any browser or image viewer.

## Options

- `--depth`  Recursion depth (default: 6). Higher = more detail.
- `--size`   Triangle width in pixels (default: 800). Height is computed.
- `--color`  Fill color for the triangle (default: `#1a1a1a`).
- `--bg`     Background color (default: `white`).
- `--output` Output SVG path (default: `sierpinski.svg`).

Examples:

```
# High detail, dark background
python3 sierpinski.py --depth 8 --size 1000 --color #222 --bg #fefefe --output out.svg

# Smaller, lighter triangle on transparent background
python3 sierpinski.py --depth 5 --size 600 --color #555 --bg transparent --output small.svg
```

## How It Works

The script draws a solid outer triangle, then recursively “carves out” the central inverted triangle at each level by layering white (or the chosen background color) triangles on top. The output is a single, compact SVG file.

## Repo Structure

- `sierpinski.py` — CLI script to generate the SVG
- `README.md` — usage and examples
- `.gitignore` — common Python ignores

## Notes

- SVG is vector; you can scale without loss.
- Very high depths produce many polygons and large files; start with `--depth 5..7`.
