#
# get graph and show limit
# arguments: <CADI number> <Figure label> <condition>
#
import sys
from optparse import OptionParser
from Result import Result
from Results import allResults
     

parser = OptionParser()
parser.add_option("--condition", dest="condition", type="str", \
                    help="condition in the form <var>=<value> (default: m2=10)", \
                    default="m2=10")
(options, args) = parser.parse_args()\

cadi = None if len(args)<1 else args[0]
fig = None if len(args)<2 else args[1]

# avoid to mix possible root logon output
import ROOT
d = ROOT.gDirectory
#
# if 1rst argument missing: list all CADI lines
#
if cadi==None:
    print "Available CADI lines are "+",".join(sorted(allResults.allResults.keys()))
    sys.exit(0)
#
# if 2nd argument missing: list all results
#
if fig==None:
    figs = [ ]
    if not cadi in allResults.allResults:
        print "Unknown CADI line",cadi
        sys.exit(1)
    print "Available results for "+cadi+" are "+",".join(sorted(allResults.allResults[cadi].keys()))
    sys.exit(0)

print "{0:10s} {1:10s}   {2:6s}  {3:6s}".format("CADI","Figure","  m1","  m2")
for c in sorted(allResults.allResults.keys()):
    if cadi!=None and c!=cadi:
        continue
    for f in sorted(allResults.allResults[c].keys()):
        if fig!=None and f!=fig:
            continue
        result = allResults.allResults[c][f]
        limits = result.computeLimit(options.condition)
        if len(limits)>0:
            print "{0:10s} {1:10s}   {2:6.1f}  {3:6.1f}".format(c,f,limits[0][0],limits[0][1])
        else:
            print "{0:10s} {1:10s}   {2:6s}  {3:6s}".format(c,f,"   -","   -")


