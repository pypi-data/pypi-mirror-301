"""
This is the module of pyblueprint
"""
from typing import Optional

import svgwrite
import svgwrite.text
import svgwrite.shapes


class Palette:
    def __init__(self):
        self.text_color = 'blue'


class BluePrint:
    def __init__(self):
        self.dwg = svgwrite.Drawing(size=(100, 100))
        self.palette = Palette()

    def background(self):
        self.dwg.add(svgwrite.shapes.Rect())

    def text(self, text: str, color: Optional[str] = None) -> None:
        if color is None:
            color = self.palette.text_color
        self.dwg.add(svgwrite.text.Text(text=text, color=color))

    def rectangle(self) -> None:
        self.dwg.add(svgwrite.shapes.Rect())

    def square(self) -> None:
        self.dwg.add(svgwrite.shapes.Rect())

    def save(self, filename: str) -> None:
        self.dwg.saveas(filename=filename)
