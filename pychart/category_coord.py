import coord
import canvas

class T(coord.T):
    def __init__(self, data, col):

        """This attribute is meaningful only when x_coord_system ==
        'category'. This attribute selects the column of
        'x_category_data' from which X values are computed.
        Meaningful only when x_coord_system == 'category'.  This
        attribute specifies the data-set from which the X values are
        extracted. See also x_category_col."""
        
        self.data = data
        self.col = col
        
    def get_canvas_pos(self, size, val, min, max):
        i = 0.5
        for v in self.data:
            if v[self.col] == val:
                return size * i / float(len(self.data))
            i = i + 1
        # the drawing area is clipped. So negative offset will make this plot
        # invisible.
        return canvas.invalid_coord;
    def get_tics(self, min, max, interval):
        return map(lambda pair, col=self.col: pair[col], self.data)
