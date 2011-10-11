import sys
import os
import string
import re
import getopt

__doc__ = """This module is defines variables for changing the default
behavior of charts. All the variables can be changed either via
environment variable PYCHART_OPTIONS or via the command-line options.

The value of PYCHART_OPTIONS should be a sequence of var=val separated
by space.  Below is an example, which tells Pychart to write to file
foo.pdf and use Times-Roman as the default font.

PYCHART_OPTIONS="output=foo.pdf font-family=Times"

The summary of attributes that can be set via PYCHART_OPTIONS follows:

output=FILENAME (default: stdout)

    Set the output file name.
    
format=[ps|pdf|pdf-uncompressed|png|x11] (default: ps)

    Set the output file format.
    
font-family=NAME (default: Helvetica)

    Set the default font to be used by texts.
    
font-size=N (default: 9)

    Set the default font to be used by texts.
line-width=X (default: 0.4)

    Set the default line width, in points.  See also
    pychart.line_style.

scale=X (default: 1.0)

    Set the scaling factor.  The default is 1.0. 

color=[yes|no] (default: no)

    If yes, Pychart colorizes default object attributes.

font-dump-dir=PATH (default: ~/.pychart-)

    This option changes the path prefix of files to which font metrics
    information is dumped. This information is generated and dumped
    internally by PyChart from Ghostscript files to speed up the
    computation of font metrics. By default, the path prefix is
    `~/.pychart-'; that is, PyChart dumps the information in
    `~/.pychart-XXX, where XXX is the font name (e.g.,
    Helvetica).  It might be useful, for example, when you are
    running PyChart as a CGI script.

You can also set these variables by calling theme.get_options.
"""

use_color=0
scale_factor = 1
output_format = None   # "ps", "pdf", "png", or "x11"
compress_output = 1
output_file = ""

font_dump_dir = None
default_font_family = "Helvetica"
default_font_size = 9
default_line_height = None
default_font_halign = "L"
default_font_valign = "B"
default_font_angle = 0
default_line_width = 0.4

debug_level = 1

def parse_yesno(str):
    if str in ("yes", "true", "1"):
        return 1
    else:
        return 0
    
def parse_option(opt, arg):
    global use_color, scale_factor, font_dump_dir
    global output_format, output_file, compress_output
    global default_font_family, default_font_size
    global default_line_height
    global default_line_width, debug_level
    if opt == "format":
        if arg in ("ps", "eps"):
            output_format = "ps"
        elif arg == "png":
            output_format = "png"
        elif arg == "x11":
            output_format = "x11"
        elif arg == "pdf-uncompressed":
            output_format = "pdf"
            compress_output = 0
        elif arg in ("pdf-compressed", "pdf"):
            output_format = "pdf"
            compress_output = 1
        else:
            raise ValueError, "Unknown output option: " + str(arg)
    elif opt == "output":
        output_file = arg
    elif opt == "color":
        use_color = 1
    elif opt == "scale":
        scale_factor = float(arg)
    elif opt == "font-family":
        default_font_family = arg
    elif opt == "font-size":
        default_font_size = int(arg)
        default_line_height = int(arg)            
    elif opt == "line-width":
        default_line_width = int(arg)
    elif opt == "debug-level":
        debug_level = int(arg)
    elif opt == "font-dump-dir":
        font_dump_dir = arg
    else:
        raise getopt.GetoptError, "Unknown option: " + opt + " " + arg
    
if os.environ.has_key("PYCHART_OPTIONS"):
    for opt in string.split(os.environ["PYCHART_OPTIONS"]):
        arg = string.split(opt, "=")
        parse_option(arg[0], arg[1])

hooks = []        
def add_reinitialization_hook(proc):
    global hooks
    hooks.append(proc)
    proc()
    
def usage():
    print "Usage: %s [options..]" % sys.argv[0]
    print """
    --scale=X: Set the scaling factor to X (default: 1.0).
    --format=[ps|png|pdf|x11]: Set the output format (default: ps).
    --font-family=NAME: Set the default font family (default: Helvetica).
    --font-size=NAME: Set the default font size (default: 9pts).
    --line-width=NAME: Set the default line width (default: 0.4).
    --debug-level=N: Set the messaging verbosity (default: 0).
    --font-dump-dir=DIR: Specify the path prefix (or directory) for files used to dump and read font metrics info. (default: HOME/.pychart-*).
    """

def reinitialize():
    for proc in hooks:
        proc()
    
def get_options(argv = None):
    """This procedure takes a list of command line arguments in ARGV and parses
    options. It returns the un-parsed portion of ARGV. ARGV can be
    omitted, in which case its value defaults to @code{sys.argv[1:]}.
    The options supported are: "@code{--format=[ps|png|pdf|x11]}",
    "@code{--output=}@var{FILE}", "@code{--color=[yes|no]}"
    "@code{--scale=}X", "@code{--font-family=}NAME", "@code{--font-size=}X",
    "@code{--line-width=}X",
    "@code{--debug-level=}N". The below code shows an example.

@example
from pychart import *
args = theme.get_options()
ar = area.T(...)
...
@end example
    """
    if argv == None:
        argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "d:co:f:",
                                   ["format=", "output=", "color=",
                                    "scale=", "font-family=", "font-size=",
                                    "line-width=", "debug-level=",
                                    "font-dump-dir="])
    except getopt.GetoptError, foo:
        print foo
        usage()
        raise getopt.GetoptError
    for opt, arg in opts:
        if opt == "-d":
            parse_option("debug-level", arg)
        elif opt == "-c":
            parse_option("color", None)
        elif opt == "-o":
            parse_option("output", arg)
        elif opt == "-f":
            parse_option("format", arg)
        else:
            parse_option(opt[2:], arg)
    reinitialize()
    return args

    
