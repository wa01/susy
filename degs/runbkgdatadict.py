import sys,os
from math import *
from autovivification import AutoVivification
import pickle

picklefilename = "bkgdata.pkl"

options = ""
tag = "nominal"
if len(sys.argv)>1: options = sys.argv[1]
if len(sys.argv)>2: tag = sys.argv[2]

print tag

ptregions = {
"SR":  "SM",
"SRL": "SML",
"SRH": "SMH",
"CR":  "HM"
}

regionsW = {
"1a":  "PRE,SR1sums,ETA15,BV,CHn,MTR1",
"1b":  "PRE,SR1sums,ETA15,BV,CHn,MTR2",
"1c":  "PRE,SR1sums,ETA15,BV,CHn,MTR3",
"1cp": "PRE,SR1sums,ETA15,BV,CHp,MTR3",
"1d":  "PRE,SR1sumsSB,ETA15,BV,CHn,MTR3",
"2":   "PRE,SR2sums,Bsr2",
"2X":  "PRE,SR1sums,Bsr2",
"2d":  "PRE,SR2sumsSB,Bsr2,MTR3"
}

regionsTT = {
"CRTT1": "PRE,ETA15,Bcrb02",
"CRTT2": "PRE,Bcrb02"
}

script = "stackotf.py"
plotstr = "njet,10,0.,10."

samples = ["WJets", "TTJets", "DY", "ZJetsInv", "singleTop", "QCD", "VV", "sum", "data"]

def add(a1,a2):
    v = a1[0]+a2[0]
    e = sqrt( pow(a1[1],2) + pow(a2[1],2) )
    return (v,e)
    
def subtract(a1,a2,cor=False):
    factor = -1. if cor else 1.
    v = a1[0]-a2[0]
    e = sqrt( pow(a1[1],2) + factor*pow(a2[1],2) )
    return (v,e)
    
def divide(a1,a2):
    if a2[0]==0.: a2 = (1e-9,1e-9)
    v = a1[0]/a2[0]
    if a1[0]==0.: a1 = (1e-9,1e-9)
    e = v * sqrt( pow(a1[1]/a1[0],2) + pow(a2[1]/a2[0],2) )
    return (v,e)
    
def multiply(a1,a2):
    if a2[0]==0.: a2 = (1e-9,1e-9)
    v = a1[0]*a2[0]
    if a1[0]==0.: a1 = (1e-9,1e-9)
    e = v * sqrt( pow(a1[1]/a1[0],2) + pow(a2[1]/a2[0],2) )
    return (v,e)

def get(out,tag):
    v = [-1.,0.]
    for line in out.split("\n"):
        l1 = line.split("\t")
        if l1[0][:len(tag)] == tag:
            v = [float(x) for x in l1[1].split("+-")]
            break
    return v

if os.path.isfile(picklefilename):
    os.system("cp "+picklefilename+" "+picklefilename+"_backup")
    picklefile = open(picklefilename,"rb")
    outdict = pickle.load(picklefile)
    outdict = AutoVivification(outdict)
    picklefile.close()
else:
    outdict = AutoVivification()

for region in regionsTT.keys():

    thisregionname = region

    command = "python {0} -t -b {1} {2} {3}".format(script,options,plotstr,regionsTT[region])
    print command
    out = os.popen(command).read()
    for sample in samples:
        outv = get(out,"H"+sample)
        outdict[thisregionname][sample]["obs"][tag] = (outv[0],outv[1])
        print thisregionname, sample, "obs", tag, (outv[0],outv[1])

for region in regionsW.keys():
    
    for ptregion in ptregions.keys():

        thisregionname = ptregion+region

        command = "python {0} -t -b {1} {2} {3},{4}".format(script,options,plotstr,regionsW[region],ptregions[ptregion])
        print command
        out = os.popen(command).read()
        for sample in samples:
            outv = get(out,"H"+sample)
            outdict[thisregionname][sample]["obs"][tag] = (outv[0],outv[1])
            print thisregionname, sample, "obs", tag, (outv[0],outv[1])
             
    crttname = "CRTT"+region[:1]
    DCRTT = outdict[crttname]["data"]["obs"][tag]
    MtCRTT = outdict[crttname]["TTJets"]["obs"][tag]
    MaCRTT = outdict[crttname]["sum"]["obs"][tag]
    MoCRTT = subtract(MaCRTT,MtCRTT,True)
    DtCRTT = subtract(DCRTT,MoCRTT)
    SFt = divide(DtCRTT,MtCRTT)
    
    crwname = "CR"+region
    DCR = outdict[crwname]["data"]["obs"][tag]
    MwCR = outdict[crwname]["WJets"]["obs"][tag]
    MtCR = outdict[crwname]["TTJets"]["obs"][tag]
    MaCR = outdict[crwname]["sum"]["obs"][tag]
    
    MtCRExp = multiply(MtCR,SFt)
    outdict[crwname]["TTJets"]["exp"][tag] = MtCRExp
    print crwname, "TTJets", "exp", tag, MtCRExp
    MtwCR = add(MwCR,MtCR)
    MoCR = subtract(MaCR,MtwCR,True)
    DtwCR = subtract(DCR,MoCR)
    DwCR = subtract(DtwCR,MtCRExp)
    SFw = divide(DwCR,MwCR)
    
    for ptregion in ptregions.keys():
        if ptregion == "CR": continue
    
        thisregionname = ptregion+region
    
        MwSR = outdict[thisregionname]["WJets"]["obs"][tag]
        MwSRExp = multiply(SFw,MwSR)
        outdict[thisregionname]["WJets"]["exp"][tag] = MwSRExp
        print thisregionname, "WJets", "exp", tag, MwSRExp
        
        MtSR = outdict[thisregionname]["TTJets"]["obs"][tag]
        MtSRExp = multiply(SFt,MtSR)
        outdict[thisregionname]["TTJets"]["exp"][tag] = MtSRExp
        print thisregionname, "TTJets", "exp", tag, MtSRExp
            
            
picklefile = open(picklefilename,"wb")
pickle.dump(outdict,picklefile)
picklefile.close()
            
