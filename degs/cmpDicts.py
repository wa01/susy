import pickle
import sys

d = pickle.load(file(sys.argv[1]))
#d = dict(av)

stack = [ ]
for k, v in d.iteritems():
  stack.append( ( [ ], k, v ) )
while stack:
  p, k, v = stack.pop()
  if isinstance(v, dict):
    for l, w in v.iteritems():
      stack.append( ( p+[l], l, w ) )
  else:
    print p, k, v
