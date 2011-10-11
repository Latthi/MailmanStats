import canvas
import tick_mark
import line_style
import pychart_util
import chart_object
import fill_style
import types
import error_bar_doc

__doc__ = """Pychart offers several styles of error bars. Some of them
only displays the min/max confidence interval, while others can display
quartiles in addition to min/max.""" 

class Base(chart_object.T):
    keys = {}
##AUTOMATICALLY GENERATED

##END AUTOMATICALLY GENERATED
    pass

# Two horizontal lines at min & max locations.
class error_bar1(Base):
    __doc__ = error_bar_doc.doc_1
    keys = {"tic_len" : (pychart_util.NumType, 0, 10, "Length of the horizontal bars"),
            "line_style": (line_style.T, 1, line_style.default, "<<line_style>>")
            }
##AUTOMATICALLY GENERATED

##END AUTOMATICALLY GENERATED
    def draw(self, loc, min, max, qmin = None, qmax = None):
        x = loc[0]
        y = min
        canvas.line(self.line_style, x-self.tic_len/2.0, y, x+self.tic_len/2.0, y)
        y = max
        canvas.line(self.line_style, x-self.tic_len/2.0, y, x+self.tic_len/2.0, y)

class error_bar2(Base):
    __doc__ = error_bar_doc.doc_2
    keys = {"tic_len" : (pychart_util.NumType, 0, 3,
                        "The length of the horizontal bars"),
            "hline_style": (line_style.T, 0, line_style.default,
                           "The style of the horizontal bars. <<line_style>>."),
            "vline_style": (line_style.T, 1, None,
                           "The style of the vertical bar.")
             }

##AUTOMATICALLY GENERATED

##END AUTOMATICALLY GENERATED
    def draw(self, loc, min, max, qmin = None, qmax = None):
        vline_style = self.vline_style
        if not vline_style:
            vline_style = self.hline_style
        x = loc[0]
        y1 = min
        canvas.line(self.hline_style, x-self.tic_len/2.0, y1, x+self.tic_len/2.0, y1)
        y2 = max
        canvas.line(self.hline_style, x-self.tic_len/2.0, y2, x+self.tic_len/2.0, y2)
        canvas.line(vline_style, x, y1, x, y2)

class error_bar3(Base):
    # Tufte style
    __doc__ = "This style is endorsed by the Tufte's books. " \
              + error_bar_doc.doc_3
    keys = { "line_style": (line_style.T, 1, line_style.default, "")
             }

##AUTOMATICALLY GENERATED

##END AUTOMATICALLY GENERATED
    def draw(self, loc, min, max, qmin, qmax):
        x = loc[0]
        canvas.line(self.line_style, x, min, x, qmin)
        canvas.line(self.line_style, x, qmax, x, max)

class error_bar4(Base):
    __doc__ = error_bar_doc.doc_4
    keys = { "line_style": (line_style.T, 1, line_style.default, ""),
             "fill_style": (fill_style.T, 1, fill_style.gray70, ""),
             "box_width": (pychart_util.NumType, 1, 4, ""),
             "tic_len": (pychart_util.NumType, 1, 4, "")
             }
##AUTOMATICALLY GENERATED

##END AUTOMATICALLY GENERATED
    def draw(self, loc, min, max, qmin, qmax):
        x = loc[0]
        style = self.line_style
        y1 = min
        canvas.line(style, x-self.tic_len/2.0, y1, x+self.tic_len/2.0, y1)
        y2 = max
        canvas.line(style, x-self.tic_len/2.0, y2, x+self.tic_len/2.0, y2)
        canvas.line(style, x, y1, x, y2)

        canvas.rectangle(style, self.fill_style,
                         x-self.box_width/2.0, qmin,
                         x+self.box_width/2.0, qmax)

# vertical line
class error_bar5(Base):
    __doc__ = error_bar_doc.doc_5
    keys = { "line_style": (line_style.T, 1, line_style.default, "")
             }
##AUTOMATICALLY GENERATED

##END AUTOMATICALLY GENERATED
    def draw(self, loc, min, max, qmin = None, qmax = None):
        x = loc[0]
        y = loc[1]

        min = (min - y) *1 + y
        max = (max - y) *1+ y
        canvas.line(self.line_style, x, min, x, max)
    
bar1 = error_bar1()
bar2 = error_bar2()
bar3 = error_bar3()
bar4 = error_bar4()
bar5 = error_bar5()





