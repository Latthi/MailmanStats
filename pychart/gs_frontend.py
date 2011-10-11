import pychart_util
import sys
import os
import os.path
import ps_lib
import tempfile
import string

def get_gs_path():
    """Guess where the Ghostscript executable is
    and return its absolute path name."""
    path = os.defpath
    if os.environ.has_key("PATH"):
        path = os.environ["PATH"]
    for dir in string.split(path, os.pathsep):
        for name in ("gs", "gs.exe", "gswin32.exe"):
            g = os.path.join(dir, name)
            if os.path.exists(g):
                return g
    raise Exception, "Ghostscript not found."

class T(ps_lib.T):
    def __write_contents(self, fp):
        fp.write(ps_lib.preamble_text)
        for name, id in self.__font_ids.items():
            fp.write("/%s {/%s findfont SF} def\n" % (id, name))
        fp.write("%d %d translate\n" % (-self.__xmin + 3, -self.__ymin + 3))
        fp.writelines(self.__output_lines)
        fp.write("showpage end\n")
        fp.flush()
        
    def start_gs(self, arg):
        gs_path = get_gs_path()
        self.pipe_fp = None
	if self.__output_lines == []:
	    return
        
        if sys.platform != "win32" and hasattr(os, "popen"):
            cmdline = "%s -q %s -g%dx%d -q >/dev/null 2>&1" % (gs_path, arg, self.__xmax-self.__xmin + 6, self.__ymax - self.__ymin + 6)
            self.pipe_fp = os.popen(cmdline, "w")
            self.__write_contents(self.pipe_fp)
        else:
            fname = tempfile.mktemp()
            fp = open(fname, "wb")
            self.__write_contents(fp)
            fp.close()
            cmdline = "%s -q %s -g%dx%d -q %s <NUL" % (gs_path, arg, self.__xmax-self.__xmin + 6, self.__ymax - self.__ymin + 6, fname)
            os.system(cmdline)
            os.unlink(fname)
    def close_gs(self):
        if self.pipe_fp:
            self.pipe_fp.close()
            self.pipe_fp = None
