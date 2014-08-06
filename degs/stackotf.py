from ROOT import *
from math import *
import os, sys, time, getopt
from hist import *
import array
from varcutlib import *

#directory = "/ivan/susy/conv_v5/copy"
#directory = "/data/conv_v8_full/copy"
#directoryalt = "/data/conv_v8/copy"
directory = "/home/adamwo/data/monoJetTuples_v8/copy"
directoryalt = "/home/adamwo/data/monoJetTuples_v7/copy"

###### options:
# -w <number of wjet sample> def=4
# -n <title of the histogram> def=""
# -d <directory extension for JER/JES syst> def=""
# -c <0,1,2> def=1 WJet ISR correction
# -x <0,1,2> def=1 TTJet pt correction
# -s def=False switch off SR veto
# -t def=False text only, dont plot
# -p <-1,0,1> def=0 PU systematics (0: puWeight; 2: weight; 3: 1.)
# -a <0,1,2> def=1 signal ISR
# -l def=False log scale
# -o def=False use old v5 tuples
# -i <loose|medium|tight> def="medium" define muon isolation WP
# -v def=False switch to v7
# -r def=False do not plot ratio
# -b go into batch mode
# -y <suffix> def="no" use btag weights with given suffix
#arguments:
# 1) var,nb,x1,x2
# 2) cutlist def="PRE"
# 3) MET,HT,Delta (define MET/HT slice)

opts, args = getopt.getopt(sys.argv[1:],"w:n:d:c:x:stp:a:loi:vrby:")

# args 1)
hdef = args[0].split(",")
var = hdef[0]
varMC = var
ibra = hdef[1].find("[")
if ibra==-1:
    nb = int(hdef[1])
    x1 = float(hdef[2])
    x2 = float(hdef[3])
    if len(hdef)>4: varMC = hdef[4]
else:
    exec("lll = "+sys.argv[1][ibra:])
    x1 = array.array("d",lll)
    nb = len(x1)-1
    x2 = -999

# args 2)
cutlist = []
if len(args)>1:
    cutlist.extend(args[1].split(","))
else:
    cutlist = ["PRE"]

# args 3)
metcut,htcut,delta = 0.,0.,-1.
if len(args)>2:
    metcut,htcut,delta = [float(x) for x in args[2].split(",")]
    if delta<0.: delta = sys.float_info.max
    cutlist.append("(type1phiMet>{0}&&ht>{1})".format(metcut,htcut))
    cutlist.append("!(type1phiMet>{0}&&ht>{1})".format(metcut+delta,htcut+delta))

# options
# - defaults
wjetsample = 4
title = ""
dirMCadd = ""
wjetisr = 1
ttjetpt = 1
vetosroff = False
textonly = False
pusys = 0
sigisr = 1
log = False
old = False
wp = "medium"
noratio = False
usebtagweights = "no"
# - set options
for opt,arg in opts:
    if opt == '-w':
        wjetsample = arg
    elif opt == '-n':
        title = arg
    elif opt == '-d':
        dirMCadd = "_"+arg
    elif opt == '-c':
        wjetisr = int(arg)
    elif opt == '-x':
        ttjetpt = int(arg)
    elif opt == '-s':
        vetosroff = True
    elif opt == '-t':
        textonly = True
    elif opt == '-p':
        pusys = int(arg)
    elif opt == '-a':
        sigisr = int(arg)
    elif opt == '-l':
        log = True
    elif opt == "-o":
        old = True
        directory = "/ivan/susy/conv_v5/copy"
    elif opt == "-i":
        wp = arg
    elif opt == "-v":
        directory = "/data/conv_v7/copy"
    elif opt == "-r":
        noratio = True
    elif opt == "-b":
        print "switching to batch mode"
        gROOT.SetBatch(True)
        print "switched to batch mode"
    elif opt == "-y":
        usebtagweights = arg
    else:
        print "Unknown option",opt,"- ignoring"
        
Wp = wp.capitalize()
mindx = wp+"MuIndex"

directoryMC = directory+dirMCadd

# initialize variable and cut dictionary
vclib = VarCutLib(wp,vetoSR=(not vetosroff))
###### special varibales

varinp = var
var = vclib.var(var)
print "varstring =",var
varMC = vclib.var(varMC)

###### samples
sampleD = "data"
#sampleS = ["stop300lsp270FullSim", "stop300lsp240g150FullSim","stop200lsp170g100FullSim"]
#sampleS = ["stop300lsp270FullSim", "stop300lsp240g150FullSim"]
sampleS = ["T2DegStop_300_270", "T2DegStop_300_240"]
colorsS = [kRed+2, kBlue+2, kGreen+2]

sampleB = ["VV", "QCD", "singleTop", "ZJetsInv", "DY", "TTJets", "WJets"]
colorsB = [kMagenta-9, kGreen-9, kBlue-9, kOrange-9, kRed-9, kCyan-10, kYellow-9]
WJets1 = ["W1JetsToLNu", "W2JetsToLNu", "W3JetsToLNu", "W4JetsToLNu"]
WJets2 = ["WplusToLNu","WminusToLNu"]
WJets3 = ["WJetsToLNu"]
WJets4 = ["WJetsHT150v2"]
WJets5 = ["WJetsToLNu_PtW-180_TuneZ2star_8TeV-madgraph-tarball", "W4JetsToLNu"]
exec("WJets = WJets{0}".format(wjetsample))
QCD = ["QCD20to600","QCD600to1000","QCD1000"]
DY = ["8TeV-DYJetsToLL_PtZ-50_TuneZ2star_8TeV_ext-madgraph-tarball"]
if not usebtagweights == "no": DY = ["DY"]
TTJets = ["TTJetsPowHeg"]
VV = ["WW","ZZ","WZ"]
if old: TTJets = ["TTJets-powheg-v2"]
#if dirMCadd != "":
#    DY = ["DY"]
#    TTJets = ["TTJets"]

###### cuts
if usebtagweights == "no":
    cutstring = vclib.cut(cutlist,vetoSR=False)
else:
    cutstring = vclib.cutnobtag(cutlist)
cutstringSRveto = vclib.cut(cutlist,vetoSR=True)
cutstringTrigger = vclib.cut(["TRIG"],vetoSR=False)
print "cutstring =",cutstring
print "cutstringSRveto =",cutstringSRveto

###### weights
isrweight = "(1.*(ptISR<120.)+0.95*(ptISR>=120.&&ptISR<150.)+0.9*(ptISR>=150.&&ptISR<250.)+0.8*(ptISR>=250.))"
#wjetisrweight = "(1.-0.001*(max(Sum$(gpPt*(abs(gpPdg)==24)),150.)-150.))"
#ttptweight = "1.24*sqrt(exp(0.156-0.00137*Sum$(gpPt*(gpPdg==6)))*exp(0.156-0.00137*Sum$(gpPt*(gpPdg==-6))))"
ttptweight = "1.24*exp(0.156-0.5*0.00137*(gpPt[6]+gpPt[7]))"
bkgweight = "puWeight"
if pusys == 1:
    bkgweight = "puWeightSysPlus"
elif pusys == -1:
    bkgweight = "puWeightSysMinus"
elif pusys == 2:
    bkgweight = "weight"
elif pusys == 3:
    bkgweight = "1."
if not usebtagweights == "no":
    bkgweight += "*"+vclib.weightbtag(cutlist,suffix=usebtagweights)
wptweight_a = "((ptw<200)*1.+(ptw>200&&ptw<250)*1.008+(ptw>250&&ptw<350)*1.063+(ptw>350&&ptw<450)*0.992+(ptw>450&&ptw<650)*0.847+(ptw>650&&ptw<800)*0.726+(ptw>800)*0.649)"
wptweight_p = "((ptw<200)*1.+(ptw>200&&ptw<250)*1.016+(ptw>250&&ptw<350)*1.028+(ptw>350&&ptw<450)*0.991+(ptw>450&&ptw<650)*0.842+(ptw>650&&ptw<800)*0.749+(ptw>800)*0.704)"
wptweight_n = "((ptw<200)*1.+(ptw>200&&ptw<250)*0.997+(ptw>250&&ptw<350)*1.129+(ptw>350&&ptw<450)*1.003+(ptw>450&&ptw<650)*0.870+(ptw>650&&ptw<800)*0.687+(ptw>800)*0.522)"
wptweight = wptweight_a
if ("CHp" in cutlist):
    wptweight = wptweight_p
elif ("CHn" in cutlist):
    wptweight = wptweight_n

wjetisrweight = wptweight.replace("ptw",vclib.vardict["wpt"])
wjetisrweight = wjetisrweight.replace(mindx,"max("+mindx+",0)")
if wjetisr: print "wjetisrweight =", wjetisrweight

###### helpers
def dirname(tag):
    if tag == sampleD:
        thisdir = directory+"/"+tag
    else:
        thisdir = directoryMC+"/"+tag
    if not os.path.isdir(thisdir):
        print "WARNING: path",thisdir,"does not exist, using",directory+"/"+tag,"instead!"
        thisdir = directory+"/"+tag
    if not os.path.isdir(thisdir):
        print "WARNING: path",thisdir,"does not exist, using",directoryalt+"/"+tag,"instead!"
        thisdir = directoryalt+"/"+tag
    if not os.path.isdir(thisdir):
        print "WARNING: path",thisdir,"does not exist, exiting"
        sys.exit()
#    print tag,">>>",thisdir
    return thisdir
    
def getchain(tag):
    t = TChain("Events")
    try:
        exec("tagvar ="+tag)
    except:
        tagvar = 1
    if type(tagvar) is list:
        thislist = tagvar
        for subtag in thislist:
            files = os.listdir(dirname(subtag))
            for f in files:
                if f[-5:] == ".root": t.Add(dirname(subtag)+"/"+f)
    else:
        files = os.listdir(dirname(tag))
        for f in files:
            if f[-5:] == ".root": t.Add(dirname(tag)+"/"+f)
    return t
    
    
def book(tag):
    return h1f("H"+tag,nb,x1,x2)

def gethisto(tag,weight="1.",extratag=""):
    t = getchain(tag)
    H = book(tag+extratag)
    fullcutstring = cutstring
    if tag == sampleD: fullcutstring = cutstringSRveto
    if tag == "data": fullcutstring += "&&"+cutstringTrigger
    thisvar = var if tag=="data" else varMC
    if True:
        print ">>>> ",tag
        print "var=", thisvar
        print "cut=", fullcutstring
        print "weight=", weight
    t.Draw(thisvar+">>H"+tag+extratag,"("+fullcutstring+")*("+weight+")","goff")
    gROOT.cd()
    Hclone = H.Clone()
    return Hclone
    
def subtract(a1,a2,cor=False):
    factor = -1. if cor else 1.
    res = []
    res.append(a1[0]-a2[0])
    res.append( sqrt( pow(a1[1],2) + factor*pow(a2[1],2) ) )
    return res
    
def divide(a1,a2):
    res = []
    if a2[0]==0.: a2[0] = 1e-9
    res.append(a1[0]/a2[0])
    if a1[0]==0.: a1[0] = 1e-9
    res.append( res[0] * sqrt( pow(a1[1]/a1[0],2) + pow(a2[1]/a2[0],2) ) )
    return res
    
def divideb(a1,a2):
    res = []
    if a2[0]==0.: a2[0] = 1e-9
    res.append(a1[0]/a2[0])
    if a1[0]==0.: a1[0] = 1e-9
    res.append( sqrt( ( (1.-2.*res[0])*pow(a1[1],2) + pow(res[0]*a2[1],2) ) ) / a2[0] )
    return res
    
def strerr(x,d=2):
    s = "{0[0]:8."+str(d)+"f}+-{0[1]:5."+str(d)+"f}"
    return s.format(x)
    
def getmtnumbers(H,HS):
    bins = [[0,60],[61,88],[89,151]]
    v  = [ [ [] for i in range(7) ] for j in range(3) ]
    vr = [ [ [] for i in range(7) ] for j in range(3) ]
    vs  = [ [ [] for i in range(len(HS)) ] for j in range(3) ]
    vsr = [ [ [] for i in range(len(HS)) ] for j in range(3) ]
    error = Double(0.)
    
    fstring = "{0:<10}   "+"   ".join(["{"+str(x+1)+":^17}" for x in range(len(v[0]))])
    print fstring.format("region","data","bckg","WJets","other","data-other","data/bckg","(d-o)/Wjets")
    for ir,r in enumerate(bins):
        for iv in range(3):
            v[ir][iv].append(H[iv].IntegralAndError(r[0],r[1],error))
            v[ir][iv].append(float(error))
        v[ir][3].extend(subtract(v[ir][1],v[ir][2],True))
        v[ir][4].extend(subtract(v[ir][0],v[ir][3]))
        v[ir][5].extend(divide(v[ir][0],v[ir][1]))
        v[ir][6].extend(divide(v[ir][4],v[ir][2]))
        fstring = "R{0}:       "+"".join(["{1["+str(x)+"]:>20}" for x in range(len(v[ir]))])
        print fstring.format(ir+1,[strerr(x) for x in v[ir]])
    for ir,r in enumerate(bins):
        if ir==1: continue
        for iv in range(7):
            vr[ir][iv].extend(divide(v[ir][iv],v[1][iv]))
        fstring = "R{0}/R2:    "+"".join(["{1["+str(x)+"]:>20}" for x in range(len(v[ir]))])
        print fstring.format(ir+1,[strerr(x,3) for x in vr[ir]])
    
    print "-"*40     
    
    fstring = "{0}\t"+"\t".join(["{"+str(x+1)+"}" for x in range(len(v[0]))])
    print fstring.format("region","data","bckg","WJets","other","data-other","data/bckg","(d-o)/WJets")
    for ir,r in enumerate(bins):
        fstring = "R{0}\t"+"\t".join(["{1["+str(x)+"]}" for x in range(len(v[ir]))])
        print "R{0}\t{1[0]}\t{1[1]}\t{1[2]}\t{1[3]}\t{1[4]}\t{1[5]}\t{1[6]}".format(ir+1,[strerr(x) for x in v[ir]])
    for ir,r in enumerate(bins):
        if ir==1: continue
        fstring = "R{0}/R2\t"+"\t".join(["{1["+str(x)+"]}" for x in range(len(v[ir]))])
        print "R{0}/R2:\t{1[0]}\t{1[1]}\t{1[2]}\t{1[3]}\t{1[4]}\t{1[5]}\t{1[6]}".format(ir+1,[strerr(x,3) for x in vr[ir]])
    
#    print "-"*40     
    
#    fstring = "{0:<10}   "+"   ".join(["{1["+str(x)+"]:^27}" for x in range(len(sampleS))])
#    print fstring.format("S/B",sampleS)
#    for ir,r in enumerate(bins):
#        for iv in range(len(HS)):
#            vs[ir][iv].append(HS[iv].IntegralAndError(r[0],r[1],error))
#            vs[ir][iv].append(float(error))
#            vsr[ir][iv].extend(divide(vs[ir][iv],v[ir][1]))
#        fstring = "R{0}:       "+"".join(["{1["+str(x)+"]:^30}" for x in range(len(HS))])
#        print fstring.format(ir+1,[strerr(x,3) for x in vsr[ir]])

def getcontributions(HT,HB,HS):
    bins = [[0,60],[61,88],[89,151]]
    error = Double(0.)
    HBn = []
    for i,s in enumerate(sampleB):
        H = gethisto(s,extratag="n")
        HBn.append(H)
    HSn = []
    for i,s in enumerate(sampleS):
        H = gethisto(s,extratag="n")
        HSn.append(H)
    for ir,r in enumerate(bins):
        print "Composition R{0}:".format(ir+1)
        vwtotal = HT.IntegralAndError(r[0],r[1],error)
        ewtotal = error
        for i,s in enumerate(sampleB):
            vn = HBn[i].Integral(r[0],r[1])
            vw = HB[i].IntegralAndError(r[0],r[1],error)
            ew = error
            print "{0:<15}\t{1:>10n}\t{2}\t{3}".format(sampleB[i],vn,strerr([vw,ew],3),strerr(divideb([vw,ew],[vwtotal,ewtotal]),3))
        print "-"*20
        for i,s in enumerate(sampleS):
            vn = HSn[i].Integral(r[0],r[1])
            vw = HS[i].IntegralAndError(r[0],r[1],error)
            ew = error
            print "{0:<30}\t{1:>10n}\t{2}\t{3}".format(sampleS[i],vn,strerr([vw,ew],3),strerr(divideb([vw,ew],[vwtotal,ewtotal]),3))
         
def getnumbers(H):
    for h in H:
        name = h.GetName()
        if name == "Hsum": vsum = h.Integral(1,h.GetNbinsX())
    for h in H:
        name = h.GetName()
        error = Double(0.)
        v = h.IntegralAndError(1,h.GetNbinsX(),error)
        e = error
        print "{0:<30}\t{1}\t({2:5.1f}%)".format(name,strerr([v,e],2),v/vsum*100.)

###### main
Hdata = gethisto(sampleD)
       
ths = THStack("ths","")
leg = TLegend(0.6,0.67,0.87,0.92)
legentries = []
Hsum = Hdata.Clone("Hsum")
Hsum.Reset()
legentries.append([0, Hdata, sampleD, "p"])

bhists = []
for i,s in enumerate(sampleB):
    weight = bkgweight
    if wjetisr>0 and s == "WJets":
        weight += "*"+wjetisrweight
        if wjetisr>1: weight += "*"+wjetisrweight
    if s == "WJets" and wjetsample == 4:
        weight += "*1.19"
    if ttjetpt>0 and s == "TTJets":
        weight += "*"+ttptweight
        if ttjetpt>1: weight += "*"+ttptweight
    H = gethisto(s,weight)
    bhists.append(H)
    H.SetFillStyle(1001)
    H.SetFillColor(colorsB[i])
    ths.Add(H)
#    leg.AddEntry(H, s, "f")
    legentries.append([len(sampleB)-i, H, s, "f"])
    Hsum.Add(H)
    
shists = []
for i,s in enumerate(sampleS):
    weight = bkgweight
    if sigisr>0:
        weight += "*"+isrweight
        if sigisr>1: weight += "*"+isrweight
    H = gethisto(s,weight)
    shists.append(H) # otherwise will be deleted from gROOT (hmmm)
    H.SetLineWidth(3)
    H.SetLineColor(colorsS[i])
#    leg.AddEntry(H, s, "l")
    legentries.append([len(sampleB)+i, H, s, "l"])

if not textonly:
    gStyle.SetOptStat(kFALSE)
    if False:
        gROOT.ProcessLine(".L tdrstyle.C")
        setTDRStyle()
        tdrStyle.SetOptStat(kFALSE)
        tdrStyle.SetMarkerStyle(1)
        tdrStyle.SetErrorX(0.5)
#    c1 = TCanvas("c1","",700,700)
#    c1 = TCanvas("c1","",1500,0,900,1000)
    c1 = TCanvas("c1","",1500,0,700,800)
    c1.Divide(1,2,0,0)
    
    yswidth = 700
    ylwidth = 1000
    scaleFacBottomPad = yswidth/float((ylwidth-yswidth))
    yBorder = (ylwidth-yswidth)/float(ylwidth)    
    p1 = c1.cd(1)
    if not noratio:
        p1.SetBottomMargin(0.001)
    else:
        p1.SetBottomMargin(0.1)
    p1.SetTopMargin(0.05)
    p1.SetRightMargin(0.1)
    p1.SetPad(p1.GetX1(), yBorder, p1.GetX2(), p1.GetY2())
    p2 = c1.cd(2)
    p2.SetTopMargin(0)
    p2.SetRightMargin(0.1)
    p2.SetBottomMargin(scaleFacBottomPad*0.13)
    p2.SetPad(p2.GetX1(), p2.GetY1(),p2.GetX2(), yBorder-0.003)
        
        
    if log: p1.SetLogy(1)

    p1.cd()
    ths.SetMinimum(1.)
    ths.SetMaximum(ths.GetMaximum()*2.)
    ths.SetTitle(title)
    ths.Draw('hist')
    ths.GetHistogram().SetXTitle(var)
    ths.GetHistogram().SetYTitle("events")
    Hsum.SetFillStyle(3001)
    Hsum.SetFillColor(1)
    Hsum.Draw("e2 same")

    Hdata.SetMarkerStyle(20)
    Hdata.Draw("e same")

    for H in shists:
        H.Draw("hist same")

    for legentry in sorted(legentries):
        leg.AddEntry(legentry[1],legentry[2],legentry[3])
    leg.Draw()
    
    targetLumi=19700
    tlatex = TLatex()
    tlatex.SetNDC()
    tlatex.SetTextFont(42)
    tlatex.SetTextSize(0.035)
    tlatex.DrawLatex(0.1, 0.955, "#bf{CMS Preliminary "+\
           str(int(round(targetLumi/10.))/100.)+" fb^{-1} at #sqrt{s} = 8 TeV}")


    if not noratio:
        p2.cd()
        p2.SetGridx(1)
        p2.SetGridy(1)
        Hr = Hdata.Clone("Hr")
        Hsumnoerr = Hsum.Clone("Hsumnoerr")
        Hsumnoerr.SetError(array.array("d",[0]*nb))
        Hr.Divide(Hsumnoerr)
        Hr.SetMaximum(2.8)
        Hr.SetMinimum(0)
        Hr.SetXTitle(var)
        Hr.SetYTitle("data/MC ")

        Hr.GetXaxis().SetTitleSize(scaleFacBottomPad*Hr.GetXaxis().GetTitleSize())
        Hr.GetXaxis().SetLabelSize(scaleFacBottomPad*Hr.GetXaxis().GetLabelSize())
        Hr.GetXaxis().SetTickLength(scaleFacBottomPad*Hr.GetXaxis().GetTickLength())
        Hr.GetYaxis().SetTitleSize(scaleFacBottomPad*Hr.GetYaxis().GetTitleSize())
        Hr.GetYaxis().SetLabelSize(scaleFacBottomPad*Hr.GetYaxis().GetLabelSize())

        Hr.GetYaxis().SetNdivisions(505)
        Hr.GetYaxis().SetTitleOffset(1.00 / scaleFacBottomPad)


        Hr.Draw("e")
        Hr2 = Hsum.Clone("Hr2")
        Hr2.Divide(Hsumnoerr)
        Hr2.Draw("e2same")
        ll = TLine(Hr.GetXaxis().GetXmin(),1,Hr.GetXaxis().GetXmax(),1)
        ll.Draw()
    
    gPad.Update()

if (var == "mt") and nb == 150:
    getmtnumbers([Hdata,Hsum,HWJets],shists)
    getcontributions(Hsum,bhists,shists)
else:
    getnumbers([Hdata,Hsum]+bhists+shists)
    if not textonly:
        c1.SaveAs("stackotf.png")
        fout = TFile("stackotf.root","RECREATE")
        c1c = c1.Clone()
        c1c.Write()
        fout.Close()

