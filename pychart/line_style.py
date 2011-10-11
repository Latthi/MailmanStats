import color
import pychart_util
import chart_object
import types
import object_set
import theme
import line_style_doc

_keys = {
    "width" : (pychart_util.NumType, 0, theme.default_line_width, "Width of the line, in points."),
    "color": (color.T, 0, color.default, "The color of the line."),
    "dash" : (types.TupleType, 1, None,
              """The value
              of None will draw a solid line. Otherwise, this
              attribute specifies the style of dashed lines. 
              The 2N'th value specifies the length of the line (in points), 
              and 2N+1'th value specfies the length of the blank.

              For example, the dash style of (3,2,4,1) draws a dashed line that
              looks like @samp{---__----_---__----_...}.
              """),
    "cap_style": (types.IntType, 0, 0,
                  """Defines the style of the tip of the line segment.
                  0: butt cap (square cutoff, with no projection beyond),
                  1: round cap (arc), 2: projecting square cap
                  (square cutoff, but the line extends half the line width).
                  See also Postscript/PDF reference manual."""),
    "join_style": (types.IntType, 0, 0,
                   """Join style. 0: Miter join (sharp, pointed corners),
                   1: round join (rounded corners),
                   2: bevel join (flattened corners).
                   See also Postscript/PDF reference manual.""")
    }

class T(chart_object.T):
    __doc__ = line_style_doc.doc
    keys = _keys
##AUTOMATICALLY GENERATED

##END AUTOMATICALLY GENERATED
    def __str__(self):
        s = name_table().lookup(self)
        if s:
            return s
        return "<linestyle: width=%s, color=%s, dash=%s, cap=%d, join=%d>" \
               % (self.width, self.color, self.dash, self.cap_style, self.join_style)
    
default = T(color=color.default)

dash1 = 1.5,1.5  # - - - -
dash2 = 5,2,5,2  # -- -- -- --
dash3 = 1,1 

black = T(color=color.black)
black_dash1 = T(color=color.black, dash=dash1)
black_dash2 = T(color=color.black, dash=dash2)

gray70 = T(color=color.gray70)
gray70_dash1 = T(color=color.gray70, dash=dash1)
gray70_dash2 = T(color=color.gray70, dash=dash2)

gray10 = T(color=color.gray10)
gray10_dash1 = T(color=color.gray10, dash=dash1)
gray10_dash2 = T(color=color.gray10, dash=dash2)

gray50 = T(color=color.gray50)
gray50_dash1 = T(color=color.gray50, dash=dash1)
gray50_dash2 = T(color=color.gray50, dash=dash2)

gray90 = T(color=color.gray90)
gray90_dash1 = T(color=color.gray90, dash=dash1)
gray90_dash2 = T(color=color.gray90, dash=dash2)

gray30 = T(color=color.gray30)
gray30_dash1 = T(color=color.gray30, dash=dash1)
gray30_dash2 = T(color=color.gray30, dash=dash2)

gray70_dash3 = T(color=color.gray70, dash=dash3)
gray10_dash3 = T(color=color.gray10, dash=dash3)
gray50_dash3 = T(color=color.gray50, dash=dash3)
gray90_dash3 = T(color=color.gray90, dash=dash3)

white = T(color=color.white)
default = black

red = T(color=color.red)
darkblue = T(color=color.darkblue)
darkseagreen = T(color=color.darkseagreen)
darkkhaki = T(color = color.darkkhaki)

red_dash1 = T(color=color.red, dash=dash1)
darkblue_dash1 = T(color=color.darkblue, dash=dash1)
darkseagreen_dash1 = T(color=color.darkseagreen, dash=dash1)
darkkhaki_dash1 = T(color=color.darkkhaki, dash=dash1)
    
red_dash2 = T(color=color.red, dash=dash2)
darkblue_dash2 = T(color=color.darkblue, dash=dash2)
darkseagreen_dash2 = T(color=color.darkseagreen, dash=dash2)
darkkhaki_dash2 = T(color=color.darkkhaki, dash=dash2)

standards = None
__name_table = None

def init():
    global standards, __name_table
    standards = object_set.T()
    
    if theme.use_color:
        standards.add(black, red, darkblue, gray70, darkseagreen,
                      darkkhaki, gray30,
                      black_dash1, red_dash1, darkblue_dash1, gray70_dash1,
                      darkseagreen_dash1, darkkhaki_dash1, gray30_dash1,
                      black_dash2, red_dash2, darkblue_dash2, gray70_dash2,
                      darkseagreen_dash2, darkkhaki_dash2, gray30_dash2)
        
    else:
        standards.add(black, black_dash1, black_dash2,
                      gray70, gray70_dash1, gray70_dash2,
                      gray10, gray10_dash1, gray10_dash2,
                      gray50, gray50_dash1, gray50_dash2,
                      gray90, gray90_dash1, gray90_dash2,
                      gray30, gray30_dash1, gray30_dash2,
                      gray70_dash3, gray10_dash3, gray50_dash3, gray90_dash3)

    __name_table = None
    
def name_table():
    global __name_table
    if not __name_table:
        __name_table = pychart_util.symbol_lookup_table(globals(), standards)
    return __name_table

init()
theme.add_reinitialization_hook(init)
