from ROOT import *
from math import *
import os, sys, array

sr = "all"
if len(sys.argv)>1: sr = sys.argv[1]
pl = "EXP"
if len(sys.argv)>2: pl = sys.argv[2]

#fn = "/afs/cern.ch/work/a/adamwo/CMSSW_6_1_1/src/Workspace/HEPHYPythonTools/cardFileWriter/lHsimple/lH"+sr+".root"
fn = "/afs/cern.ch/work/a/adamwo/CMSSW_6_1_1/src/Workspace/HEPHYPythonTools/cardFileWriter/lH"+sr+".root"

gStyle.SetPaintTextFormat(".2f")
gStyle.SetOptStat(0)

cont = array.array("d",[-1.e300,1.])
cols = array.array("i",[kRed-10,kGreen-9])

gStyle.SetPalette(2,cols)

f = TFile(fn)
H = f.Get(pl)

H.SetContour(2,cont)

H.SetXTitle("m_{stop} [GeV]")
H.SetYTitle("m_{LSP} [GeV]")
H.SetMaximum(2)
H.SetAxisRange(80.,430.,"X")
H.SetAxisRange(0.,430.,"Y")
H.Draw("colztext")
