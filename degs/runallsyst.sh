#!/bin/tcsh -x
setcms 600

python runbkgdatadict.py "-c 1" nominal
python runbkgdatadict.py "-c 0" WPTdown
python runbkgdatadict.py "-c 2" WPTup
python runbkgdatadict.py "-x 0" TPTdown
python runbkgdatadict.py "-x 2" TPTup
python runbkgdatadict.py "-p -1" PUdown
python runbkgdatadict.py "-x 1" PUup
python runbkgdatadict.py "-d JESup" JESup
python runbkgdatadict.py "-d JESdown" JESdown
python runbkgdatadict.py "-d JERcentral" JERcentral
python runbkgdatadict.py "-d JERup" JERup
python runbkgdatadict.py "-d JERdown" JERdown
python runbkgdatadict.py "-y _SF" Bcentral
python runbkgdatadict.py "-y _SF_b_Up" Bbup
python runbkgdatadict.py "-y _SF_b_Down" Bbdown
python runbkgdatadict.py "-y _SF_light_Up" Blup
python runbkgdatadict.py "-y _SF_light_Down" Bldown

#python runsigdict_new.py nominal -b
#python runsigdict_new.py -a 0 ISRdown -b
#python runsigdict_new.py -a 2 ISRup -b
#python runsigdict_new.py -d JERdown JERdown -b
#python runsigdict_new.py -d JERup JERup -b
#python runsigdict_new.py -d JERcentral JERcentral -b
#python runsigdict_new.py -d JESdown JESdown -b
#python runsigdict_new.py -d JESup JESup -b
