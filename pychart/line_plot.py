import canvas
import tick_mark
import line_style
import pychart_util
import error_bar
import chart_object
import legend
import types
import object_set
import line_plot_doc
import theme

default_width = 1.2
line_style_itr = None


_keys = {
    "data" : (pychart_util.AnyType, 1, None, pychart_util.data_desc),
    "label": (types.StringType, 1, "???", pychart_util.label_desc),
    "data_label_offset": (pychart_util.CoordType, 1, (0, 5),
                          """The location of data labels relative to the sample point. Meaningful only when data_label_format != None."""),
    "data_label_format": (pychart_util.FormatType, 1, None,
                          """The format string for the label printed 
                          beside a sample point.
                          It can be a `printf' style format string, or 
                          a two-parameter function that takes the (x, y)
                          values and returns a string. """
                          + pychart_util.string_desc),
    "xcol" : (types.IntType, 0, 0, pychart_util.xcol_desc),
    "ycol": (types.IntType, 0, 1, pychart_util.ycol_desc),
    "y_error_minus_col": (types.IntType, 0, 2,
                          """The column (within "data") from which the depth of the errorbar is extracted. Meaningful only when error_bar != None. <<error_bar>>"""),
    "y_error_plus_col": (types.IntType, 1, None,
                         """The column (within "data") from which the height of the errorbar is extracted. Meaningful only when error_bar != None. <<error_bar>>"""),
    "y_qerror_minus_col":  (types.IntType, 1, None, "<<error_bar>>"),
    "y_qerror_plus_col":  (types.IntType, 1, None, "<<error_bar>>"),

    "line_style": (line_style.T, 1, lambda: line_style_itr.next(), pychart_util.line_desc,
                   "By default, a style is picked from standard styles round-robin. @xref{line_style}."),

    "tick_mark": (tick_mark.Base, 1, None, pychart_util.tick_mark_desc),
    "error_bar": (error_bar.Base, 1, None,
                  "The style of the error bar. <<error_bar>>"),
    }

class T(chart_object.T):
    __doc__ = line_plot_doc.doc
    keys =  _keys
    def check_integrity(self):
	self.type_check()
        pychart_util.check_data_integrity(self, self.data,
                                          (self.xcol, self.ycol))
        
##AUTOMATICALLY GENERATED

##END AUTOMATICALLY GENERATED
    def get_data_range(self, which):
        if which == 'X':
            return pychart_util.get_data_range(self.data, self.xcol)
        else:
            return pychart_util.get_data_range(self.data, self.ycol)
    def get_legend_entry(self):
        if self.label:
            return legend.Entry(line_style=self.line_style,
                                tick_mark=self.tick_mark,
                                fill_style=None,
                                label=self.label)
        return None
    
    def draw(self, ar):

        # Draw the line
        canvas.clip(ar.loc[0], ar.loc[1],
                ar.loc[0] + ar.size[0],
                ar.loc[1] + ar.size[1])
        if self.line_style:
            points = []
            for pair in self.data:
                points.append((ar.x_pos(pair[self.xcol]), ar.y_pos(pair[self.ycol])))
            canvas.lines(self.line_style, points)
        canvas.endclip()
        
        # Draw tick marks and error bars
        canvas.clip(ar.loc[0] - 10, ar.loc[1] - 10,
                ar.loc[0] + ar.size[0] + 10,
                ar.loc[1] + ar.size[1] + 10)
        for pair in self.data:
            x = pair[self.xcol]
            y = pair[self.ycol]
            x_pos = ar.x_pos(x)
            y_pos = ar.y_pos(y)

            if self.error_bar:
                plus = pair[self.y_error_plus_col or self.y_error_minus_col]
                minus = pair[self.y_error_minus_col or self.y_error_plus_col]
                if self.y_qerror_minus_col or self.y_qerror_plus_col:
                    q_plus = pair[self.y_qerror_minus_col or self.y_qerror_plus_col]
                    q_minus = pair[self.y_qerror_plus_col or self.y_qerror_minus_col]
                    self.error_bar.draw((x_pos, y_pos),
                                       ar.y_pos(y - minus),
                                       ar.y_pos(y + plus),
                                       ar.y_pos(y - q_minus),
                                       ar.y_pos(y + q_plus))
                else:
                    self.error_bar.draw((x_pos, y_pos),
                                        ar.y_pos(y - minus),
                                        ar.y_pos(y + plus))
                    
            if self.tick_mark:
                self.tick_mark.draw(x_pos, y_pos)
            if self.data_label_format:
                canvas.show(x_pos + self.data_label_offset[0],
                            y_pos + self.data_label_offset[1],
                            "/hC" + pychart_util.apply_format(self.data_label_format, (x, y), 1))

        canvas.endclip()

def init():
    global line_style_itr
    line_styles = object_set.T()
    for org_style in line_style.standards.objs:
        style = line_style.T(width = default_width, color = org_style.color,
                             dash = org_style.dash)
        line_styles.add(style)

    line_style_itr = line_styles.iterate()

theme.add_reinitialization_hook(init)

