1) stackotf.py
- uses helper scripts hist.py and varcutlib.py
- you have to modify the directory pointing to ntuples in the script
- basic usage:
python -i stackotf.py <options> <variable,nbins,low-edge,high-edge> <cutlist>
- options are described in the script
- variable to plot can be either a string like "type1phiMet", or one of muon array variables like "muPt" (the index is automatically inserted) or one of predefined variables in varcutlib.py dictionary
- nbins,low-edge,high-edge are definitions of the histogram. Optionally one can use variable bins with "[x1,x2,x3,...]" list of bin edges
- cutlist is a comma separated list of cuts which again can be strings like "type1phiMet>200" or predefined cuts in varcutlib.py dictionary like e.g. PRE
- example:
python -i stackotf.py muPt,40,0,200 PRE,ETA15
- this script uses only the Draw method so the plotting is reasonably fast

2) runbkgdatadict.py
- uses stackotf in text mode to produce entries in "bkgdata.pkl"
- example usage is in the script runallsyst.sh

3) runsigdict_new.py
- generates entries in signal.pkl
- example usage is in the script runallsyst.py
- need to add b-tag syst. analogous to stackotf.py and pdf syst.

4) cardWriter/limitHistos.py
- needs to be installed in CMSSW_6_1_1/src/Workspace/HEPHYPythonTools/cardFileWriter
- uses bkgdata.pkl and signal.pkl to create cards per point and run combine tool
in asymptotic mode
- creates root files with histograms for exp/obs limits and uncert.
- example usage in runlimitHistos.sh
- has options for additional SRs
- uses only lnN; need to add propoer stat. treatment (see e.g. limitHistosSta.py)
- the b-tag syst. needs to be added (the values are already available in bkgdata.pkl)

5) plotlimit.py
- uses files from cardWriter/limitHistos.py to plot the limits
- options are reagion tag as in cardWriter/limitHistos.py and e.g. "EXP"

