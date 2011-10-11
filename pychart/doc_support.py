import string
import sys
import types
import re
import os.path
from pychart import *

oldstdout = sys.stdout
if os.path.exists("/dev/null"):
    sys.stdout = open("/dev/null", "w")

modules = {}
values = []

sys.stdout = oldstdout
g = globals()
for mod in g.keys():
    val = g[mod]
    if type(val) == types.ModuleType:
        dic = {}
        modules[mod] = dic
        for name in val.__dict__.keys():
            v = val.__dict__[name]
            if name[0] != '_':
                values.append((v, mod + "." + name))
            if type(v) == types.ClassType and issubclass(v, chart_object.T):
                dic[name] = v

def stringify_type(t):
    s = str(t)
    if t == pychart_util.AnyType:
        return "any"
    if t == pychart_util.ShadowType:
        return "(xoff,yoff,fill)"
    elif re.search("NumType", s):    
        return "number"
    elif re.search("CoordType", s):
        return "(x,y)"
    elif re.search("CoordSystemType", s):
        return "['linear'|'log'|'category']"
    elif re.search("CoordOrNoneType", s):
        return "(x,y) or None"
    elif re.search("TextAlignType", s):
        return "['R'|'L'|'C'|None]"
    elif re.search("FormatType", s):
        return "printf format string"
    elif re.search("IntervalType", s):
        return "Number or function"
    #print "NOMATCH: ", area.CoordSystemType, t
    mo= re.match("<type '([^']+)'>", s)
    if mo:
        s = mo.group(1)
    mo = re.match("pychart\\.(.*)", s)
    if mo:
        s = mo.group(1)
    return s

def stringify_value(val):
    t = type(val)
    if t == types.StringType:
        return '"' + val + '"'
    if t == types.IntType or t == types.LongType or t == types.FloatType:
        return str(val)
    if val == None:
        return "None"
    if type(val) == types.ListType:
        return map(stringify_value, val)
    for pair in values:
        if pair[0] == val:
            return pair[1]
    return str(val)

def break_string(name):
    if len(name) < 8:
        return name
    
    name = re.sub("(\\d\\d)([^\\d])", "\\1-\n\\2", name) 
    name = re.sub("black(.)", "black-\n\\1", name)

    elems = string.split(name, "\n")
    while 1:
        broken = 0
        for i in range(len(elems)):
            elem = elems[i]
            if len(elem) < 8:
                continue
            broken = 1
            elem1 = elem[0:len(elem)/2]
            elem2 = elem[len(elem)/2:]
            elems[i:i+1] = [elem1, elem2]
            break
        if not broken:
            break
    name = string.join(elems, "\n")
    return name
