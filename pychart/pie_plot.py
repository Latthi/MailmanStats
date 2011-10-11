import canvas
import text_box
import fill_style
import line_style
import pychart_util
import chart_object
import arrow
import legend
import types
import font
import pie_plot_doc

class T(chart_object.T):
    __doc__ = pie_plot_doc.doc
    keys = {
        "start_angle" : (pychart_util.NumType, 0, 90,
                         """The angle at which the first item is drawn."""),
        "center" : (pychart_util.CoordType, 1, None, ""),
        "radius" : (pychart_util.NumType, 1, None, ""),
        "line_style" : (line_style.T, 0, line_style.default, ""),
        "fill_styles" : (types.ListType, 0, fill_style.standards.objs,
                         """The fill style of each item. The length of the
                         list should be equal to the length of the data. 
                         """),
        "arc_offsets" : (types.ListType, 1, None,
                         """You can draw each pie "slice" offset from the
                         center of the circle. This attribute specifies the
                         amount of offset (in points) from the center.
                         The value of None will draw the slice archored at the
                         center."""
                         ),
        "data" : (pychart_util.AnyType, 1, None, pychart_util.data_desc),
        "label_col" : (types.IntType, 0, 0,
                       """The column, within "data", from which the labels of items are retrieved."""),
        "data_col": (types.IntType, 0, 1,
                     """ The column, within "data", from which the data values are retrieved."""),
        "label_offset": (pychart_util.NumType, 1, None, ""),
        "arrow_style": (arrow.T, 1, None,
                        """The style of arrow that connects a label
                        to the corresponding "pie"."""),
        "label_line_style": (line_style.T, 1, None, ""),
        "label_fill_style": (fill_style.T, 0, fill_style.default, ""),
        "shadow": (pychart_util.ShadowType, 1, None, pychart_util.shadow_desc)
        }
##AUTOMATICALLY GENERATED

##END AUTOMATICALLY GENERATED
    def _total(self):
        v = 0
        for val in self.data:
            v = v + val[self.data_col]
        return v

    def check_integrity(self):
	self.type_check()
        pychart_util.check_data_integrity(self, self.data,
                                          (self.label_col, self.data_col))
    def get_data_range(self, which):
        return (0, 1)
    def get_legend_entry(self):
        legends = []
        i = 0
        for val in self.data:
            fill = self.fill_styles[i]
            i = (i + 1) % len(self.fill_styles)
            legends.append(legend.Entry(line_style=self.line_style,
                                        fill_style=fill, 
                                        label=val[self.label_col]))
        return legends
    
    def draw(self, ar):
        center = self.center
        if not center:
            center = (ar.loc[0] + ar.size[0]/2.0,
                      ar.loc[1] + ar.size[1]/2.0)
        radius = self.radius
        if not radius:
            radius = min(ar.size[0]/2.0, ar.size[1]/2.0) * 0.5

        label_offset = radius + (self.label_offset or radius * 0.1)
        
        total = self._total()
        i = 0
        cur_angle = self.start_angle
        for val in self.data:
            fill = self.fill_styles[i]
            degree = 360 * float(val[self.data_col]) / float(total)
            
            off = (0, 0)
            if len(self.arc_offsets) > i:
                off = pychart_util.rotate(self.arc_offsets[i], 0, cur_angle - degree/2.0)
            x_center = center[0]+ off[0]
            y_center = center[1]+ off[1]
            
            canvas.ellipsis(self.line_style, fill,
                            x_center, y_center, radius, 1,
                            cur_angle - degree, cur_angle,
                            self.shadow)

            label = val[self.label_col]
            (x_label, y_label) = pychart_util.rotate(label_offset, 0, cur_angle - degree/2.0)
            (x_arrowtip, y_arrowtip) = pychart_util.rotate(radius, 0, cur_angle - degree/2.0)
            # Labels on left side of pie need
            # their text to avoid obscuring the pie
            if x_label < 0:
	       x_label = x_label - font.text_width(label)
            
            t = text_box.T(loc = (x_label + x_center, y_label + y_center),
                           text = label,
                           line_style = self.label_line_style,
                           fill_style = self.label_fill_style)
            if self.arrow_style:
                t.add_arrow((x_arrowtip + x_center, y_arrowtip + y_center),
                            None, self.arrow_style)
                
            t.draw()
            cur_angle = (cur_angle - degree) % 360
            i = (i + 1) % len(self.fill_styles)


