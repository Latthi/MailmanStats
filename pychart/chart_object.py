import pychart_util
import types
import sys

def _check_attr_types(obj, keys):
    for attr in obj.__dict__.keys():
        if not keys.has_key(attr):
            pychart_util.warn(obj, ": unknown attribute ", attr)
            pychart_util.warn("Use pydoc to see the documentation of the class.")
        typeval, can_be_none, default_value, docstring, = keys[attr][0:4]
        val = getattr(obj, attr)
        if val == None:
            if not can_be_none:
                raise Exception, "%s: Missing attribute '%s'" % (obj, attr)
            continue
        if typeval == pychart_util.AnyType:
            pass
        elif isinstance(typeval, types.FunctionType):
            # user-defined check procedure
            error = apply(typeval, (val,))
            if error != "":
                raise Exception, "%s: %s for attribute '%s', but got '%s'" % (obj, error, attr, val)
        elif 1:
            try:
                if isinstance(val, typeval):
                    pass
            except:
                pychart_util.warn("OBJ=", obj,
                                  "VAL=", val,
                                  "TYPE=", typeval,
                                  "ATTR=", attr, keys[attr])
                sys.exit(1)
        else:
            raise Exception, "%s: attribute '%s' expects type %s but found %s" % (obj, attr, typeval, val)

def set_defaults(cls, **dict):
    keys = getattr(cls, "keys")
    for attr in dict.keys():
        if not keys.has_key(attr):
            pychart_util.warn(cls, ": unknown attribute ", attr)
            pychart_util.warn("Use pydoc to see the documentation of the class.")
            sys.exit(1)
        tuple = keys[attr]   
        keys[attr] = (tuple[0], tuple[1], dict[attr], tuple[2])
        # 0 : type
        # 1: isOptional
        # 2: defaultValue
        # 3: document
        # 4: defaultValue document (optional)
        
class T:
    def init(self, args):
        keys = self.keys
        for attr in keys.keys():
            val = keys[attr][2]
            if isinstance(val, types.FunctionType):
                # if the value is procedure, use the result of the proc call
                # as the default value
                val = apply(val, ())
            setattr(self, attr, val)
            
        for key in args.keys():
            setattr(self, key, args[key])
        _check_attr_types(self, keys)
    def __init__(self, **args):
        self.init(args)

    def type_check(self):
        _check_attr_types(self, self.keys)
