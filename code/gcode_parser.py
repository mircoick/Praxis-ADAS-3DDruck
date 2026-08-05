from pygcode import Line
import pandas as pd

rows = []

with open("data/overhang test.gcode") as f:
    for text in f:
        line = Line(text)

        row = {}

        if line.block.gcodes:
            row["cmd"] = str(line.block.gcodes[0])

        for word in line.block.words:
            row[word.letter] = word.value

        rows.append(row)

df = pd.DataFrame(rows)

print(df)
df.to_csv("data/test/gcode.csv", index=False)