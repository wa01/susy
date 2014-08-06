import sys
import pickle
from cardFileWriter import cardFileWriter
from math import *
from ROOT import *

inputSignal = "/afs/cern.ch/work/a/adamwo/susy/degs/signal.pkl"
inputBkgData = "/afs/cern.ch/work/a/adamwo/susy/degs/bkgdata.pkl"

fs = open(inputSignal,"rb")
fb = open(inputBkgData,"rb")

dictSignal = pickle.load(fs)
dictBkgData = pickle.load(fb)

shapesyst = {
"WJets":  {"SR1a": 0.10, "SR1a1": 0.10, "SR1a2": 0.10, "SR1b": 0.20, "SR1c": 0.30, "SR1cp": 0.30, "SR1d": 0.30, "SR2": 0.20, "SR2X": 0.20, "SR2d": 0.20},
"TTJets": {"SR1a": 0.20, "SR1a1": 0.20, "SR1a2": 0.20, "SR1b": 0.20, "SR1c": 0.20, "SR1cp": 0.20, "SR1d": 0.20, "SR2": 0.20, "SR2X": 0.20, "SR2d": 0.20},
"other":  {"SR1a": 0.50, "SR1a1": 0.50, "SR1a2": 0.50, "SR1b": 0.50, "SR1c": 0.50, "SR1cp": 0.50, "SR1d": 0.50, "SR2": 0.50, "SR2X": 0.50, "SR2d": 0.50}
}

for b in shapesyst.keys():
    for sr in shapesyst[b].keys():
        shapesyst[b][sr+"L"] = shapesyst[b][sr]
        shapesyst[b][sr+"H"] = shapesyst[b][sr]


signalsystematics = 0.25

syseffects = ["PU", "JER", "JES", "WPT","TPT"]

srshort = ["SR2"]

c = cardFileWriter()
c.defWidth=12
c.precision=6

def specifyExpectationWithErrorSta(c, b, p, (v,e), syst=0.):
    name = p+b
    c.specifyExpectation(b,p,v)
    if v>0. and e>0.:
        N = int(pow(v/e,2)+0.5)
        a = e*e/v 
        c.addUncertainty(name+"Sta", 'gmN',N)
        c.specifyUncertainty(name+"Sta",b,p,a)
    if syst>0.:
        c.addUncertainty(name+"Sys", 'lnN')
        r = 1. + syst
        c.specifyUncertainty(name+"Sys",b,p,r)

def specifyExpectationWithError(c, b, p, (v,e), syst=0.):
    name = p+b
    c.specifyExpectation(b,p,v)
    c.addUncertainty(name+"Sta", 'lnN')
    r = 1. + e/v if v>0. else 1.
    c.specifyUncertainty(name+"Sta",b,p,r)
    if syst>0.:
        c.addUncertainty(name+"Sys", 'lnN')
        r = 1. + syst
        c.specifyUncertainty(name+"Sys",b,p,r)

def addtuple((v1,e1),(v2,e2)):
    v = v1+v2
    e = sqrt(e1*e1+e2*e2)
    return (v,e)
    
def scaletuple((v1,e1),scale):
    v = v1*scale
    e = e1*scale
    return (v,e)
    
def getbackgrounds(sr,tag):
    bkglist = dictBkgData[sr].keys()
    bkglist.remove("data")
    bkgsum = (0.,0.)
    bkgoth = (0.,0.)
    outdict = {}
    for bkg in bkglist:
        if bkg in shapesyst.keys():
            bkgvalue = dictBkgData[sr][bkg]["exp"][tag]
            outdict[bkg] = bkgvalue
        else:
            bkgvalue = dictBkgData[sr][bkg]["obs"][tag]
            bkgoth = addtuple(bkgoth,bkgvalue)
        bkgsum = addtuple(bkgsum,bkgvalue)
        outdict["other"] = bkgoth
        outdict["sum"] = bkgsum
    return outdict
    
def sysupdown(sr,syseffect):
    bup = getbackgrounds(sr,syseffect+"up")
    if syseffect in ["JER"]:
        bcentral = getbackgrounds(sr,syseffect+"central")
    else:
        bcentral = getbackgrounds(sr,"nominal")
    bdown = getbackgrounds(sr,syseffect+"down")
    for bkg in shapesyst.keys():
        dup = bup[bkg][0]/bcentral[bkg][0] - 1.
        ddown = bdown[bkg][0]/bcentral[bkg][0] - 1.
        maxdiff = max(abs(dup),abs(ddown))
        if maxdiff > 1.: maxdiff = 1.
        sys = 1.+maxdiff if dup>0. else 1.-maxdiff
        c.specifyUncertainty(syseffect,sr,bkg,sys)
    
histos = {'0.500': ["EXP"], '0.840': ["P1S"], '0.975': ["P2S"], '0.160': ["M1S"], '-1.000': ["OBS"], '0.025': ["M2S"]}

srs = dictSignal.keys()
outnameext = "all"
if len(sys.argv)>1: outnameext = sys.argv[1]
outname = "lH"+outnameext
if outnameext[:2] == "SR" and outnameext in srs:
    usesrs = [outnameext]
elif outnameext == "all":
    usesrs = ["SR1a","SR1b","SR1c","SR2"]
elif outnameext == "allX":
    usesrs = ["SR1a","SR1b","SR1c","SR2X"]
elif outnameext == "allplus":
    usesrs = ["SR1a1","SR1a2","SR1b","SR1c","SR1cp","SR1d","SR2","SR2d"]
elif outnameext == "alllowmt":
    usesrs = ["SR1a1","SR1a2","SR1b","SR1c","SR2"]
elif outnameext == "alllowmthighmtplus":
    usesrs = ["SR1a1","SR1a2","SR1b","SR1c","SR1cp","SR2"]
elif outnameext == "alllowmthighmt1":
    usesrs = ["SR1a1","SR1a2","SR1b","SR1c","SR1cp","SR1d","SR2"]
else:
    usesrs = srs
    

fout = TFile(outname+".root","recreate")
for key in histos.keys():
    histos[key].append( TH2F(histos[key][0],"",20,12.5,512.5,100,2.5,502.5) )
    

points = dictSignal[dictSignal.keys()[0]].keys()
#for point in points:
for point in ["T2DegStop_300_270"]:
    l = point.split("_")
    mstop = float(l[1])
    mlsp = float(l[2])
    print
    print ">>>>>>>>",mstop,mlsp
    print

    c.addUncertainty('lumi', 'lnN')
    c.addUncertainty('signalSys', 'lnN')
    for syseffect in syseffects:
       c.addUncertainty(syseffect, 'lnN')
    for sr in usesrs:
        if sr not in dictBkgData.keys():
            print "signal regions do not match in",inputSignal,"and",inputBkgData
            print sr
            print dictBkgData.keys()
            sys.exit()
        bkglist = dictBkgData[sr].keys()
        bkglist.remove("data")
        c.addBin(sr,shapesyst.keys(),sr)
        specifyExpectationWithErrorSta(c,sr,"signal",scaletuple(dictSignal[sr][point]["obs"]["nominal"],1.))
        c.specifyUncertainty('lumi',sr,"signal",1.026)
        c.specifyUncertainty('signalSys',sr,"signal",1.+signalsystematics)
        
        bnominal = getbackgrounds(sr,"nominal")
        for bkg in shapesyst.keys():
            if bkg == "other":
                specifyExpectationWithErrorSta(c,sr,bkg,bnominal[bkg],shapesyst[bkg][sr])
            else:
                specifyExpectationWithError(c,sr,bkg,bnominal[bkg],shapesyst[bkg][sr])
        c.specifyObservation(sr, int(bnominal["sum"][0]+0.5))
        
        for syseffect in syseffects:
            sysupdown(sr,syseffect)

    c.writeToFile(outname+'.txt')

    res = c.calcLimit()
    for key in res.keys():
        histos[key][1].Fill(mstop,mlsp,res[key])
        
    c.reset()
        
fout.Write()
fout.Close()

