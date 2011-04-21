import os

import math

src_name = 'FNSB.txt'

src_file = open(src_name, 'r')
i=0
outdir = 'tiles'
outfiles = {}

maxx = 1
maxy = 1
minx = 1
miny = 1
tilefiles = []
os.mkdir('tiles')
for line in src_file:
    i=i+1
    if i%1000 == 0:
        print 'Working on Line %d - %d Files open'%(i,len(outfiles))
    linarray = line.split(',')
    coords = [float(x) for x in linarray]
    outfname = '%03dx%03d-%d.json'%(math.floor(coords[0]/100),math.floor(coords[1]/100),coords[3])
    outfpath = 'tiles/' + outfname
    if os.path.exists(outfpath):
        try:
            f = outfiles[outfpath]
        except:
            outfiles[outfpath] = open(outfpath,'a')
            f = outfiles[outfpath]
        f.write(',%g,%g,%g'%(coords[0],coords[1],coords[2]))
    else:
        outfiles[outfpath] = open(outfpath,'w')
        f = outfiles[outfpath]
        f.write('[%g,%g,%g'%(coords[0],coords[1],coords[2]))
    if len(outfiles) > 200:
        print 'Closing 200 Files'
        for k in range(0,100):
            kv = outfiles.popitem()
            kv[1].close()
    maxx = max(maxx, coords[0])
    maxy = max(maxy, coords[1])
    minx = min(minx, coords[0])
    miny = min(miny, coords[1])
    
print 'Closing JSON Files'
outfiles = None    
"""for outfpath in tilefiles:
    f = open(outfpath,'a')
    f.write(']')
    f.close()"""
dirList=os.listdir('tiles')
for fname in dirList:
    f = open('tiles/' + fname,'a')
    f.write(']')
    f.close()


f = open('tiles/borders.json', 'w')
f.write('[%f,%f,0,%f,%f,0,%f,%f,0,%f,%f,0]'%(maxx,maxy,minx,miny,maxx,miny,minx,maxy))
f.close()
