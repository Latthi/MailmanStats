import canvas
import line_style
import color
import pychart_util
import chart_object
import object_set
import types
import math
import arrow_doc

from scaling import *

__doc__ = """
Arrow is an optional component of a chart that draws line segments with
an arrowhead. To draw an arrow, one creates an arrow.T object, and calls
its "draw" method usually after area.draw() is called (otherwise, area.draw()
may overwrite the arrow). For example, the below code draws an arrow
from (10,10) to (20,30).

ar = area.T(...)
a = arrow.T(head_style = 1)
ar.draw()
a.draw([(10,10), (20,30)])
"""

def draw_arrowhead(tailx, taily, tipx, tipy, thickness, head_len, style):
    out = canvas.out
    out.comment("ARROWHEAD tail=(%d,%d) tip=(%d,%d)\n" 
	        % (tailx, taily, tipx, tipy))
    
    halfthickness = thickness/2.0
    dx = tipx - tailx
    dy = tipy - taily
    arrow_len = math.sqrt(dx*dx + dy*dy)
    angle = math.atan2(dy, dx) * 360 / (2*math.pi)
    base = arrow_len - head_len
    out.push_transformation((tailx, taily), None, angle)    

    if style == 0:
        out.moveto(base, - halfthickness)
        out.lineto(base, halfthickness)
        out.lineto(arrow_len, 0)
        out.closepath()
    elif style == 1:
        depth = head_len / 2.5
        out.moveto(base - depth, -halfthickness)
        out.lineto(base, 0)
        out.lineto(base - depth, halfthickness)
        out.lineto(arrow_len, 0)
        out.closepath()
    elif style == 2:
        out.moveto(base + head_len/2.0, 0)
        out.path_arc(base + head_len / 2.0, 0, head_len / 2.0, 1.0, 0, 400)
    elif style == 3:
        out.moveto(base, 0)
        out.lineto(base + head_len/2.0, -halfthickness)
        out.lineto(arrow_len, 0)
        out.lineto(base + head_len/2.0, halfthickness)
        out.closepath()
    else:
        raise Exception, "Arrow style must be a number between 0 and 3."
    out.fill()
    out.pop_transformation()
    out.comment("end ARROWHEAD.\n")

def draw_arrowbody(tailx, taily, tipx, tipy, head_len):
    out = canvas.out
    dx = tipx - tailx
    dy = tipy - taily
    arrow_len = math.sqrt(dx*dx + dy*dy)
    angle = math.atan2(dy, dx) * 360 / (2*math.pi)
    base = arrow_len - head_len
    out.push_transformation((tailx, taily), None, angle)
    out.moveto(0, 0)
    out.lineto(base+head_len*0.1, 0)
    out.stroke()
    out.pop_transformation()


class T(chart_object.T):
    __doc__ = arrow_doc.doc
    keys = {
        "thickness" : (pychart_util.NumType, 0, 4,
                        "The width of the arrow head."),
        "head_len": (pychart_util.NumType, 0, 8,
                    "The length of the arrow head."),
        "head_color": (color.T, 0, color.default,
                      "The color of the arrow head."),
        "line_style": (line_style.T, 1, line_style.default,
                       "Line style."),
        "head_style": (types.IntType, 1, 1,
                       "The value of 0 draws a triangular arrow head. 1 draws a swallow-tail arrow head")
            }
##AUTOMATICALLY GENERATED

##END AUTOMATICALLY GENERATED
    def draw(self, points):
        """Points: The list of points the arrow traverses.
        It should contain at least two points, ie
        the tail and tip."""
        self.type_check()
        xtip = points[-1][0]
        ytip = points[-1][1]
        
        xtail = points[-2][0]
        ytail = points[-2][1]

        canvas.out.newpath()
        canvas.out.set_line_style(self.line_style)
        if len(points) > 2:
            canvas.out.moveto(points[0][0], points[0][1])
            for i in range(1, len(points)-1):
                canvas.out.lineto(points[i][0], points[i][1])

        draw_arrowbody(xscale(xtail), yscale(ytail),
                       yscale(xtip), yscale(ytip),
                       nscale(self.head_len))

        canvas.out.set_fill_color(self.head_color)
        draw_arrowhead(xscale(xtail), yscale(ytail),
                       xscale(xtip), yscale(ytip),
                       nscale(self.thickness),
                       nscale(self.head_len),
                       self.head_style)
        
        canvas.setbb(xtail, ytail)
        canvas.setbb(xtip, ytip)

standards = object_set.T()
def __intern(a):
    global standards
    standards.add(a)
    return a

a0 = __intern(T(head_style=0))
a1 = __intern(T(head_style=1))
a2 = __intern(T(head_style=2))
a3 = __intern(T(head_style=3))
gray0 = __intern(T(head_style=0, head_color = color.gray50,
                   line_style=line_style.T(color=color.gray50)))
gray1 = __intern(T(head_style=1, head_color = color.gray50,
                   line_style=line_style.T(color=color.gray50)))
gray2 = __intern(T(head_style=2, head_color = color.gray50,
                   line_style=line_style.T(color=color.gray50)))
gray3 = __intern(T(head_style=3, head_color = color.gray50,
                   line_style=line_style.T(color=color.gray50)))

fat0 = __intern(T(head_style=0, head_len=12, thickness=10, line_style=line_style.T(width=2)))
fat1 = __intern(T(head_style=1, head_len=12, thickness=10, line_style=line_style.T(width=2)))
fat2 = __intern(T(head_style=2, head_len=12, thickness=10, line_style=line_style.T(width=2)))
fat3 = __intern(T(head_style=3, head_len=12, thickness=10, line_style=line_style.T(width=2)))
fatgray0 = __intern(T(head_style=0, head_len=12, thickness=10,
                      head_color = color.gray50,
                      line_style=line_style.T(width=2, color=color.gray50)))
fatgray1 = __intern(T(head_style=1, head_len=12, thickness=10,
                      head_color = color.gray50,
                      line_style=line_style.T(width=2, color=color.gray50)))
fatgray2 = __intern(T(head_style=2, head_len=12, thickness=10,
                      head_color = color.gray50,
                      line_style=line_style.T(width=2, color=color.gray50)))
fatgray3 = __intern(T(head_style=3, head_len=12, thickness=10,
                      head_color = color.gray50,
                      line_style=line_style.T(width=2, color=color.gray50)))

default = a1


