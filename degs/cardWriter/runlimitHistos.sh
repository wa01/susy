#!/bin/tcsh -x
cmsenv
python limitHistos.py all
python limitHistos.py allplus
python limitHistos.py allX
python limitHistos.py allhighmtplus
python limitHistos.py allhighmtd

python limitHistos.py SR1a
#python limitHistos.py SR1b
python limitHistos.py SR1c
python limitHistos.py SR1cp
python limitHistos.py SR1d
python limitHistos.py SR2
python limitHistos.py SR2d

python limitHistos.py SR2X
python limitHistos.py SR1aL
python limitHistos.py SR1aH
python limitHistos.py SR2L
python limitHistos.py SR2H
