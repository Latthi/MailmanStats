import canvas
import line_style
import pychart_util
import chart_object
import fill_style
import legend
import types
import range_plot_doc

from scaling import *


class T(chart_object.T):
    __doc__ = range_plot_doc.doc
    keys = {
        "data" : (pychart_util.AnyType, 1, None, pychart_util.data_desc),
        "label": (types.StringType, 1, "???", pychart_util.label_desc),
        "xcol" : (types.IntType, 0, 0, pychart_util.xcol_desc),
        "min_col": (types.IntType, 0, 1,
                   "The lower bound of the sweep is extracted from "
                   + "this column of data."),
        "max_col": (types.IntType, 0, 2, 
                   "The upper bound of the sweep is extracted from "
                   + "this column of data."),
        "line_style": (line_style.T, 1, line_style.default,
                      "The style of the boundary line."),
        "fill_style": (fill_style.T, 1, fill_style.default,
                      ""),
        }
    
##AUTOMATICALLY GENERATED

##END AUTOMATICALLY GENERATED

    def check_integrity(self):
	self.type_check()
        pychart_util.check_data_integrity(self, self.data,
                                          (self.xcol, self.min_col, self.max_col))
    def get_data_range(self, which):
        if which == 'X':
            return pychart_util.get_data_range(self.data, self.xcol)
        else:
            ymax = (pychart_util.get_data_range(self.data, self.max_col))[1]
            ymin = (pychart_util.get_data_range(self.data, self.min_col))[0]
            return (ymin, ymax)
    def get_legend_entry(self):
        if self.label:
            return legend.Entry(line_style=self.line_style,
                                fill_style=self.fill_style,
                                label=self.label)
        return None

    def draw(self, ar):
        
        prevPair = None

        xmin=9999999
        xmax=-9999999
        ymin=9999999
        ymax=-9999999

        # Draw the boundary in a single stroke.
        canvas.out.gsave()
        canvas.out.newpath()
        for pair in self.data:
            x = pair[self.xcol]
            y = pair[self.max_col]
            xmin = min(xmin, ar.x_pos(x))
            xmax = max(xmax, ar.x_pos(x))
            ymin = min(ymin, ar.y_pos(y))
            ymax = max(ymax, ar.y_pos(y))
            if prevPair != None:
                canvas.out.lineto(xscale(ar.x_pos(x)), yscale(ar.y_pos(y)))
            else:
                canvas.out.moveto(xscale(ar.x_pos(x)), yscale(ar.y_pos(y)))
            prevPair = pair

        for i in range(len(self.data)-1, -1, -1):
            pair = self.data[i]
            x = pair[self.xcol]
            y = pair[self.min_col]
            xmin = min(xmin, ar.x_pos(x))
            xmax = max(xmax, ar.x_pos(x))
            ymin = min(ymin, ar.y_pos(y))
            ymax = max(ymax, ar.y_pos(y))
            canvas.out.lineto(xscale(ar.x_pos(x)), yscale(ar.y_pos(y)))
        canvas.out.closepath()

        # create a clip region, and fill it.
        canvas.out.clip()
        canvas.fill_with_pattern(self.fill_style, xmin, ymin, xmax, ymax)
        canvas.out.grestore()

        # draw the boundary.
        prevPair = None
        canvas.out.newpath()
        canvas.out.set_line_style(self.line_style)
        for pair in self.data:
            x = pair[self.xcol]
            y = pair[self.min_col]
            if prevPair != None:
                canvas.out.lineto(xscale(ar.x_pos(x)), yscale(ar.y_pos(y)))
            else:
                canvas.out.moveto(xscale(ar.x_pos(x)), yscale(ar.y_pos(y)))
            prevPair = pair
        canvas.out.stroke()

        prevPair = None
        canvas.out.newpath()
        canvas.out.set_line_style(self.line_style)
        for pair in self.data:
            x = pair[self.xcol]
            y = pair[self.max_col]
            if prevPair != None:
                canvas.out.lineto(xscale(ar.x_pos(x)), yscale(ar.y_pos(y)))
            else:
                canvas.out.moveto(xscale(ar.x_pos(x)), yscale(ar.y_pos(y)))
            prevPair = pair
        canvas.out.stroke()


