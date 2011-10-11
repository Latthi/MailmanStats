import canvas
import color
import line_style
import fill_style
import chart_object
import object_set
import types
import pychart_util
import tick_mark_doc

_keys = {
    "line_style": (line_style.T, 1, line_style.default, "The line style of the tick mark."),
    "fill_style": (fill_style.T, 1, fill_style.white, "The fill style."),
    "size": (pychart_util.NumType, 0, 5, "Size of the tick mark."),
    }

class Base(chart_object.T):
    __doc__ = tick_mark_doc.doc
    keys = _keys
##AUTOMATICALLY GENERATED

##END AUTOMATICALLY GENERATED
    
    def predraw_check(self):
	if not hasattr(self, "type_checked"):
	    self.type_check()
	self.type_checked = 1

class Circle(Base):
    """Draws a circle. """
    def draw (self, x, y):
	self.predraw_check()
        canvas.ellipsis(self.line_style, self.fill_style, x, y,
                        self.size/2.0, 1)
        
class Square(Base):
    """Draws a square."""
    def draw (self, x, y):
	self.predraw_check()
        # move to the bottom-left corner
        x = x - self.size/2.0
        y = y - self.size/2.0
        canvas.rectangle(self.line_style, self.fill_style,
                         x, y, x+self.size, y+self.size)

class Triangle(Base):
    """Draws a triangle pointing up."""
    def draw (self, x, y):
	self.predraw_check()
        canvas.polygon(self.line_style, self.fill_style,
                       ((x-self.size/1.6, y-self.size/2.0),
                        (x+self.size/1.6, y-self.size/2.0),
                        (x, y+self.size/2.0)))
class DownTriangle(Base):
    """Draws a triangle pointing down."""
    def draw (self, x, y):
	self.predraw_check()
        canvas.polygon(self.line_style, self.fill_style,
                       ((x, y-self.size/2.0),
                        (x-self.size/1.6, y+self.size/2.0),
                        (x+self.size/1.6, y+self.size/2.0)))


class X(Base):
    """Draw a "X"-shaped tick mark. Attribute "fill-style" is ignored."""
    keys = pychart_util.union_dict(Base.keys,
                         {"line_style": (line_style.T, 0,
                                         line_style.T(width=0.7),
                                         "The line style of the tick mark")})
    def draw (self, x, y):
	self.predraw_check()
        # move to the bottom-left corner
        x = x - self.size/2.0
        y = y - self.size/2.0
        canvas.line(self.line_style, x, y, x+self.size, y+self.size)
        canvas.line(self.line_style, x+self.size, y, x, y+self.size)
        
class Plus(Base):
    """Draw a "+"-shaped tick mark. Attribute "fill-style" is ignored."""
    keys = pychart_util.union_dict(Base.keys,
                         {"line_style": (line_style.T, 0,
                                        line_style.T(width=1),
                                         "The line style of the tick mark.")})
    def draw (self, x, y):
	self.predraw_check()
        # move to the bottom-left corner
        canvas.line(self.line_style, x-self.size/1.4, y, x+self.size/1.4, y)
        canvas.line(self.line_style, x, y-self.size/1.4, x, y+self.size/1.4)
        
class Diamond(Base):
    """Draw a square rotated at 45 degrees."""
    def draw (self, x, y):
	self.predraw_check()
        # move to the bottom-left corner
        canvas.polygon(self.line_style, self.fill_style,
                   ((x-self.size/1.4, y), (x, y+self.size/1.4),
                    (x+self.size/1.4, y), (x, y-self.size/1.4)))

class Star(Base):
    """Draw a "*". Attribute "fill-style" is ignored."""
    keys = pychart_util.union_dict(Base.keys,
                         {"line_style": (line_style.T, 0,
                                        line_style.T(width=1),
                                         "The line style of the tick mark.")})
    def draw (self, x, y):
	self.predraw_check()
        # move to the bottom-left corner
        midx = x
        midy = y
        d_len = self.size / 2.0
        r_len = self.size * 1.414 / 2.0
        canvas.line(self.line_style, x-d_len, y-d_len,
                    x+d_len, y+d_len)
        canvas.line(self.line_style, x+d_len, y-d_len,
                    x-d_len, y+d_len) 
        canvas.line(self.line_style, midx, y-r_len, midx, y+r_len)
        canvas.line(self.line_style, x-r_len, midy, x+r_len, midy)
        
class Null(Base):
    """This tickmark doesn't draw anything. All the attributes are ignored."""
    def __init__ (self):
        self.line_style = None
        self.fill_style = None
        self.size = -1
    def draw (self, x, y):
        pass
    
standards = object_set.T()
def __intern(style):
    standards.add(style)
    return style
     
square = __intern(Square())
x = __intern(X())
star = __intern(Star())
plus = __intern(Plus())
dia = __intern(Diamond())
tri = __intern(Triangle())
dtri = __intern(DownTriangle())
circle1 = __intern(Circle(size=1))
circle2 = __intern(Circle(size=3))
circle3 = __intern(Circle(size=5))
blacksquare = __intern(Square(fill_style=fill_style.black))
blackdia = __intern(Diamond(fill_style=fill_style.black))
blacktri = __intern(Triangle(fill_style=fill_style.black))
blackdtri = __intern(DownTriangle(fill_style=fill_style.black))
blackcircle3 = __intern(Circle(size=3, fill_style=fill_style.black))
blackcircle1 = __intern(Circle(size=1, fill_style=fill_style.black))
gray70square = __intern(Square(fill_style=fill_style.gray70))
gray70dia = __intern(Diamond(fill_style=fill_style.gray70))
gray70tri = __intern(Triangle(fill_style=fill_style.gray70))
gray70dtri = __intern(DownTriangle(fill_style=fill_style.gray70))
gray70circle3 = __intern(Circle(size=3, fill_style=fill_style.gray70))
gray70circle1 = __intern(Circle(size=1, fill_style=fill_style.gray70))
default = __intern(Null())

