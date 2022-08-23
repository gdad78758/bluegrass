import sys

from fpdf import FPDF
from fpdf.drawing import (Line, Point, Rectangle, Ellipse, PaintedPath)

pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=24)
pdf.text(x=60, y=140, txt="Some text.")
pdf.text_annotation(
    x=100,
    y=130,
    text="This is a text annotation.",
)

c = Point(5,5)
r = Point(9,9)
e = Ellipse(c,r)
e = PaintedPath(100,20)
# e.ellipse(20,20,10,15)
g = Line(Point(200,200))
e.line_to(100,120).move_to(105,120).line_to(105,100)
e.add_path_element(g)

r = Rectangle(Point(150,100),Point(40,50))
e.add_path_element(r)

pdf.set_draw_color(1,1,1)
pdf.set_fill_color(1,1,250)
pdf.draw_path(e)
pdf.set_fill_color(250,0,0)
pdf.set_draw_color(250,0,0)
pdf.ellipse(50,50,15,5,'F')
pdf.output("text_annotation.pdf")
