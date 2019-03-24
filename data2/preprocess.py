import numpy as np
import csv

f = open("data/in.txt")

def clean(ls):
    ret = []
    for l in ls:
        if(len(l) != 6 and len(l)!=0):
            l.pop()
        if(len(l) == 6):
            del l[0]
            del l[1]
            ret.append(l)
    return ret

ls = [line.rstrip(';').split(",") for line in f.read().splitlines()]
ls = clean(ls)

with open("in.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerows(ls)
