import os
import gs_frontend
import theme
import sys

class T(gs_frontend.T):
    def close(self, out_fname):
        self.start_gs("-sDEVICE=x11")
        sys.stdin.readline()
        self.close_gs()

