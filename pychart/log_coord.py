import coord
import math

class T(coord.T):
    def get_canvas_pos(self, size, val, min, max):
        if val <= 0:
            return 0
        xminl = math.log(min)
        xmaxl = math.log(max)
        vl = math.log(val)
        return size * (vl-xminl) / float(xmaxl-xminl)
    def get_tics(self, min, max, interval):
        "Generate the list of places for drawing tick marks."
        v = []
        x = min
        while x <= max:
            v.append(x)
            x = x * interval
        return v
    def get_min_max(self, dmin, dmax, interval):
        if not interval:
            interval = 10
        if dmin <= 0:
            # we can't have a negative value with a log scale.
            dmin = 1
        v = 1.0
        while v > dmin:
            v = v / interval
        dmin = v
        v = 1.0
        while v < dmax:
            v = v * interval
        dmax = v

        return dmin, dmax, interval
    
