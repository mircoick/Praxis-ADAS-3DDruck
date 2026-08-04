from pygcode import *
import numpy as np
from time import *

gcodes = [
";TYPE:SKIN",
G1 F600 Z48.05,
G1 F2400 E871.62376,
G1 F2338.4 X121.299 Y149.663 E871.62967,
G0 F15000 X121.254 Y149.142,
G1 F2338.4 X120.626 Y149.77 E871.66438
]
gcodes = '\n'.join(str(g) for g in gcodes)

file_path = f"data/test/{strftime("%d-%b-%Y_%H-%M-%S", gmtime())}.gcode"

with open(file_path,"w",encoding="utf-8") as data:
    data.write(gcodes)
print(gcodes)