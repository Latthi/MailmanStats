import string
import canvas
import tick_mark
import font
import line_style
import color
import fill_style
import chart_object
import pychart_util
import types
import legend_doc

class Entry(chart_object.T):
    keys = {"line_len" : (pychart_util.NumType, 0, 10,
                          "Length of the sample line for line plots."),
            "rect_size" : (pychart_util.NumType, 0, 7,
                           "Size of the sample 'blob' for bar range charts."),
            "tick_mark": (tick_mark.Base, 1, None, ""),
            "line_style": (line_style.T, 1, None, ""),
            "fill_style": (fill_style.T, 1, None, ""),
            "label": (types.StringType, 0, "???", ""),
            }
    __doc__ = legend_doc.doc_entry
##AUTOMATICALLY GENERATED

##END AUTOMATICALLY GENERATED
    
    def label_width(self):
        return font.text_width(" " + self.label)
    def sample_width(self):
        w = 0
        if self.fill_style != None:
            w = w + self.line_len
        elif self.line_style != None:
            w = w + self.line_len
        elif self.tick_mark != None:
            w = w + self.tick_mark.size
        return w
    def height(self):
        h = font.text_height(self.label)[0]
        return h
    
    def draw(self, ar, x_tick, x_label, y):
        """Draw a legend entry. X_TICK and X_LABEL are the X location \
        (in points) of where the sample and label are drawn."""
        
        nr_lines = len(string.split(self.label, "\n"))
        text_height = font.text_height(self.label)[0]
        line_height = text_height / float(nr_lines)
        y_center = y + text_height - line_height/1.5
            
        if self.fill_style != None:
            canvas.rectangle(self.line_style, self.fill_style,
                             x_tick, y_center - self.rect_size/2.0,
                             x_tick + self.rect_size,
                             y_center + self.rect_size/2.0)
        elif self.line_style != None:
            canvas.line(self.line_style, x_tick, y_center,
                        x_tick + self.line_len, y_center)
            if self.tick_mark != None:
                self.tick_mark.draw(x_tick + self.line_len/2.0, y_center)
        elif self.tick_mark != None:
            self.tick_mark.draw(x_tick, y_center)
            
        canvas.show(x_label, y, self.label)

__doc__ = """Legend is a rectangular box drawn in a chart to describe
the meanings of plots. The contents of a legend box is extracted from
plots' "label", "line-style", and "tick-mark" attributes.

This module exports a single class, legend.T.  Legend.T is a part of
an area.T object, and is drawn automatically when area.draw() method
is called. """

class T(chart_object.T):
    __doc__ = legend_doc.doc
    keys = {
        "inter_row_sep": (pychart_util.NumType, 0, 0,
                          "Space between each row in the legend."),
        "inter_col_sep": (pychart_util.NumType, 0, 0,
                          "Space between each column in the legend."),
        "frame_line_style": (line_style.T, 1, line_style.default, ""),
        "frame_fill_style": (fill_style.T, 0, fill_style.white, ""),
        "top_fudge": (pychart_util.NumType, 0, 0,
                      "Amount of space above the first line."),
        "bottom_fudge": (pychart_util.NumType, 0, 3,
                         "Amount of space below the last line."),
        "left_fudge": (pychart_util.NumType, 0, 5,
                       "Amount of space left of the legend."),
        "right_fudge": (pychart_util.NumType, 0, 5,
                        "Amount of space right of the legend."),
        "loc": (pychart_util.CoordType, 1, None,
                "Bottom-left corner of the legend."),
	"shadow": (pychart_util.ShadowType, 1, None, pychart_util.shadow_desc),
        "nr_rows": (types.IntType, 1, 9999, "Number of rows in the legend. If the number of plots in a chart is larger than nr_rows, multiple columns are created for their legends."),

        }
##AUTOMATICALLY GENERATED

##END AUTOMATICALLY GENERATED
    def draw(self, ar, entries):
        if not self.loc:
            x = ar.loc[0] + ar.size[0] * 1.1
            y = ar.loc[1]
        else:
            x = self.loc[0]
            y = self.loc[1]

        nr_rows = min(self.nr_rows, len(entries))
        nr_cols = (len(entries)-1) / nr_rows + 1
        
        ymin = y
	max_label_width = [0] * nr_cols
        max_sample_width = [0] * nr_cols
        heights = [0] * nr_rows
        
        for i in range(len(entries)):
            l = entries[i]
            (col, row) = divmod(i, nr_rows)
            max_label_width[col] = max(l.label_width(), max_label_width[col])
            max_sample_width[col] = max(l.sample_width(), max_sample_width[col])
            heights[row] = max(l.height(), heights[row])

        for h in heights:
            y = y + h
        y = y + self.inter_row_sep * (nr_rows - 1)
        ymax = y

        tot_width = self.inter_col_sep * (nr_cols -1)
        for w in max_label_width:
            tot_width = tot_width + w
        for w in max_sample_width:
            tot_width = tot_width + w
            
	canvas.rectangle(self.frame_line_style, self.frame_fill_style,
                         x - self.left_fudge,	
                         ymin - self.bottom_fudge,	
                         x + tot_width + self.right_fudge,
                         ymax + self.top_fudge,
			 self.shadow)

        for col in range(nr_cols):
            this_y = y
            this_x = x
            for row in range(nr_rows):
                pass
                this_y = this_y - heights[row]
                l = entries[col * nr_cols + row]
                if row != 0:
                    this_y = this_y - self.inter_row_sep
                    
                l.draw(ar, this_x, this_x + max_sample_width[col], this_y)
            x = x + max_label_width[col] + max_sample_width[col] + self.inter_col_sep


