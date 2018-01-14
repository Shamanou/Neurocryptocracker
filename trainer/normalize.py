#! /usr/bin/env python

from keras.utils import normalize
import sys
import numpy

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

out = open(sys.argv[1],'r').read().strip().split('\n')

data = [ [ float(z) for z in x.split(',') if isfloat(z)  ]  for x in out if '+' not in x ]


out = normalize(numpy.array(data, 'float64'))
outfile = open(sys.argv[2],'w+')

for line in out:
    outfile.write(str(line[0]) +','+str(line[1]) +'\n')
outfile.close()
