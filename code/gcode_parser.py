from pygcode import Line
from time import *

comments, params, gcodes = [],[],[]


with open('data/overhang test.gcode', 'r') as fh:
    for line_text in fh.readlines():
        line = Line(line_text)

        #print(line)  # will print the line (with cosmetic changes)
        gcodes.extend(line.block.gcodes)  # is your list of gcodes
        #print(line.block.gcodes)
        params.extend(line.block.modal_params)  # are all parameters not assigned to a gcode, assumed to be motion modal parameters
        if line.comment:
            comments.extend(line.comment.text)  # your comment text

print(gcodes)

gcodes = '\n'.join(str(g) for g in gcodes)
params = '\n'.join(str(g) for g in params)
comments = '\n'.join(str(g) for g in comments)

with open("data/test/gcode.csv","w",encoding="utf-8") as data:
    data.write(gcodes)

with open("data/test/comments.csv","w",encoding="utf-8") as data:
    data.write(comments)

with open("data/test/params.csv","w",encoding="utf-8") as data:
    data.write(params)