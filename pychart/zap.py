import fill_style
import line_style
import canvas
import copy
import pychart_util

def __draw_zap(p1, p2, style, pat):
    x = copy.deepcopy(p1)
    x.extend(p2)
    canvas.polygon(None, pat, x)
    canvas.lines(style, p1)
    canvas.lines(style, p2)
    

def zap_horizontally(style, pat, x1, y1, x2, y2, xsize, ysize):
    """Draw a horizontal "zapping" symbol on the canvas that shows
    that a graph is ripped in the middle.

    STYLE specifies the style for the zig-zag lines.
    PAT specifies the pattern with which the area is filled.
    The symbol is drawn in the rectangle (X1, Y1) - (X2, Y2).
    Each "zigzag" has the width XSIZE, height YSIZE."""

    assert isinstance(style, line_style.T)
    assert isinstance(pat, fill_style.T)

    points = []
    points2 = []
    x = x1
    y = y1
    while x < x2:
        points.append((x, y))
        points2.append((x, y + (y2-y1)))
        x = x + xsize
        if y == y1:
            y = y + ysize
        else:
            y = y - ysize

    points2.reverse()
    __draw_zap(points, points2, style, pat)

def zap_vertically(style, pat, x1, y1, x2, y2, xsize, ysize):
    """Draw a vertical "zapping" symbol on the canvas that shows
    that a graph is ripped in the middle.

    STYLE specifies the style for the zig-zag lines.
    PAT specifies the pattern with which the area is filled.
    The symbol is drawn in the rectangle (X1, Y1) - (X2, Y2).
    Each "zigzag" has the width XSIZE, height YSIZE."""
    
    points = []
    points2 = []
    x = x1
    y = y1
    while y < y2:
        points.append((x, y))
        points2.append((x + (x2-x1), y))
        y = y + ysize
        if x == x1:
            x = x + xsize
        else:
            x = x - xsize

    points2.reverse()
    __draw_zap(points, points2, style, pat)

