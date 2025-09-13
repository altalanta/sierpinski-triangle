import math
import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox

from pathlib import Path

try:
    from sierpinski import generate_svg
except Exception:
    generate_svg = None  # Fallback if script is run from elsewhere


def midpoint(a, b):
    return (0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1]))


def draw_sierpinski(canvas: tk.Canvas, tri, depth: int, fill: str):
    if depth <= 0:
        canvas.create_polygon([tri[0][0], tri[0][1], tri[1][0], tri[1][1], tri[2][0], tri[2][1]], fill=fill, outline="")
        return
    a, b, c = tri
    m_ab = midpoint(a, b)
    m_bc = midpoint(b, c)
    m_ca = midpoint(c, a)
    draw_sierpinski(canvas, (a, m_ab, m_ca), depth - 1, fill)
    draw_sierpinski(canvas, (m_ab, b, m_bc), depth - 1, fill)
    draw_sierpinski(canvas, (m_ca, m_bc, c), depth - 1, fill)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sierpinski Triangle")
        self.minsize(640, 480)

        self.depth = tk.IntVar(value=6)
        self.size = tk.IntVar(value=800)
        self.tri_color = tk.StringVar(value="#1a1a1a")
        self.bg_color = tk.StringVar(value="#ffffff")
        self.transparent = tk.BooleanVar(value=False)

        self._build_ui()
        self._bind_events()
        self.render()

    def _build_ui(self):
        top = ttk.Frame(self, padding=8)
        top.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Controls
        controls = ttk.Frame(top)
        controls.grid(row=0, column=0, sticky="ew")
        controls.columnconfigure(10, weight=1)

        ttk.Label(controls, text="Depth").grid(row=0, column=0, padx=(0, 6))
        depth_scale = ttk.Scale(controls, from_=0, to=9, orient=tk.HORIZONTAL, variable=self.depth)
        depth_scale.grid(row=0, column=1, sticky="ew", padx=(0, 12))

        ttk.Label(controls, text="Width").grid(row=0, column=2, padx=(0, 6))
        size_scale = ttk.Scale(controls, from_=200, to=1200, orient=tk.HORIZONTAL, variable=self.size)
        size_scale.grid(row=0, column=3, sticky="ew", padx=(0, 12))

        self.color_btn = ttk.Button(controls, text="Triangle Color", command=self.pick_tri_color)
        self.color_btn.grid(row=0, column=4, padx=(0, 6))

        self.bg_btn = ttk.Button(controls, text="Background", command=self.pick_bg_color)
        self.bg_btn.grid(row=0, column=5, padx=(0, 6))

        self.transparent_chk = ttk.Checkbutton(controls, text="Transparent BG", variable=self.transparent, command=self.render)
        self.transparent_chk.grid(row=0, column=6, padx=(0, 12))

        self.save_btn = ttk.Button(controls, text="Save SVG…", command=self.save_svg)
        self.save_btn.grid(row=0, column=7)

        # Canvas
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def _bind_events(self):
        self.depth.trace_add("write", lambda *_: self.render())
        self.size.trace_add("write", lambda *_: self.render())

    def pick_tri_color(self):
        color = colorchooser.askcolor(initialcolor=self.tri_color.get(), title="Choose triangle color")[1]
        if color:
            self.tri_color.set(color)
            self.render()

    def pick_bg_color(self):
        color = colorchooser.askcolor(initialcolor=self.bg_color.get(), title="Choose background color")[1]
        if color:
            self.bg_color.set(color)
            self.render()

    def _compute_geometry(self):
        width = max(200, int(self.size.get()))
        height = int(math.sqrt(3.0) * 0.5 * width)
        margin = max(8, int(0.02 * width))
        inner_w = width - 2 * margin
        inner_h = math.sqrt(3.0) * 0.5 * inner_w
        a = (margin, margin + inner_h)
        b = (margin + inner_w, margin + inner_h)
        c = (margin + 0.5 * inner_w, margin)
        return width, int(inner_h + 2 * margin), (a, b, c)

    def render(self):
        width, height, tri = self._compute_geometry()
        bg = "white" if self.transparent.get() else self.bg_color.get()

        self.canvas.configure(width=width, height=height, bg=bg)
        self.canvas.delete("all")
        draw_sierpinski(self.canvas, tri, int(self.depth.get()), self.tri_color.get())

    def save_svg(self):
        if generate_svg is None:
            messagebox.showerror("Unavailable", "SVG generator not found. Place gui.py next to sierpinski.py and run from that folder.")
            return
        width, _, _ = self._compute_geometry()
        depth = int(self.depth.get())
        color = self.tri_color.get()
        bg = "transparent" if self.transparent.get() else self.bg_color.get()
        svg = generate_svg(size=width, depth=depth, color=color, bg=bg)
        path = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=[("SVG", ".svg")], initialfile="sierpinski.svg")
        if not path:
            return
        try:
            Path(path).write_text(svg, encoding="utf-8")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save SVG: {e}")
        else:
            messagebox.showinfo("Saved", f"Saved: {path}")


if __name__ == "__main__":
    App().mainloop()

