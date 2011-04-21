import os
import re
import math

src_name = 'uaf.json'

ptrn = re.compile( r"[^\d]*(\d*\.\d*).(\d*\.\d*).(\d*\.\d*).*" ) 
src_file = open(src_name, 'r')
i=0
outdir = 'tiles'
outfiles = {}

maxx = 1
maxy = 1
minx = 1
miny = 1

for line in src_file:
    i=i+1
    try:
        linarray = ptrn.match(line).groups()
    except:
        print line
        raise
    coords = [float(x) for x in linarray]
    outfname = '%03dx%03d.json'%(math.floor(coords[0]/100),math.floor(coords[1]/100))
    printcomma = True
    try:
        f = outfiles[outfname]
    except:
        outfiles[outfname] = open('tiles/' + outfname, 'w')
        f = outfiles[outfname]
        f.write('[');
        printcomma = False
    if printcomma:
         f.write(',')
    f.write('%f,%f,%f'%(coords[0],coords[1],coords[2]))
    maxx = max(maxx, coords[0])
    maxy = max(maxy, coords[1])
    minx = min(minx, coords[0])
    miny = min(miny, coords[1])

for f in outfiles.values():
    f.write(']')
    f.close()
outfiles = None

f = open('tiles/borders.json', 'w')
f.write('[%f,%f,0,%f,%f,0,%f,%f,0,%f,%f,0]'%(maxx,maxy,minx,miny,maxx,miny,minx,maxy))
f.close()
