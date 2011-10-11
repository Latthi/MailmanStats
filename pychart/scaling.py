import theme

x_base = 300
y_base = 300

def xscale(x):
    return x * theme.scale_factor + x_base
def yscale(y):
    return y * theme.scale_factor + y_base

def nscale(x):
    return x * theme.scale_factor
def nscale_seq(x):
    return map(nscale, x)

