from ROOT import *
from math import *
import os, sys, re, glob, getopt
from array import array
from varcutlib import *
from autovivification import AutoVivification
import pickle


samples = ["T2DegStop*"]
directory = "/data/conv_v8_full/copy"
#directory = "/data/conv_v8/copy"
picklefilename = "signal.pkl"

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

###### options:
# -d <directory extension for JER/JES syst> def=""
# -p <-1,0,1> def=0 PU systematics
# -a <0,1,2> def=1 signal ISR
# -i <loose|medium|tight> def="medium" define muon isolation WP

opts, args = getopt.getopt(sys.argv[1:],"d:p:a:i:")

tag = "nominal"
if len(args)>0: tag = args[0]

# options
# - defaults
pusys = 0
sigisr = 1
wp = "medium"
# - set options
for opt,arg in opts:
    if opt == '-d':
        directory += "_"+arg
    elif opt == '-p':
        pusys = int(arg)
    elif opt == '-a':
        sigisr = int(arg)
    elif opt == "-i":
        wp = arg
    else:
        print "Unknown option",opt,"- ignoring"

nbmstop,mstop1,mstop2 = 13,100.,400.
nbdm,dm1,dm2 = 8,10.,80.
dmstop = (mstop2-mstop1)/float(nbmstop-1)
ddm = (dm2-dm1)/float(nbdm-1)

isrweight = "(1.*(ptISR<120.)+0.95*(ptISR>=120.&&ptISR<150.)+0.9*(ptISR>=150.&&ptISR<250.)+0.8*(ptISR>=250.))"

def dirname(tag):
    thisdir = directory+"/"+tag
    return thisdir
    
def filenames(tag):
    ds = glob.glob(dirname(tag))
    fns = []
    for d in ds:
        fns.extend(glob.glob(d+"/*.root"))
    return fns
    
def getchain(tag):
    t = TChain("Events")
    try:
        exec("tagvar ="+tag)
    except:
        tagvar = 1
    if type(tagvar) is list:
        thislist = tagvar
        for subtag in thislist:
            files = filenames(subtag)
            for f in files:
                if f[-5:] == ".root": t.Add(f)
    else:
        files = filenames(tag)
        for f in files:
            if f[-5:] == ".root": t.Add(f)
    return t
    
def gethisto(t,H,cutstring,weight="1."):
    hname = H.GetName()
    gROOT.cd()
    t.Draw("Max$(gpM*(gpPdg==1000006))-Max$(gpM*(gpPdg==1000022)):Max$(gpM*(gpPdg==1000006))>>"+hname,"("+weight+")*("+cutstring+")","goff")
    return
    
if os.path.isfile(picklefilename):
    os.system("cp "+picklefilename+" "+picklefilename+"_backup")
    picklefile = open(picklefilename,"rb")
    outdict = pickle.load(picklefile)
    outdict = AutoVivification(outdict)
    picklefile.close()
else:
    outdict = AutoVivification()

# initialize variable and cut dictionary
vclib = VarCutLib(wp,vetoSR=False)

t = getchain(samples[0])

Hl = []
for region in regionsW.keys():
    
    for ptregion in ptregions.keys():

        thisregionname = ptregion+region

        H = TH2F("H"+thisregionname,"",nbmstop,mstop1-0.5*dmstop,mstop2+0.5*dmstop,nbdm,dm1-0.5*ddm,dm2+0.5*ddm)
        Hl.append( H )
        H.Sumw2()
        cutstring = vclib.cut(regionsW[region]+","+ptregions[ptregion],vetoSR=False)

        weight = "puWeight"
        if sigisr>0:
            weight += "*"+isrweight
            if sigisr>1: weight += "*"+isrweight
        gethisto(t,H,cutstring,weight)
        for ix in range(nbmstop):
            x = mstop1+ix*dmstop
            for iy in range(nbdm):
                y = dm1+iy*ddm
                signalkey = "T2DegStop_{0}_{1}".format(int(x),int(x-y))
                v = H.GetBinContent(ix+1,iy+1)
                e = H.GetBinError(ix+1,iy+1)
                outdict[thisregionname][signalkey]["obs"][tag] = (v,e)
#                print thisregionname, signalkey, "obs", tag, (v,e)


picklefile = open(picklefilename,"wb")
pickle.dump(outdict,picklefile)
picklefile.close()
