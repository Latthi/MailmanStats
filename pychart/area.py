import coord
import line_style
import legend
import axis
import pychart_util
import chart_object
import fill_style
import types
import math
import canvas
import area_doc
import linear_coord
import category_coord

_dummy_legend = legend.T()

zigZagSize=30

_keys = {
    "loc" : (pychart_util.CoordType, 0, (0,0),
             """The location of the bottom-left corner of the chart.
@cindex chart location
@cindex location, chart."""),
    "size" : (pychart_util.CoordType, 0, (120,110),
              """The size of the chart-drawing area, excluding axis labels,
              legends, tick marks, etc.
@cindex chart size
@cindex size, chart              
              """),
    "bg_style": (fill_style.T, 1, None, "Background fill-pattern."),
    "border_line_style": (line_style.T, 1, None, "Line style of the outer frameof the chart."),
    "x_coord":
    (coord.T, 0, linear_coord.T(),
     """Specifies the X coordinate system. <<coord>>.
"""),
    "y_coord": (coord.T, 0, linear_coord.T(),
                "Set the Y coordinate system. See also x_coord."),
    "x_range": (pychart_util.CoordType, 1, None,
                """Specifies the range of X values to be displayed in the
                chart. The value can be None, in which case both the values are
                computed automatically.  Otherwise, the value must be
                a tuple of format (MIN, MAX). Both MIN and MAX must be
                either None or a number. If MIN (or MAX) is None, its value
                is computed automatically. For example, if x_range = (None,5),
                then the minimum X value is computed automatically, but
                the maximum X value is fixed at 5."""
                ),
    "y_range": (pychart_util.CoordType, 1, None,
                """Specifies the range of Y values to be displayed in the
                chart. The value can be None, in which case both the values are
                computed automatically.  Otherwise, the value must be
                a tuple of format (MIN, MAX). Both MIN and MAX must be
                either None or a number. If MIN (or MAX) is None, its value
                is computed automatically. For example, if y_range = (None,5),
                then the minimum Y value is computed automatically, but
                the maximum Y value is fixed at 5."""),
    "x_axis": (axis.X, 1, None, "The X axis. <<axis>>."),
    "y_axis": (axis.Y, 1, None, "The Y axis. <<axis>>."),
    "x_grid_style" : (line_style.T, 1, None,
                      """The style of X grid lines.
@cindex grid lines"""),
    "y_grid_style" : (line_style.T, 1, line_style.gray70_dash3,
                      "The style of Y grid lines."),
    "x_grid_interval": (pychart_util.IntervalType, 1, None,
                        "The horizontal grid-line interval."),
    "y_grid_interval": (pychart_util.IntervalType, 1, None,
                        "The vertical grid-line interval."),
    "x_grid_over_plot": (types.IntType, 0, 0,
                      "If true, grid lines are drawn over plots. Otherwise, plots are drawn over grid lines."),
    "y_grid_over_plot": (types.IntType, 0, 0, "See x_grid_over_plot."),
    "_plots": (types.ListType, 1, pychart_util.new_list, "Used only intervally by pychart"),
    "legend": (legend.T, 1, _dummy_legend, "The legend of the chart.",
               "a legend is by default displayed in the right-center of the chart."),
    }


class T(chart_object.T):
    keys = _keys
    __doc__ = area_doc.doc
##AUTOMATICALLY GENERATED

##END AUTOMATICALLY GENERATED
    def x_pos(self, xval):
        "Return the x position (on the canvas) corresponding to XVAL."
        off = self.x_coord.get_canvas_pos(self.size[0], xval,
                                          self.x_range[0], self.x_range[1])
        return self.loc[0] + off
    
    def y_pos(self, yval):
        "Return the y position (on the canvas) corresponding to YVAL."
        off = self.y_coord.get_canvas_pos(self.size[1], yval,
                                          self.y_range[0], self.y_range[1])
        return self.loc[1] + off

    def x_tic_points(self, interval):
        "Return the list of X values for which tick marks and grid lines are drawn."
        if type(interval) == types.FunctionType:
            return apply(interval, self.x_range)

        return self.x_coord.get_tics(self.x_range[0], self.x_range[1], interval)
    def y_tic_points(self, interval):
        "Return the list of Y values for which tick marks and grid lines are drawn."
        if type(interval) == types.FunctionType:
            return apply(interval, self.y_range)

        return self.y_coord.get_tics(self.y_range[0], self.y_range[1], interval)
    def __draw_x_grid_and_axis(self):
        if self.x_grid_style:
            for i in self.x_tic_points(self.x_grid_interval):
                x = self.x_pos(i)
                if x > self.loc[0]:
                    canvas.line(self.x_grid_style,
                                x, self.loc[1], x, self.loc[1]+self.size[1])
        if self.x_axis:
            self.x_axis.draw(self)
    def __draw_y_grid_and_axis(self):
        if self.y_grid_style:
            for i in self.y_tic_points(self.y_grid_interval):
                y = self.y_pos(i)
                if y > self.loc[1]:
                    canvas.line(self.y_grid_style,
                                self.loc[0], y,
                                self.loc[0]+self.size[0], y)
        if self.y_axis:
            self.y_axis.draw(self)

    def __get_data_range(self, r, which, coord, interval):
        if isinstance(coord, category_coord.T):
            # This info is unused for the category coord type.
            # So I just return a random value.
            return ((0,0), 1)

        r = r or (None, None)
        
        if len(self._plots) == 0:
            raise ValueError, "No chart to draw, and no data range specified.\n";
        dmin, dmax = 99999999, -99999999
 
        for plot in self._plots:
            this_min, this_max = plot.get_data_range(which)
            dmin = min(this_min, dmin)
            dmax = max(this_max, dmax)

        if interval and type(interval) == types.FunctionType:
            tics = apply(interval, (dmin, dmax))
            dmin = tics[0]
            dmax = tics[len(tics)-1]
        else:
            dmin, dmax, interval = coord.get_min_max(dmin, dmax, interval)

        if r[0] != None:
            dmin = r[0]
        if r[1] != None:
            dmax = r[1]
        return ((dmin, dmax), interval)
    def draw(self):
        "Draw the charts."
        self.type_check()
        for plot in self._plots:
            plot.check_integrity()
            
        self.x_range, self.x_grid_interval = \
                      self.__get_data_range(self.x_range, 'X',
                                            self.x_coord,
                                            self.x_grid_interval)
            
        self.y_range, self.y_grid_interval = \
                      self.__get_data_range(self.y_range, 'Y',
                                            self.y_coord,
                                            self.y_grid_interval)
        
        canvas.rectangle(self.border_line_style, self.bg_style,
                         self.loc[0], self.loc[1],
                         self.loc[0] + self.size[0], self.loc[1] + self.size[1])

        if not self.x_grid_over_plot:
            self.__draw_x_grid_and_axis()

        if not self.y_grid_over_plot:
            self.__draw_y_grid_and_axis()
        canvas.clip(self.loc[0] - 10, self.loc[1] - 10,
                    self.loc[0] + self.size[0] + 10,
                    self.loc[1] + self.size[1] + 10)
        for plot in self._plots:
            plot.draw(self)
            
        canvas.endclip()
            
        if self.x_grid_over_plot:
            self.__draw_x_grid_and_axis()
        if self.y_grid_over_plot:
            self.__draw_y_grid_and_axis()

        if self.legend == _dummy_legend:
            self.legend = legend.T()
            
        if self.legend:
            legends = []
            for plot in self._plots:
                entry = plot.get_legend_entry()
                if entry == None:
                    pass
                elif type(entry) != types.ListType:
                    legends.append(entry)
                else:
                    for e in entry:
                        legends.append(e)
            self.legend.draw(self, legends)

    def add_plot(self, *plots):
        "Add PLOTS... to the area."
        for plot in plots:
            self._plots.append(plot)
