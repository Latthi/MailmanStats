import canvas
import font
import pychart_util
import chart_object
import line_style
import types
import math
import theme
import axis_doc

class Base(chart_object.T):
    keys = {
       "tic_interval" : (pychart_util.IntervalType, 1, None, 
                         pychart_util.interval_desc("tick marks")),
       "tic_len" : (pychart_util.NumType, 0, 6, """The length of tick lines. The value can be negative, in which case the tick lines are drawn right of (or above) the axis."""),
       "minor_tic_interval" : (pychart_util.IntervalType, 1, None,
                               pychart_util.interval_desc("minor tick marks")),
       "minor_tic_len" : (pychart_util.NumType, 0, 3, "The length of minor tick marks.  The value can be negative, in which case the tick lines are drawn right of (or above) the axis."""),
       "line_style": (line_style.T, 1, line_style.default, 
                      "The style of tick lines."),
       "label": (types.StringType, 1, "axis label",
                 "The description of the axis. <<font>>."),
       "format": (pychart_util.FormatType, 0, "%s", 
                  """The format string for tick labels.
                  It can be a `printf' style format string, or 
                  a single-parameter function that takes a X (or Y) value
                  and returns a string. """ +
                  pychart_util.string_desc),
       "label_offset": (pychart_util.CoordOrNoneType, 0, (None,None),
                        "The location where the axis label is drawn. "
                        "Relative to the middle of the axis."),
       "tic_label_offset": (pychart_util.CoordType, 0, (0,0),
                            "The location where the tick labels is drawn. "
                            "Relative to the tip of the tick mark."),
       "offset": (pychart_util.NumType, 0, 0,
                  """The location of the axis. The unit is points.
                  The value of 0 draws the
                  axis at the left (for the Y axis) or bottom (for the X axis)
                  edge of the drawing area.""")
       }

def pick_tick_interval(axis_len, p):
    range = p[1]-p[0]
    interval = 10 ** int(math.log(range)/math.log(10))
    while axis_len * interval / range >= 30:
        interval = float(interval / 10.0)
    if axis_len * interval / range < 10:
       interval = interval * 5
    return interval

class X(Base):
    __doc__ = axis_doc.doc_x
##AUTOMATICALLY GENERATED

##END AUTOMATICALLY GENERATED
    def draw(self, ar):
        self.type_check()
        self.tic_interval = self.tic_interval or ar.x_grid_interval
        y_base = ar.loc[1] + self.offset
      
        canvas.line(self.line_style, ar.loc[0], y_base,
                    ar.loc[0]+ ar.size[0], y_base)

        tic_dic = {}
        max_tic_height = 0
      
        for i in ar.x_tic_points(self.tic_interval):
            tic_dic[i] = 1
            ticx = ar.x_pos(i)

            str = "/hC" + pychart_util.apply_format(self.format, (i, ), 0)

            (total_height, base_height) = font.text_height(str)
            max_tic_height = max(max_tic_height, total_height)

            canvas.line(self.line_style, ticx, y_base, ticx, y_base-self.tic_len)
            canvas.show(ticx+self.tic_label_offset[0], 
                        y_base-self.tic_len-base_height+self.tic_label_offset[1],
                        str)
         
        if self.minor_tic_interval:
            for i in ar.x_tic_points(self.minor_tic_interval):
                if tic_dic.has_key(i):
                    # a major tic was drawn already.
                    pass
                else:
                    ticx = ar.x_pos(i)
                    canvas.line(self.line_style, ticx, y_base, ticx,
                                y_base-self.minor_tic_len)

        if self.label != None:
            str = "/hC/vM" + self.label
            (label_height, base_height) = font.text_height(str)
            xlabel = ar.loc[0] + ar.size[0]/2.0
            ylabel = y_base - self.tic_len - max_tic_height - 10
            if self.label_offset[0] != None:
                xlabel = xlabel + self.label_offset[0]
            if self.label_offset[1] != None:
                ylabel = ylabel + self.label_offset[1]
            canvas.show(xlabel, ylabel, str)

        tic_dic = {}
        max_tic_height = 0

        for i in ar.x_tic_points(self.tic_interval):
            tic_dic[i] = 1
            ticx = ar.x_pos(i)

            str = "/hC" + pychart_util.apply_format(self.format, (i,), 0)

            (total_height, base_height) = font.text_height(str)
            max_tic_height = max(max_tic_height, total_height)

            canvas.line(self.line_style, ticx, y_base, ticx, y_base-self.tic_len)
            canvas.show(ticx+self.tic_label_offset[0], 
                        y_base-self.tic_len-base_height+self.tic_label_offset[1],
                        str)

        if self.minor_tic_interval:
            for i in ar.x_tic_points(self.minor_tic_interval):
                if tic_dic.has_key(i):
                    # a major tic was drawn already.
                    pass
                else:
                    ticx = ar.x_pos(i)
                    canvas.line(self.line_style, ticx, y_base, ticx,
                                y_base-self.minor_tic_len)

        if self.label != None:
            str = "/hC/vM" + self.label
            (label_height, base_height) = font.text_height(str)
            if self.label_offset[0] != None:
                xlabel = ar.loc[0] + self.label_offset[0]
            else:
                xlabel = ar.loc[0] + ar.size[0]/2.0
            if self.label_offset[1] != None:
                ylabel = y_base + self.label_offset[1]
            else:
                ylabel = y_base - self.tic_len - max_tic_height - 10
            canvas.show(xlabel, ylabel, str)

class Y(Base):
   __doc__ = axis_doc.doc_y   
   def draw(self, ar):
      self.type_check()
      self.tic_interval = self.tic_interval or ar.y_grid_interval
      x_base = ar.loc[0] + self.offset

      canvas.line(self.line_style, x_base, ar.loc[1],
                  x_base, ar.loc[1]+ar.size[1])
      
      xmin = x_base + ar.size[0] # somebigvalue
      tic_dic = {}
      for i in ar.y_tic_points(self.tic_interval):
         y_tic = ar.y_pos(i)
         tic_dic[i] = 1
         canvas.line(self.line_style, x_base, y_tic,
                     x_base - self.tic_len, y_tic)
         tic_label = pychart_util.apply_format(self.format, (i,), 0)
         x = x_base - self.tic_len + self.tic_label_offset[0]
         if self.tic_len > 0:
            tic_label = "/hR" + tic_label
            
         tic_height, base_height = font.text_height(tic_label)
         canvas.show(x, y_tic - tic_height/2.0 + self.tic_label_offset[1],
		     tic_label)
         xmin = min(xmin, x - font.text_width(tic_label))
      if self.minor_tic_interval:
         for i in ar.y_tic_points(self.minor_tic_interval):
            if tic_dic.has_key(i):
               # a major tic was drawn already.
               pass
            else:
               y_tic = ar.y_pos(i)
               canvas.line(self.line_style, x_base, y_tic,
                           x_base - self.minor_tic_len, y_tic)
               
      if self.label != None:
         xlabel = xmin - theme.default_font_size/2.0
         ylabel = ar.loc[1] + ar.size[1] / 2
         if self.label_offset[0] != None:
            xlabel = xlabel + self.label_offset[0]
         if self.label_offset[1] != None:
            ylabel = ylabel + self.label_offset[1]
         canvas.show(xlabel, ylabel, "/a90/hC" + self.label)
