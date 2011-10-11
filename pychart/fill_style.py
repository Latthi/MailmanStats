import pychart_util
import color
import line_style
import chart_object
import object_set
import types
import canvas
import theme
import fill_style_doc

from scaling import *

_keys = {
    "bgcolor" : (color.T, 1, color.white, "The background color."),
    "line_style": (line_style.T, 1, line_style.default,
                   pychart_util.line_desc),
    "line_interval": (pychart_util.NumType, 0, 3,
                      "The interval between successive stitch lines.")
    }

class T(chart_object.T):
    __doc__ = fill_style_doc.doc
    keys = _keys
##AUTOMATICALLY GENERATED
##END AUTOMATICALLY GENERATED
    def __str__(self):
        s = name_table().lookup(self)
        if s:
            return s
        return "<fillstyle: bg=%s line=%s interval=%s>" % \
               (self.bgcolor, self.line_style, self.line_interval)

class Plain(T):
    """This class just fills the region with the solid background color.
Attributes line_style and line_interval are ignored."""
    def draw(self, x1, y1, x2, y2):
        pass
    
class Diag(T):
    "This class fills the region with diagonal lines."

    def draw(self, x1, y1, x2, y2):
        line_width = self.line_style.width
        interval = self.line_interval * 1.414
        x1 = x1 - line_width
        y1 = y1 - line_width
        x2 = x2 + line_width
        y2 = y2 + line_width
        height = y2 - y1
        width = x2 - x2
        len = max(height, width)
        curx = x1 - len
        while curx < x2:
            canvas.line(self.line_style, curx, y1, curx+len, y1+len)
            curx = curx + interval

class Rdiag(T):
    """Fills the region with diagonal lines, but tilted in the opposite
direction from fill_style.Diag."""
    def draw(self, x1, y1, x2, y2):    
        line_width = self.line_style.width
        interval = self.line_interval * 1.414

        x1 = x1 - line_width
        y1 = y1 - line_width
        x2 = x2 + line_width
        y2 = y2 + line_width
        height = y2 - y1
        width = x2 - x2
        len = max(height, width)
        curx = x1
        endx = x2 + len
        while curx < endx:
            canvas.line(self.line_style, curx, y1, curx-len, y1+len)
            curx = curx + interval

class Vert(T):
    "Fills the region with vertical lines"
    def draw(self, x1, y1, x2, y2):    
        interval = self.line_interval
        curx = x1
        while curx < x2:
            canvas.line(self.line_style, curx, y1, curx, y2)
            curx = curx + interval
            
class Horiz(T):
    "Fills the region with horizontal lines"
    def draw(self, x1, y1, x2, y2):
        interval = self.line_interval
        cury = y1
        while cury < y2:
            canvas.line(self.line_style, x1, cury, x2, cury)            
            cury = cury + interval
            
class Stitch(T):
    "Fills the region with horizontal and vertical lines."
    def draw(self, x1, y1, x2, y2):
        interval = self.line_interval
        cury = y1
        while cury < y2:
            canvas.line(self.line_style, x1, cury, x2, cury)
            cury = cury + interval
        curx = x1
        while curx < x2:
            canvas.line(self.line_style, curx, y1, curx, y2)
            curx = curx + interval

class Wave(T):
    "Fills the region with horizontal wavy lines."
    def draw(self, x1, y1, x2, y2):
        x1 = xscale(x1)
        x2 = xscale(x2)
        y1 = yscale(y1)
        y2 = yscale(y2)
        line_width = nscale(self.line_style.width)
        interval = nscale(self.line_interval)
        
        canvas.out.set_line_style(self.line_style)        
        x1 = x1 - line_width
        x2 = x2 + line_width
        cury = y1
        half = interval/2.0
        while cury < y2:
            curx = x1
            canvas.out.newpath()
            canvas.out.moveto(curx, cury)
            while curx < x2:
                canvas.out.lineto(curx + half, cury + half)
                canvas.out.lineto(curx + interval, cury)
                curx = curx + interval
            canvas.out.stroke()
            cury = cury + interval

class Vwave(T):
    """Fills the region with vertical wavy lines."""
    def draw(self, x1, y1, x2, y2):
        x1 = xscale(x1)
        x2 = xscale(x2)
        y1 = yscale(y1)
        y2 = yscale(y2)
        line_width = nscale(self.line_style.width)
        interval = nscale(self.line_interval)
        
        canvas.out.set_line_style(self.line_style)
        y1 = y1 - line_width
        y2 = y2 + line_width
        curx = x1
        half = interval/2.0
        while curx < x2:
            cury = y1
            canvas.out.newpath()
            canvas.out.moveto(curx, cury)
            while cury < y2:
                canvas.out.lineto(curx + half, cury + half)
                canvas.out.lineto(curx, cury + interval)
                cury = cury + interval
            canvas.out.stroke()
            curx = curx + interval        

class Lines(T):
    """Fills the region with a series of short line segments."""
    def draw(self, x1, y1, x2, y2):
        interval = nscale(self.line_interval)
        cury = y1
        j = 0
        while cury < y2:
            curx = x1
            if j % 2 == 1:
                curx = curx + interval/2.0
            while curx < x2:
                canvas.line(self.line_style, curx, cury,
                            curx+interval/2.0, cury)
                curx = curx + interval * 1.5
            j = j + 1
            cury = cury + interval

default = Plain()

color_standards = object_set.T()
gray_standards = object_set.T()

def __intern_both(style):
    global color_standards, gray_standards
    color_standards.add(style)
    gray_standards.add(style)
    return style

def __intern_color(style):
    global color_standards, gray_standards    
    color_standards.add(style)
    return style

def __intern_grayscale(style):
    global color_standards, gray_standards    
    gray_standards.add(style)
    return style

black = __intern_both(Plain(bgcolor=color.gray_scale(0.0), line_style=None))

#
# Fill styles for grayscale charts.
#
gray70 = __intern_grayscale(Plain(bgcolor=color.gray70, line_style=None))
diag = __intern_grayscale(Diag(line_style=line_style.T(cap_style=2)))
gray30 = __intern_grayscale(Plain(bgcolor=color.gray30, line_style=None))
rdiag = __intern_grayscale(Rdiag(line_style=line_style.T(cap_style=2)))
gray10 = __intern_grayscale(Plain(bgcolor=color.gray10, line_style=None))
diag2 = __intern_grayscale(Diag(line_style=line_style.T(width=3, cap_style=2),
                      line_interval=6))
white = __intern_grayscale(Plain(bgcolor=color.gray_scale(1.0), line_style=None))
rdiag2 = __intern_grayscale(Rdiag(line_style=line_style.T(width=3, cap_style=2),
                        line_interval=6))
vert = __intern_grayscale(Vert())
diag3 = __intern_grayscale(Diag(line_style=line_style.T(width=3, color=color.gray50, cap_style=2),
                      line_interval=6))
gray50 = __intern_grayscale(Plain(bgcolor=color.gray50, line_style=None))
horiz = __intern_grayscale(Horiz())
gray90 = __intern_grayscale(Plain(bgcolor=color.gray90, line_style=None))
rdiag3 = __intern_grayscale(Rdiag(line_style=line_style.T(width=3,
                                                          color=color.gray50,
                                                          cap_style=2),
                        line_interval=6))

wave = __intern_grayscale(Wave(line_style=line_style.T(cap_style=2, join_style=1)))
vwave = __intern_grayscale(Vwave(line_style=line_style.T(cap_style=2, join_style=1)))
stitch = __intern_grayscale(Stitch(line_style=line_style.T(cap_style=2, join_style=1)))
lines = __intern_grayscale(Lines(line_style=line_style.T()))

#
# Fill styles for color charts.
#

red = __intern_color(Plain(bgcolor=color.red))
darkseagreen = __intern_color(Plain(bgcolor=color.darkseagreen))
aquamarine1 = __intern_color(Plain(bgcolor=color.aquamarine1))
__intern_color(gray70)
brown = __intern_color(Plain(bgcolor=color.brown))
darkorchid = __intern_color(Plain(bgcolor=color.darkorchid))    
__intern_color(gray50)
__intern_color(diag)
__intern_color(vert)
__intern_color(horiz)
goldenrod = __intern_color(Plain(bgcolor=color.goldenrod))
__intern_color(rdiag)
__intern_color(white)

standards = None
__name_table = None

def init():
    global standards, __name_table
    if theme.use_color:
        standards = color_standards
    else:
        standards = gray_standards
    __name_table = None

def name_table():
    global __name_table
    if not __name_table:
        __name_table = pychart_util.symbol_lookup_table(globals(), standards)
    return __name_table

init()
theme.add_reinitialization_hook(init)

