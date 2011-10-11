#
# Generate files under afm/ by reading Ghostscript AFM files.
#
import color
import string
import pychart_util
import re
import cPickle
import dircache
import os
import os.path
import sys
import theme

# The directories to look for font files.
_afm_paths = ["/usr/share/ghostscript/fonts/afms/adobe",
              "/usr/share/ghostscript/fonts",
              "c:/cygwin/usr/share/ghostscript/fonts",
              "c:/gs/fonts",
              "/usr/local/share/ghostscript/fonts/afms/adobe",
              "/usr/lib/ghostscript/fonts/afms/adobe",
              "/usr/lib/share/ghostscript/fonts/afms/adobe",
              "/usr/share/fonts/afms/adobe" ]

# Maps font name to the AFM path.
_afm_files = {}

# maps font name to char to its width.
_afm_cache = {}

_afm_line_re_pat = re.compile("^C (\\d+) ; WX (\\d+)")

def discover_afm_files_in_dir(dir):
    reg2 = re.compile("FontName (.*)")
    found = 0
    for file in dircache.listdir(dir):
        if re.search("afm$", file) != None:
            try:
                path = os.path.join(dir, file)
                fp = open(path)
                found = 1
                for line in fp.readlines():
                    mo = reg2.match(line)
                    if mo != None:
                        _afm_files[mo.group(1)] = path
                fp.close()
            except IOError, why:
                pychart_util.warn(path + ":" + why)
    return found

# Aliases for ghostscript font names.
_font_aliases = {
    'Bookman-Demi': "URWBookmanL-DemiBold",
    'Bookman-DemiItalic':	"URWBookmanL-DemiBoldItal",
    'Bookman-Light':		"URWBookmanL-Ligh",
    'Bookman-LightItalic':		"URWBookmanL-LighItal",
    'Courier':		"NimbusMonL-Regu",
    'Courier-Oblique':	"NimbusMonL-ReguObli",
    'Courier-Bold':		"NimbusMonL-Bold",
    'Courier-BoldOblique':	"NimbusMonL-BoldObli",
    'AvantGarde-Book':	"URWGothicL-Book",
    'AvantGarde-BookOblique':	"URWGothicL-BookObli",
    'AvantGarde-Demi':	"URWGothicL-Demi",
    'AvantGarde-DemiOblique':	"URWGothicL-DemiObli",
    'Helvetica':		"NimbusSanL-Regu",
    'Helvetica-Oblique':	"NimbusSanL-ReguItal",
    'Helvetica-Bold':		"NimbusSanL-Bold",
    'Helvetica-BoldOblique':	"NimbusSanL-BoldItal",
    'Helvetica-Narrow': "NimbusSanL-ReguCond",
    'Helvetica-Narrow-Oblique': "NimbusSanL-ReguCondItal",
    'Helvetica-Narrow-Bold':		"NimbusSanL-BoldCond",
    'Helvetica-Narrow-BoldOblique':	"NimbusSanL-BoldCondItal",
    'Palatino-Roman':			"URWPalladioL-Roma",
    'Palatino-Italic':		"URWPalladioL-Ital",
    'Palatino-Bold':			"URWPalladioL-Bold",
    'Palatino-BoldItalic':		"URWPalladioL-BoldItal",
    'NewCenturySchlbk-Roman':		"CenturySchL-Roma",
    'NewCenturySchlbk-Italic':	"CenturySchL-Ital",
    'NewCenturySchlbk-Bold':		"CenturySchL-Bold",
    'NewCenturySchlbk-BoldItalic':	"CenturySchL-BoldItal",
    'Times-Roman':			"NimbusRomNo9L-Regu",
    'Times-Italic':			"NimbusRomNo9L-ReguItal",
    'Times-Bold':			"NimbusRomNo9L-Medi",
    'Times-BoldItalic':		"NimbusRomNo9L-MediItal",
    'Symbol':				"StandardSymL",
    'ZapfChancery-MediumItalic':	"URWChanceryL-MediItal",
    'ZapfDingbats':			"Dingbats"
}

def read_afm(path):
    fp = open(path)

    table = {} # maps charcode -> width
    for line in fp.readlines():
        mo = _afm_line_re_pat.match(line)
        if not mo:
            continue
        table[int(mo.group(1))] = int(mo.group(2))
    fp.close()
    return table


for dir in _afm_paths:
    if discover_afm_files_in_dir(dir):
        pychart_util.warn("Found AFM dir: ", dir) 
        break
if len(_afm_files) == 0:
    pychart_util.warn("Warning: AFM files not found. I searched the following directories:")
    for dir in _afm_paths:
        pychart_util.warn("   "+dir)
    sys.exit(1)

for (f,g) in _font_aliases.items():
    if _afm_files.has_key(g):
        _afm_files[f] = _afm_files[g]

init_fp = open(os.path.join("afm", "__init__.py"), "wb")
init_fp.write("__all__ = [")

for font, afm_path in _afm_files.items():
    table = read_afm(afm_path)

    normFont = re.sub("-", "_", font)
    init_fp.write("\"%s\", " % (normFont, ))
    
    fp = open(os.path.join("afm", normFont + ".py"), "wb")
    fp.write("# AFM font %s (path: %s).\n" %(font, afm_path))
    fp.write("# Derived from Ghostscript distribution.\n")
    fp.write("# Go to www.cs.wisc.edu/~ghost to get the Ghostcript source code.\n")
    fp.write("import dir\ndir.afm[\"%s\"] = (" % font)
    keys = table.keys()
    for i in range(0, max(keys)+1):
        if table.has_key(i):
            fp.write("%d, " % table[i])
        else:
            fp.write("500, ")
    fp.write(")\n")
    fp.close()
    
    
init_fp.write("\"dir\"]\n")
init_fp.close()

