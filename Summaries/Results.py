#
# list of results
#
from Result import Result

#
# simple class holding the list
#
class Results:

    def __init__(self):
        self.allResults = { }

    def add(self,result):
        cadi = result.cadi
        if not cadi in self.allResults:
            self.allResults[cadi] = { }
        assert not result.figure in self.allResults[cadi]
        self.allResults[cadi][result.figure] = result

#
# main body
#

allResults = Results()

# SSDL2015 / Fig4a (T1tttt)
allResults.add(Result("SUS-15-008","Fig4a","g~g~, g~ #rightarrow tt N1~","", \
                    fname="Data/SUS-15-008/CMS-SUS-15-008_Figure_004-a.root",
                    gobs="ssobs"))
# SSDL2015 / Fig4b (T5ttbbWW)
allResults.add(Result("SUS-15-008","Fig4b","g~g~, g~ #rightarrow bt C1~, C1~ #rightarrow W N1~","", \
                    fname="Data/SUS-15-008/CMS-SUS-15-008_Figure_004-b.root",
                    gobs="ssobs"))
# SSDL2015 / Fig5a (T5tttt, dm=m(t))
allResults.add(Result("SUS-15-008","Fig5a","g~g~, g~ #rightarrow t~t, t~ #rightarrow t N1~","m(t~)=m(N1~)+m(t)", \
                    fname="Data/SUS-15-008/CMS-SUS-15-008_Figure_005-a.root",
                    gobs="ssobs"))
# SSDL2015 / Fig5b (T5tttt, dm=20)
allResults.add(Result("SUS-15-008","Fig5b","g~g~, g~ #rightarrow t~t, t~ #rightarrow t N1~","m(t~)=m(N1~)+20GeV", \
                    fname="Data/SUS-15-008/CMS-SUS-15-008_Figure_005-b.root",
                    gobs="ssobs"))
# SSDL2015 / Fig5c (T5ttcc)
allResults.add(Result("SUS-15-008","Fig5c","g~g~, g~ #rightarrow t~t, t~ #rightarrow c N1~","m(t~)=m(N1~)+20GeV", \
                    fname="Data/SUS-15-008/CMS-SUS-15-008_Figure_005-c.root",
                    gobs="ssobs"))
# SSDL2015 / Fig6 (T6ttWW)
allResults.add(Result("SUS-15-008","Fig6","b~b~, b~ #rightarrow t C1~, C1~ #rightarrow W N1~","m(N1~)=50GeV", \
                    fname="Data/SUS-15-008/CMS-SUS-15-008_Figure_006.root",
                    gobs="ssobs"))
# SSDL2015 / Fig 7a (T5qqqqWW)
allResults.add(Result("SUS-15-008","Fig7a","g~g~, g~ #rightarrow qq C1~, C1~ #rightarrow W N1~","dm(C1~)=0.5*(m(g~)+m(N1~)", \
                    fname="Data/SUS-15-008/CMS-SUS-15-008_Figure_007-a.root",
                    gobs="ssobs"))
# SSDL2015 / Fig 7b (T5qqqqWW)
allResults.add(Result("SUS-15-008","Fig7b","g~g~, g~ #rightarrow qq C1~, C1~ #rightarrow W N1~","dm(C1~)=20GeV", \
                    fname="Data/SUS-15-008/CMS-SUS-15-008_Figure_007-b.root",
                    gobs="ssobs"))

# MT2 / T2tt
allResults.add(Result("SUS-16-014","Fig9a","t~t~, t~ #rightarrow t N1~","", \
                    fname="Data/SUS-16-014/CMS-PAS-SUS-16-014_Figure_009-a.root",
                    gobs="ObsLim2"))
# MT2 / T2bb
allResults.add(Result("SUS-16-014","Fig9b","b~b~, b~ #rightarrow b N1~","", \
                    fname="Data/SUS-16-014/CMS-PAS-SUS-16-014_Figure_009-b.root",
                    gobs="ObsLim"))
# MT2 / T2cc (degenerate udsc)
allResults.add(Result("SUS-16-014","Fig9c_4q","q~q~, q~ #rightarrow q N1~","4*(qL+qR)", \
                    fname="Data/SUS-16-014/CMS-PAS-SUS-16-014_Figure_009-c.root",
                    gobs="ObsLim"))
# MT2 / T2cc (one light squark)
allResults.add(Result("SUS-16-014","Fig9c2_1q","q~q~, q~ #rightarrow q N1~","1 light squark", \
                    fname="Data/SUS-16-014/CMS-PAS-SUS-16-014_Figure_009-c.root",
                    gobs="ObsLim2"))
# MT2 / T1tttt
allResults.add(Result("SUS-16-014","Fig10a","g~g~, g~ #rightarrow tt N1~","", \
                    fname="Data/SUS-16-014/CMS-PAS-SUS-16-014_Figure_010-a.root",
                    gobs="ObsLim"))
# MT2 / T1bbbb
allResults.add(Result("SUS-16-014","Fig10b","g~g~, g~ #rightarrow bb N1~","", \
                    fname="Data/SUS-16-014/CMS-PAS-SUS-16-014_Figure_010-b.root",
                    gobs="ObsLim"))
# MT2 / T1qqqq
allResults.add(Result("SUS-16-014","Fig10c","g~g~, g~ #rightarrow qq N1~","", \
                    fname="Data/SUS-16-014/CMS-PAS-SUS-16-014_Figure_010-c.root",
                    gobs="ObsLim"))
# MT2 / T5qqqqVV
allResults.add(Result("SUS-16-014","Fig10d","g~g~, g~ #rightarrow qq V~, V~ #rightarrow W/Z N1~","m(C1~)=0.5*(m(g~)+m(N1~)", \
                    fname="Data/SUS-16-014/CMS-PAS-SUS-16-014_Figure_010-d.root",
                    gobs="ObsLim"))
# RA2b / T1bbbb
allResults.add(Result("SUS-16-015","Fig6a","g~g~, g~ #rightarrow bb N1~","", \
                    fname="Data/SUS-16-015/CMS-PAS-SUS-16-015_Figure_006-a.root",
                    gobs="ObsLim"))
# RA2b / T1tttt
allResults.add(Result("SUS-16-015","Fig6b","g~g~, g~ #rightarrow tt N1~","", \
                    fname="Data/SUS-16-015/CMS-PAS-SUS-16-015_Figure_006-b.root",
                    gobs="ObsLim"))
# RA2b / T1qqqq
allResults.add(Result("SUS-16-015","Fig6c","g~g~, g~ #rightarrow qq N1~","", \
                    fname="Data/SUS-16-015/CMS-PAS-SUS-16-015_Figure_006-c.root",
                    gobs="ObsLim"))
# RA2 / T2bb
allResults.add(Result("SUS-16-015","Fig7a","b~b~, b~ #rightarrow b N1~","", \
                    fname="Data/SUS-16-015/CMS-PAS-SUS-16-015_Figure_007-a.root",
                    gobs="ObsLim"))
# RA2 / T2tt
allResults.add(Result("SUS-16-015","Fig7b","t~t~, t~ #rightarrow t N1~","", \
                    fname="Data/SUS-16-015/CMS-PAS-SUS-16-015_Figure_007-b.root",
                    gobs="ObsLim"))
# RA2 / T2qq
allResults.add(Result("SUS-16-015","Fig7c","t~t~, t~ #rightarrow t N1~","4*(qL+qR)", \
                    fname="Data/SUS-16-015/CMS-PAS-SUS-16-015_Figure_007-c.root",
                    gobs="ObsLim"))
# RA4DPhi / T1tttt
allResults.add(Result("SUS-16-019","Fig6a","g~g~, g~ #rightarrow tt N1~","", \
                    fname="Data/SUS-16-019/CMS-PAS-SUS-16-019_Figure_006-a.root",
                    gobs="graph_smoothed_Obs"))
# RA4DPhi / T5qqqqWW
allResults.add(Result("SUS-16-019","Fig6b","g~g~, g~ #rightarrow qq C1~, C1~ #rightarrow W N1~","dm(C1~)=0.5*(m(g~)+m(N1~)", \
                    fname="Data/SUS-16-019/CMS-PAS-SUS-16-019_Figure_006-b.root",
                    gobs="graph_smoothed_Obs"))
# RA7 / T1tttt
allResults.add(Result("SUS-16-022","Fig5a","g~g~, g~ #rightarrow tt N1~","", \
                    fname="Data/SUS-16-022/CMS-PAS-SUS-16-022_Figure_005-a.root",
                    gobs="gr_obs_smoothed"))
# RA7 / T1qqqqVV
allResults.add(Result("SUS-16-022","Fig5b","g~g~, g~ #rightarrow qq C1~, C1~ #rightarrow W N1~","dm(C1~)=0.5*(m(g~)+m(N1~)", \
                    fname="Data/SUS-16-022/CMS-PAS-SUS-16-022_Figure_005-b.root",
                    gobs="gr_obs_smoothed"))
# EWK Fig.7
allResults.add(Result("SUS-16-022","Fig7","C1~N1~ ...","3l, flavour-democratic, dm(l~)=0.5*(m(C1~)+m(N1~)", \
                    fname="Data/SUS-16-024/CMS-PAS-SUS-16-024_Figure_007.root",
                    gobs="gr_obs_smoothed"))
# EWK Fig8c
allResults.add(Result("SUS-16-022","Fig8c","C1~N1~ ...","SS2l+3l, flavour-democratic, dm(l~)=0.05*(m(C1~)+m(N1~)", \
                    fname="Data/SUS-16-024/CMS-PAS-SUS-16-024_Figure_008-c.root",
                    gobs="gr_obs_smoothed"))
# EWK Fig.9
allResults.add(Result("SUS-16-022","Fig9","C1~N1~ ...","3l, tau-dominated, dm(l~)=0.5*(m(C1~)+m(N1~)", \
                    fname="Data/SUS-16-024/CMS-PAS-SUS-16-024_Figure_009.root",
                    gobs="gr_obs_smoothed"))
# EWK Fig.10a
allResults.add(Result("SUS-16-024","Fig10a","C1~N1~ ...","3l, WZ", \
                    fname="Data/SUS-16-024/CMS-PAS-SUS-16-024_Figure_010-a.root",
                    gobs="gr_obs_smoothed"))
# EWK Fig.10b
allResults.add(Result("SUS-16-024","Fig10b","C1~N1~ ...","3l, WH", \
                    fname="Data/SUS-16-024/CMS-PAS-SUS-16-024_Figure_010-b.root",
                    gobs="gr_obs"))
## stop 2l / Fig. 10 (T2tt)
#allResults.add(Result("SUS-16-027","Fig10","t~t~, t~ #rightarrow t N1~","", \
#                    fname="Data/SUS-16-027/CMS-PAS-SUS-16-027_Figure_010.root",
#                    gobs="ObsLim"))

