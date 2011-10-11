import string
import copy

def __convert_item(v, typ, line):
    if typ == "a":
        try:
            i = string.atof(v)
        except ValueError: # non-number
            i = v
        return i
    elif typ == "d":
        try:
            return string.atoi(v)
        except ValueError:
            raise ValueError, "Can't convert %s to int line=%s" % (v, line)
    elif typ == "f":
        try:
            return string.atof(v)
        except ValueError:
            raise ValueError, "Can't convert %s to float line=%s" % (v, line)
    elif typ == "s":
        return v
    else:
        raise ValueError, "Unknown conversion type, type=%s, line=%s" % (typ,line)
        
def parse_line(line, delim):
    data = []
    if string.find(delim, "%") < 0:
        for item in string.split(line, delim):
            data.append(__convert_item(item, "a", line))
    else:
        id = 0 # indexes delim
        ch = 'f'
        sep = ','
        
        while id < len(delim):
            if delim[id] != '%':
                raise ValueError, "bad delimitor: '" + delim + "'"
            ch = delim[id+1]
            id = id + 2
            sep = ""
            while id < len(delim) and delim[id] != '%':
                sep = sep + delim[id]
                id = id + 1
            xx = string.split(line, sep, 1)
            data.append(__convert_item(xx[0], ch, line))
            if len(xx) >= 2:
                line = xx[1]
            else:
                line = ""
                break
                
        if line != "":
            for item in string.split(line, sep):
                data.append(__convert_item(item, ch, line))
    return data

def escape_string(str):
    return string.replace(str, "/", "//")

def extract_rows(data, *rows):
    """Extract rows specified in the argument list.

data2 = chart_data.extract_rows([[10,20], [30,40], [50,60]], 1, 2)
# data2 will become [[30,40],[50,60]]."""

    try:
        out = []
        for r in rows:
            out.append(data[r])
        return out
    except IndexError:
        raise IndexError, "data=%s rows=%s" % (data, rows)
    return out

def extract_columns(data, *cols):
    """Extract columns specified in the argument list.

data2 = chart_data.extract_columns([[10,20], [30,40], [50,60]], 0)
# data2 will become [[10],[30],[50]]."""

    out = []
    try:
        for r in data:
            col = []
            for c in cols:
                col.append(r[c])
            out.append(col)
    except IndexError:
        raise IndexError, "data=%s col=%s" % (data, col)        
    return out

def moving_average(data, xcol, ycol, width):
    """Compute the moving average of  YCOL'th column of each sample point
in  DATA. In particular, for each element  I in  DATA,
this function extracts up to  WIDTH*2+1 elements, consisting of
 I itself,  WIDTH elements before  I, and  WIDTH
elements after  I. It then computes the mean of the  YCOL'th
column of these elements, and it composes a two-element sample
consisting of  XCOL'th element and the mean.

data = [[10,20], [20,30], [30,50], [40,70], [50,5]]
data2 = chart_data.moving_average(data, 0, 1, 1)

In the above example, data2 will be computed as:

[(10, (20+30)/2), (20, (20+30+50)/3), (30, (30+50+70)/3), 
  (40, (50+70+5)/3), (50, (70+5)/2)]"""
    
    out = []
    try:
        for i in range(0, len(data)):
            n = 0
            total = 0
            for j in range(i-width, i+width+1):
                if j >= 0 and j < len(data):
                    total = total + data[j][ycol]
                    n = n + 1
            out.append((data[i][xcol], float(total) / n))
    except IndexError:
        raise IndexError, "bad data: %s,xcol=%d,ycol=%d,width=%d" % (data,xcol,ycol,width)
    
    return out
    
def filter(func, data):
    """FUNC must be a single-argument function that takes a sequence (i.e.,
a sample point) and returns a boolean. This procedure calls FUNC on
each element in DATA and returns a list comprising elements for
which FUNC returns true.

>>> data = [[1,5], [2,10], [3,13], [4,16]]
... chart_data.filter(lambda x: x[1] % 2 == 0, data)
[[2,10], [4,16]].
"""
    
    out = []
    for r in data:
	if func(r):
	    out.append(r)
    return out

def transform(func, data):
    """Apply FUNC on each element in DATA and return the list
consisting of the return values from FUNC.

data = [[10,20], [30,40], [50,60]]
data2 = chart_data.transform(lambda x: [x[0], x[1]+1], data)
# data2 will become [[10, 21], [30, 41], [50, 61]]."""
    out = []
    for r in data:
        out.append(func(r))
    return out

def aggregate_rows(data, col):
    out = copy.deepcopy(data)
    total = 0
    for r in out:
        total = total + r[col]
        r[col] = total
    return out

def empty_line_p(s):
    return string.strip(s) == ""

def fread_csv(fp, delim = ','):
    """This function is similar to read_csv, except that it reads from
    an open file handle FP.

fp = open("foo", "r")
data = chart_data.fread_csv(fp, ",") """
    
    data = []
    line = fp.readline()
    while line != "":
        if line[0] != '#' and not empty_line_p(line):
            data.append(parse_line(line, delim))
        line = fp.readline()
    return data

def read_csv(file, delim = ','):
    """This function reads
    comma-separated samples from FILE. Empty lines and lines
    beginning with "#" are ignored.  DELIM specifies how
    values in each line are separated. If it does not contain the
    letter "%", then DELIM is simply used to split each
    line into values. Otherwise, this function acts like scanf
    in C:

chart_data.read_csv("file", "%d,%s:%d")

    This function currently supports only three conversion specifiers:
    "d"(int), "f"(double), and "s"(string)."""
        
    f = open(file)
    data = fread_csv(f, delim)
    f.close()
    return data

def read_str(delim = ',', *lines):
    """This function is similar to read_csv, but it reads data from the
    list of LINES.

fp = open("foo", "r")
data = chart_data.read_str(",", fp.readlines())"""

    data = []
    for line in lines:
        com = parse_line(line, delim)
        data.append(com)
    return data
    
def func(f, xmin, xmax, step = None):
    """Create sample points from function F, which must be a
    single-parameter function that returns a number (e.g., math.sin).
    XMIN and XMAX specify the first and last X values, and
    STEP specfies the sampling interval.

sin_samples = chart_data.func(math.sin, 0, math.pi*4, 0.1)"""

    
    data = []
    x = xmin
    if not step:
        step = (xmax - xmin) / 100.0
    while x < xmax:
        data.append((x, f(x)))
        x = x + step
    return data

def __nr_data(data, col):
    nr_data = 0
    for d in data:
        nr_data = nr_data + d[col]
    return nr_data
    
def median(data, freq_col=1):
    """Compute the median of the COL'th column of the values is DATA.
    For example, chart_data.median([(10,20), (20,4), (30,5)], 0) returns 20.
    chart_data.median([(10,20), (20,4), (30,5)], 1) returns 5.
    """
    
    nr_data = __nr_data(data, freq_col)
    median_idx = nr_data / 2
    i = 0
    for d in data:
        i = i + d[freq_col]
        if i >= median_idx:
            return d
    raise Exception, "??? median ???"

def cut_extremes(data, cutoff_percentage, freq_col=1):
    nr_data = __nr_data(data, freq_col)
    min_idx = nr_data * cutoff_percentage / 100.0
    max_idx = nr_data * (100 - cutoff_percentage) / 100.0
    r = []
    
    i = 0
    for d in data:
        if i < min_idx:
            if i + d[freq_col] >= min_idx:
                x = copy.deepcopy(d)
                x[freq_col] = x[freq_col] - (min_idx - i)
                r.append(x)
            i = i + d[freq_col]
            continue
	elif i + d[freq_col] >= max_idx:
            if i < max_idx and i + d[freq_col] >= max_idx:
                x = copy.deepcopy(d)
                x[freq_col] = x[freq_col] - (max_idx - i)
                r.append(x)
            break
        i = i + d[freq_col]
        r.append(d)
    return r

def mean(data, val_col, freq_col):
    nr_data = 0
    sum = 0
    for d in data:
        sum = sum + d[val_col] * d[freq_col]
        nr_data = nr_data + d[freq_col]
    if nr_data == 0:
	raise IndexError, "data is empty"

    return sum / float(nr_data)
