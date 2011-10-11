import os
import gs_frontend
import theme

class T(gs_frontend.T):
    def close(self, out_fname):
	if self.__output_lines == []:
	    return

        if theme.use_color:
            gs_args = "-sDEVICE=png256 -q -dNOPAUSE"
        else:
            gs_args = "-sDEVICE=pnggray -q -dNOPAUSE"
        
        if out_fname:
            gs_args = gs_args + " -sOutputFile=%s" % out_fname
        else:
            raise Exception, "PNG file cannot be sent to stdout. (due to some arcane problem regarding ghostscript interaction."
            #dev = dev + " -sOutputFile=-"
            
        self.start_gs(gs_args)
        self.close_gs()

