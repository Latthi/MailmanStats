import coord
import math
import pychart_util

class T(coord.T):
    def get_canvas_pos(self, size, val, min, max):
        return size * (val - min) / float(max - min)

    def get_tics(self, min, max, interval):
        v = []
        x = min
        while x <= max:
            v.append(x)
            x = x + interval
        return v
    def get_min_max(self, dmin, dmax, interval):
        if not interval:
            if dmax == dmin:
                interval = 10
            else:
                interval = 10 ** (float(int(math.log(dmax-dmin)/math.log(10))))
        dmin = min(dmin, pychart_util.round_down(dmin, interval))
        dmax = max(dmax, pychart_util.round_up(dmax, interval) + interval/2.0)
        return dmin, dmax, interval
