import sys
import pickle

inputSignal = "/afs/cern.ch/work/a/adamwo/public/susy/degs/signal.pkl"
inputBkgData = "/afs/cern.ch/work/a/adamwo/public/susy/degs/bkgdata.pkl"

tag = "nominal"
if len(sys.argv)>1: tag = sys.argv[1]

def strerr(x,d=2):
    s = "{0[0]:8."+str(d)+"f}+-{0[1]:5."+str(d)+"f}"
    return s.format(x)
    
fs = open(inputSignal,"rb")
fb = open(inputBkgData,"rb")

dictSignal = pickle.load(fs)
dictBkgData = pickle.load(fb)

for key0 in dictSignal.keys():
    for key1 in dictSignal[key0].keys():
        for key2 in dictSignal[key0][key1].keys():
#            if key2 != tag: continue
            for key3 in dictSignal[key0][key1][key2].keys():
                print "{0}\t{1}\t{2}\t{3}\t{4}".format(key0,key1,key2,key3,strerr(dictSignal[key0][key1][key2][key3],3))
for key0 in dictBkgData.keys():
    for key1 in dictBkgData[key0].keys():
        for key2 in dictBkgData[key0][key1].keys():
#            if key2 != tag: continue
            for key3 in dictBkgData[key0][key1][key2].keys():
                print "{0}\t{1}\t{2}\t{3}\t{4}".format(key0,key1,key2,key3,strerr(dictBkgData[key0][key1][key2][key3],3))
                
                
