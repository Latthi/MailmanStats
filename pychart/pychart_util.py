import sys
import math
import types
import traceback

AnyType = 9998
NumType = 9999

def inch_to_point(inch):
    return inch * 72.0
def point_to_inch(pt):
    return float(pt) / 72.0

def rotate(x, y, degree):
    radian = float(degree) * 2 * math.pi / 360.0
    newx = math.cos(radian) * x - math.sin(radian) * y
    newy = math.sin(radian) * x + math.cos(radian) * y
    return (newx, newy)

debug_level = 1
error_happened = 0

def warn(*strs):
    for s in strs:
        sys.stderr.write(str(s))
        sys.stderr.write(" ")
    sys.stderr.write("\n")

def info(*strs):
    if debug_level < 100:
	return
    for s in strs:
        sys.stderr.write(str(s))
    sys.stderr.write("\n")

def check_data_integrity(self, data, cols):
    col = max(cols)
    for item in data:
        if len(item) <= col:
            raise IndexError, "No %dth column in data %s given to %s" \
                  % (col, item, str(self))
        
def get_data_range(data, col):
    data = map(lambda pair, col=col: pair[col], data)
    for item in data:
	if type(item) not in (types.IntType, types.FloatType):
            raise TypeError, "Non-number passed to data: %s" % (data)
    return (min(data), max(data))

def round_down(val, bound):
    return int(val/float(bound)) * bound

def round_up(val, bound):
    return (int((val-1)/float(bound))+1) * bound


#
# Attribute type checking stuff
#

def new_list():
    return []

def union_dict(dict1, dict2):
    dict = {}
    for attr, val in dict1.items():
        dict[attr] = val
    for attr, val in dict2.items():
        dict[attr] = val
    return dict

def TextVAlignType(val):
    if val == 'T' or val == 'B' or val == 'M' or val == None:
        return ""
    return "Text vertical alignment must be one of T(op), B(ottom), or M(iddle).\n"

def TextAlignType(val):
    if val == 'C' or val == 'R' or val == 'L' or val == None:
        return ""
    return "Text horizontal alignment must be one of C(enter), R(ight), or L(eft)."

def FormatType(val):
    if type(val) == types.StringType:
        return ""
    if type(val) == types.FunctionType:
        return ""
    return "Format must be a string or a function"

def apply_format(format, val, defaultidx):
    if type(format) == types.StringType:
        return format % val[defaultidx]
    else:
        return apply(format, val)

def NumType(val):
   if type(val) == types.IntType or type(val) == types.FloatType:
       return ""
   else:
       return "Expecting a number, found \"" + str(val) + "\""

def ShadowType(val):
    if type(val) != types.TupleType and type(val) != types.ListType:
	return "Expecting tuple or list."
    if len(val) != 3:
	return "Expecting (xoff, yoff, fill)."
    return ""
    
def CoordType(val):
    if type(val) != types.TupleType and type(val) != types.ListType:
        return (" not a valid coordinate.")
    if len(val) != 2:
        return "Coordinate must be a pair of numbers.\n"
    error = NumType(val[0])
    if val[0] != None and error != "":
        return error
    error = NumType(val[1])
    if val[1] != None and error != "":
        return error
    return ""

def IntervalType(val):
    if NumType(val) == "":
	return ""
    if type(val) == types.FunctionType:
	return ""
    return "Expecting a number or a function"

def CoordOrNoneType(val):
    if type(val) != types.TupleType and type(val) != types.ListType:
        return "Expecting a tuple or a list."
    if len(val) != 2:
        return "Coordinate must be a pair of numbers.\n"
    error = NumType(val[0])
    if val[0] != None and error != "":
        return error
    error = NumType(val[1])
    if val[1] != None and error != "":
        return error
    return ""
    
data_desc = "Specifies the data points. <<chart_data>>"
label_desc = "The label to be displayed in the legend. <<legend>>, <<font>>"
xcol_desc = """The column, within "data", from which the X values of sample points are extracted. <<chart_data>>"""
ycol_desc = """The column, within "data", from which the Y values of sample points are extracted. <<chart_data>>"""
tick_mark_desc = "Tick marks to be displayed at each sample point."
line_desc="The style of the line. "

def interval_desc(w):
    return "When the value is a number, it specifies the interval with which %s are drawn. Otherwise, the value must be a function. It must take no argument and return the list of numbers, which specifies the X or Y points where %s are drawn." % (w,w)

shadow_desc = """The value is either None or a tuple. When non-None,
a drop-shadow is drawn beneath the object. X-off, and y-off specifies the
offset of the shadow relative to the object, and fill specifies the
style of the shadow (@pxref{fill_style})."""

string_desc = """The appearance of the string produced here can be
controlled using escape sequences. <<font>>"""

#
#

class symbol_lookup_table:
    def __init__(self, dict, objs):
        self.names = {}
        for name, val in dict.items():
            for obj in objs.list():
                if val == obj:
                    self.names[val] = name
                    break
    def lookup(self, obj):
        if self.names.has_key(obj):
            return self.names[obj]
        return None
