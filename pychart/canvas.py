# -*- python -*-
import traceback
import font
import line_style
import color
import fill_style
import pychart_util
import string
import re
import pdf_lib
import ps_lib
import png_lib
import x11_lib
import os
import math
import theme
import sys
from scaling import *

__doc__ = """A collection of device-independent drawing procedures.

Canvas is an internal component of pychart that provides
device-independent drawing procedures.  Each canvas corresponds to a
single (eps or pdf) file.  The default canvas, created when pychart
starts up, is written to stdout or wherever specified by the "output="
option. You can create additional canvases by calling
canvas.init(fname) procedure. Only one canvas can be active at a time,
and all drawing procedures will output to that canvas. Calling
canvas.init() will automatically close the current canvas before
opening the new one.

"""

invalid_coord = -99999999 
__xmax = -9999999
__xmin = 9999999
__ymax = -9999999
__ymin = 9999999
__clip_box = (-99999, -99999, 99999, 99999)
__clip_stack = []
__nr_gsave = 0
__out_fname = None
_oldexitfunc = None
out = None

def close():
    """Close the current canvas and the corresponding output file, if any."""
    global out, __out_fname
    if out == None:
        return

    out.close(__out_fname)
    out = None

def _exit():
    global _oldexitfunc
    close()
    if _oldexitfunc:
        foo = _oldexitfunc
        _oldexitfunc = None
        foo()
        
def init(fname):

    """Open a new canvas. Close the existing canvas, if any.
    Parameter ``fname`` specifies the file to which the contents of
    the canvas will be dumped when it closes.  The format of the file
    is determined by variable ``theme.output_format``, or if it's
    None, by ``fname``'s suffix -- i.e., PDF if the file name ends
    with ``.pdf``, PNG if the file name ends with ``.png``, and
    Encapsulated PS otherwise.  """
    
    global __xmax, __xmin, __ymax, __ymin, __clip_box, __clip_stack
    global __nr_gsave, __out_fname
    global out, _oldexitfunc

    if out:
        close()
        
    __xmax = -99999999
    __xmin = 99999999
    __ymax = -99999999
    __ymin = 99999999
    __clip_box = (-99999, -99999, 99999, 99999)
    __clip_stack = []
    __nr_gsave = 0
    __out_fname = fname or theme.output_file

    format = theme.output_format
    
    if format == None:
        if re.search("pdf$", __out_fname):
            format = "pdf"
        elif re.search("png$", __out_fname):
            format = "png"
        else:
            format = "ps"

    if format == "ps":
        out = ps_lib.T()
    elif format == "png":
        out = png_lib.T()
    elif format == "x11":
        out = x11_lib.T()
    else:
        out = pdf_lib.T(theme.compress_output)

    if not vars(sys).has_key("exitfunc"):
        sys.exitfunc = _exit
    elif sys.exitfunc != _exit:
        _oldexitfunc = sys.exitfunc
        sys.exitfunc = _exit

def _compute_bounding_box(points):
    """Given the list of coordinates (x,y), this procedure computes
    the smallest rectangle that covers all the points."""
    (xmin, ymin, xmax, ymax) = (99999999, 99999999, -99999999, -99999999)
    for p in points:
        xmin = min(xmin, p[0])
	xmax = max(xmax, p[0])
	ymin = min(ymin, p[1])
	ymax = max(ymax, p[1])
    return (xmin, ymin, xmax, ymax)

def _intersect_box(b1, b2):
    xmin = max(b1[0], b2[0])
    ymin = max(b1[1], b2[1])
    xmax = min(b1[2], b2[2])
    ymax = min(b1[3], b2[3])
    return (xmin, ymin, xmax, ymax)

def setbb(x, y):
    global __xmin, __xmax, __ymin, __ymax, __clip_box
    __xmin = min(__xmin, max(x, __clip_box[0]))
    __xmax = max(__xmax, min(x, __clip_box[2]))
    __ymin = min(__ymin, max(y, __clip_box[1]))
    __ymax = max(__ymax, min(y, __clip_box[3]))
    out.setbb(xscale(__xmin),xscale(__ymin),
              xscale(__xmax), xscale(__ymax))

def invisible_p(x, y):
    """Return true if the point (X, Y) is visible in the canvas."""
    if x < -49999999 or y < -49999999:
        return 1
    return 0

def fill_with_pattern(pat, x1, y1, x2, y2):
    if invisible_p(x2, y2):
        return
	
    out.comment("FILL pat=%s (%d %d)-(%d %d)\n" % (pat, x1, y1, x2, y2))
    out.set_fill_color(pat.bgcolor)
    __path_polygon([(x1, y1), (x1, y2), (x2, y2), (x2, y1)])
    out.fill()
    pat.draw(x1, y1, x2, y2)
	
    x1 = xscale(x1)
    x2 = xscale(x2)
    y1 = yscale(y1)
    y2 = yscale(y2)
	
    out.comment("end FILL.\n")

def __path_polygon(points):
    (xmin, ymin, xmax, ymax) = _compute_bounding_box(points)
    if invisible_p(xmax, ymax):
        return
	
    setbb(xmin, ymin)
    setbb(xmax, ymax)
    out.polygon(map(lambda p: (xscale(p[0]), yscale(p[1])), points))

def polygon(edge_style, pat, points, shadow = None):

    """Draw a polygon with EDGE_STYLE, fill with PAT, and the edges
    POINTS. POINTS is a sequence of coordinates, e.g., ((10,10), (15,5),
    (20,8)). SHADOW is either None or a tuple (XDELTA, YDELTA,
    fillstyle). If non-null, a shadow of FILLSTYLE is drawn beneath
    the polygon at the offset of (XDELTA, YDELTA)."""

    if pat:
        out.comment("POLYGON points=[%s] pat=[%s]"
                    % (str(points), str(pat)))
        (xmin, ymin, xmax, ymax) = _compute_bounding_box(points)
		
        if shadow:
            x_off, y_off, shadow_pat = shadow
            out.gsave()
            __path_polygon(map(lambda p,x_off=x_off,y_off=y_off: (p[0]+x_off, p[1]+y_off), points))
            out.clip()
            fill_with_pattern(shadow_pat, xmin+x_off, ymin+y_off,
                              xmax+x_off, ymax+y_off)
            out.grestore()
									  
        out.gsave();
        __path_polygon(points)
        out.clip()
        (xmin, ymin, xmax, ymax) = _compute_bounding_box(points)
        fill_with_pattern(pat, xmin, ymin, xmax, ymax)
        out.grestore()
    if edge_style:
        out.comment("POLYGON points=[%s] edge=[%s]"
                    % (str(points), str(edge_style)))
        out.set_line_style(edge_style)
        __path_polygon(points)
        out.stroke()
		
def rectangle(edge_style, pat, x1, y1, x2, y2, shadow = None): 
    """Draw
    a rectangle with EDGE_STYLE, fill with PAT, and the bounding box
    (X1, Y1, X2, Y2).  SHADOW is either None or a tuple (XDELTA,
    YDELTA, fillstyle). If non-null, a shadow of FILLSTYLE is drawn
    beneath the polygon at the offset of (XDELTA, YDELTA)."""
    polygon(edge_style, pat, [(x1,y1), (x1,y2), (x2,y2), (x2, y1)], shadow)

def to_radian(deg):
    return deg*2*math.pi / 360.0

def __path_ellipsis(x, y, radius, ratio, start_angle, end_angle):
    oradius = nscale(radius)
    centerx, centery = xscale(x), yscale(y)
    startx, starty = centerx+oradius * math.cos(to_radian(start_angle)), \
                     centery+oradius * math.sin(to_radian(start_angle))
    out.moveto(centerx, centery)
    if start_angle % 360 != end_angle % 360:
        out.moveto(centerx, centery)
        out.lineto(startx, starty)
    else:
        out.moveto(startx, starty)
    out.path_arc(xscale(x), yscale(y), nscale(radius),
                 ratio, start_angle, end_angle)
    out.closepath()

def ellipsis(line_style, pattern, x, y, radius, ratio = 1.0,
             start_angle=0, end_angle=360, shadow=None):
    """Draw an ellipsis with line_style and fill PATTERN. The center is \
    (X, Y), X radius is RADIUS, and Y radius is RADIUS*RATIO, whose \
    default value is 1.0. SHADOW is either None or a tuple (XDELTA,
    YDELTA, fillstyle). If non-null, a shadow of FILLSTYLE is drawn
    beneath the polygon at the offset of (XDELTA, YDELTA)."""

    if invisible_p(x + radius, y + radius*ratio):
        return
	
    setbb(x - radius, y - radius*ratio)
    setbb(x + radius, y + radius*ratio)

    if pattern:
        if shadow:
            x_off, y_off, shadow_pat = shadow
            out.gsave()
            out.newpath()
            __path_ellipsis(x+x_off, y+y_off, radius, ratio,
                            start_angle, end_angle)
            out.clip()
            fill_with_pattern(shadow_pat,
                              x-radius*2+x_off, y-radius*ratio*2+y_off,
                              x+radius*2+x_off, y+radius*ratio*2+y_off)
            out.grestore()
        out.gsave()
        out.newpath()		
        __path_ellipsis(x, y, radius, ratio, start_angle, end_angle)
        out.clip()
        fill_with_pattern(pattern,
                          (x-radius*2), (y-radius*ratio*2),
                          (x+radius*2), (y+radius*ratio*2))
        out.grestore()
    if line_style:
        out.set_line_style(line_style)
        out.newpath()
        __path_ellipsis(x, y, radius, ratio, start_angle, end_angle)
        out.stroke()

def clip_ellipsis(x, y, radius, ratio = 1.0):
    """Create an elliptical clip region. You must call endclip() after
    you completed drawing. See also the ellipsis method."""
    
    global __clip_stack, __clip_box
    out.gsave()
    out.newpath()
    out.moveto(xscale(x)+nscale(radius), yscale(y))
    out.path_arc(xscale(x), yscale(y), nscale(radius), ratio, 0, 360)
    out.closepath()
    __clip_stack.append(__clip_box)
    out.clip()
	
def clip_polygon(points):
    """Create a polygon clip region. You must call endclip() after
    you completed drawing. See also the polygon method."""
    global __clip_stack, __clip_box
    out.gsave()
    __path_polygon(points)
    __clip_stack.append(__clip_box)
    __clip_box = _intersect_box(__clip_box, _compute_bounding_box(points))
    out.clip()
		
def clip(x1, y1, x2, y2):
    
    """Activate a rectangular clip region, (X1, Y1) - (X2, Y2).
    You must call endclip() after you completed drawing.

canvas.clip(x,y,x2,y2)
draw something ...
canvas.endclip()
    """
    
    global __clip_stack, __clip_box
    __clip_stack.append(__clip_box)
    __clip_box = _intersect_box(__clip_box, (x1, y1, x2, y2))
    out.gsave()
    out.newpath()
    out.moveto(xscale(x1), yscale(y1))
    out.lineto(xscale(x1), yscale(y2))
    out.lineto(xscale(x2), yscale(y2))
    out.lineto(xscale(x2), yscale(y1))
    out.closepath()
    out.clip()
	
def endclip():
    global __clip_stack, __clip_box
    __clip_box = __clip_stack[-1]
    del __clip_stack[-1]
    out.grestore()

def midpoint(p1, p2):
    return ( (p1[0]+p2[0])/2.0, (p1[1]+p2[1])/2.0 )

def curve(style, points):
    for p in points:
        setbb(p[0], p[1])
    out.newpath()
    out.set_line_style(style)
    out.moveto(xscale(points[0][0]), xscale(points[0][1]))
    i = 1
    n = 1
    while i < len(points):
        if n == 1:
            x2 = points[i]
            n = n + 1
        elif n == 2:
            x3 = points[i]
            n = n + 1
        elif n == 3:
            x4 = midpoint(x3, points[i])
            out.curveto(xscale(x2[0]), xscale(x2[1]),
                        xscale(x3[0]), xscale(x3[1]),
                        xscale(x4[0]), xscale(x4[1]))
            n = 1
        i = i+1
	if n == 1:
            pass
	if n == 2:
            out.lineto(xscale(x2[0]), xscale(x2[1]))
	if n == 3:
            out.curveto(xscale(x2[0]), xscale(x2[1]),
                        xscale(x2[0]), xscale(x2[1]),
                        xscale(x3[0]), xscale(x3[1]))
        out.stroke()
		
def line(style, x1, y1, x2, y2):
    if not style:
        return
    if invisible_p(x2, y2) and invisible_p(x1, y1):
        return
		
    setbb(x1, y1)
    setbb(x2, y2)
	
    out.newpath()
    out.set_line_style(style)
    out.moveto(xscale(x1), yscale(y1))
    out.lineto(xscale(x2), yscale(y2))
    out.stroke()

def lines(style, segments):
    if not style:
        return
    (xmin, ymin, xmax, ymax) = _compute_bounding_box(segments)
    if invisible_p(xmax, ymax):
        return
	
    setbb(xmin, ymin)
    setbb(xmax, ymax)
    out.newpath()
    out.set_line_style(style)
    out.moveto(xscale(segments[0][0]), xscale(segments[0][1]))
    i = 1
    while i < len(segments):
        out.lineto(xscale(segments[i][0]), yscale(segments[i][1]))
        i = i + 1
    out.stroke()

def __path_round_rectangle(x1, y1, x2, y2, radius):
    out.moveto(xscale(x1 + radius), yscale(y1))
    out.lineto(xscale(x2 - radius), yscale(y1))
    out.path_arc(xscale(x2-radius), yscale(y1+radius), nscale(radius), 1, 270, 360)
    out.lineto(xscale(x2), yscale(y2-radius))
    out.path_arc(xscale(x2-radius), yscale(y2-radius), nscale(radius), 1, 0, 90)
    out.lineto(xscale(x1+radius), yscale(y2))
    out.path_arc(xscale(x1 + radius), yscale(y2 - radius), nscale(radius), 1, 90, 180)
    out.lineto(xscale(x1), xscale(y1+radius))
    out.path_arc(xscale(x1 + radius), yscale(y1 + radius), nscale(radius), 1, 180, 270)
	
def round_rectangle(style, fill, x1, y1, x2, y2, radius, shadow=None):

    """Draw a rectangle with rounded four corners."""
    
    if invisible_p(x2, y2):
        return
    setbb(x1, y1)
    setbb(x2, y2)

    if fill:
        if shadow:
            x_off, y_off, shadow_fill = shadow
            out.gsave();
            out.newpath()
            __path_round_rectangle(x1+x_off, y1+y_off, x2+x_off, y2+y_off,
                                   radius)
            out.closepath()
            out.clip()
            fill_with_pattern(shadow_fill, x1+x_off, y1+y_off,
                              x2+x_off, y2+y_off)
            out.grestore()
			
	out.gsave();
        out.newpath()
        __path_round_rectangle(x1, y1, x2, y2, radius)
        out.closepath()
        out.clip()
        fill_with_pattern(fill, x1, y1, x2, y2)
        out.grestore()
    if style:
        out.set_line_style(style)
        out.newpath()
        __path_round_rectangle(x1, y1, x2, y2, radius)
        out.closepath()
        out.stroke()

def show(x, y, str):
    global out
    y_org = y
    org_str = str

    if invisible_p(x, y):
        return

    (xmin, xmax, ymin, ymax) = font.get_dimension(str)
	
    # rectangle(line_style.default, None, x+xmin, y+ymin, x+xmax, y+ymax)
    # ellipsis(line_style.default, None, x, y, 1)
    setbb(x+xmin, y+ymin)
    setbb(x+xmax, y+ymax)
	
    (halign, valign, angle) = font.get_align(str)

    base_x = x
    base_y = y

    # Handle vertical alignment
    if valign == "B":
        y = font.unaligned_text_height(str)
    elif valign == "T":
        y = 0
    elif valign == "M":
        y = font.unaligned_text_height(str) / 2.0
        
    (xmin, xmax, ymin, ymax) = font.get_dimension(org_str)
    # print org_str, xmin, xmax, ymin, ymax, x, y_org, y
    setbb(x+xmin, y_org+y+ymin)
    setbb(x+xmax, y_org+y+ymax)
    
    itr = font.text_iterator(None)
    
    max_width = 0
    
    lines = []
    for line in string.split(str, '\n'):
        cur_width = 0
        cur_height = 0
		
        itr.reset(line)
        
        strs = []
        
        while 1:
            elem = itr.next()
            if not elem:
                break
			
            (font_name, size, line_height, color, _h, _v, _a, str) = elem
            cur_width = cur_width + font.line_width(font_name, size, str)
            max_width = max(cur_width, max_width)
            cur_height = max(cur_height, line_height)
            
            # replace '(' -> '\(', ')' -> '\)' to make
            # Postscript string parser happy.
            str = string.replace(str, "(", "\\(")
            str = string.replace(str, ")", "\\)")
            strs.append((font_name, size, color, str))
        lines.append((cur_width, cur_height, strs))
		
    for line in lines:
        cur_width, cur_height, strs = line
        cur_y = y - cur_height
        y = y - cur_height
        out.comment("cury: %d hei %d str %s\n" % (cur_y, cur_height, strs))
        if halign == 'C':
            cur_x = -cur_width/2.0
        elif halign == 'R':
            cur_x = -cur_width
        else:
            cur_x = 0

	rel_x, rel_y = pychart_util.rotate(cur_x, cur_y, angle)
        out.text_begin()
        out.text_moveto(xscale(base_x + rel_x),
                        yscale(base_y + rel_y), angle)
        for segment in strs:
            font_name, size, color, str = segment
            out.text_show(font_name, nscale(size), color, str)
        out.text_end()
	
		
def verbatim(str):
    "Add STR to the output file verbatim." 
    out.verbatim(str)
def comment(str):
    "Add STR as a comment to the output file."
    out.comment(str)
	
init(None)
theme.add_reinitialization_hook(lambda: init(None))
