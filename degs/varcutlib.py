import re

class VarCutLib:

    def __init__(self,wp="medium",vetoSR=True):
        self.wp = wp
        self.vetoSR = vetoSR
        self.vardict = self.initvar(wp)
        self.cutdict = self.initcut(wp)
        self.weightdict = self.initweight()
        
    def initvar(self,wp):
        mindx = wp+"MuIndex"
        vardict = {}
        vardict["mt"] = "muMT[{0}]".format(mindx)
        vardict["dphijmet"] = "min(abs(isrJetPhi-type1phiMetphi),2.*pi-abs(isrJetPhi-type1phiMetphi))"
        vardict["wpt"] = "muWPt[{0}]".format(mindx)
        vardict["cosa"] = "abs(cos(muPhi[{0}]-atan((muPt[{0}]*sin(muPhi[{0}])+type1phiMet*sin(type1phiMetphi))/"\
                                           "(muPt[{0}]*cos(muPhi[{0}])+type1phiMet*cos(type1phiMetphi)))))".format(mindx)
        vardict["a"] = "acos(abs(cos(abs(muPhi[{0}]-atan((muPt[{0}]*sin(muPhi[{0}])+type1phiMet*sin(type1phiMetphi))/"\
                                           "(muPt[{0}]*cos(muPhi[{0}])+type1phiMet*cos(type1phiMetphi)))))))".format(mindx)
        vardict["aomt"] = "acos(abs(cos(abs(muPhi[{0}]-atan((muPt[{0}]*sin(muPhi[{0}])+type1phiMet*sin(type1phiMetphi))/"\
                                           "(muPt[{0}]*cos(muPhi[{0}])+type1phiMet*cos(type1phiMetphi)))))))/muMT[{0}]".format(mindx)
        vardict["maxbtag"] = "Max$(jetBtag*(abs(jetEta)<2.4))"
        vardict["wgenm"] = "Sum$(gpM*(abs(gpPdg)==24))"
        vardict["genht"] = "Sum$(gpPt*(Iteration$>5&&gpSta==3&&(abs(gpPdg)<6||gpPdg==21)))"
        vardict["genwpt"] = "Sum$(gpPt*(gpSta==3&&abs(gpPdg)==14))"
        vardict["sumslice"] = "min(type1phiMet,ht-100.)"
        vardict["sumslicejet"] = "min(type1phiMet,isrJetPt-25.)"
        vardict["ht40"] = "Sum$(jetPt*(jetPt>40))"
        vardict["metvht40"] = "type1phiMet/Sum$(jetPt*(jetPt>40))"
        vardict["dphijet12"] = "acos(cos(abs(jetPhi[0]-jetPhi[1])))"
        vardict["ptb"] = "Max$(jetPt*(jetBtag>0.679&&abs(jetEta)<2.4))"
        
        return vardict
        
    def initcut(self,wp):
        Wp = wp.capitalize()
        mindx = wp+"MuIndex"
        cutdict = {}
        cutdict["TRIG"] = "(HLTMET120HBHENoiseCleaned||HLTMonoCentralPFJet80PFMETnoMu105NHEF0p95||HLTMonoCentralPFJet80PFMETnoMu95NHEF0p95)"
        cutdict["PREt0"] = "type1phiMet>200.&&isrJetPt>110."
        cutdict["PREt"] = "type1phiMet>200.&&isrJetPt>110.&&ht>300."
        cutdict["PREq"] = "isrJetBTBVetoPassed"
        cutdict["PREet"] = "(nHardElectrons+nHardTaus)==0"
        cutdict["PREm"] = "{0}>-1&&(muPt[{0}]<20.||nHardMuons{1}WP==1)".format(mindx,Wp)
        cutdict["PREmind"] = "{0}>-1".format(mindx)

        cutdict["PREnj"] = ["PREt","PREq","PREet","PREm"]
        cutdict["JET12"] = "njet60<3"
        cutdict["JET3"] = "njet60>=3"

        cutdict["PRE"] = ["PREnj","JET12"]

        cutdict["PREqSB"] = ["PREt","isrJetBTBVetoPassed==0","PREet","PREm","JET12"]
        cutdict["PREnob2b"] = ["PREt","PREet","PREm","JET12"]
        cutdict["PREnoht"] = ["PREt0","PREq","PREet","PREm","JET12"]
        cutdict["PREj3"] = ["PREnj","JET3"]
        
        cutdict["CHn"] = "muPdg[{0}]>0".format(mindx)
        cutdict["CHp"] = "muPdg[{0}]<0".format(mindx)

        cutdict["BV"] = "nbtags==0"
        cutdict["B1"] = "nbtags==1"
        cutdict["B1p"] = "nbtags>0"
        cutdict["B2"] = "nbtags==2"
        cutdict["Bsr2"] = "nHardbtags==0&&nSoftbtags>0"
        cutdict["Bcrb0"] = "nHardbtags>0&&nbtags==2"
        cutdict["Bcrb12"] = "nHardbtags>0"
        cutdict["Bcrb02"] = "nHardbtags>0&&nbtags>1"
        cutdict["Bcrb01"] = "nHardbtags==1&&nSoftbtags==0"

        cutdict["SR1sums"] = "ht>400.&&type1phiMet>300."
        cutdict["SR1sumsSB"] = "ht>300.&&type1phiMet>200.&&!(ht>400.&&type1phiMet>300.)"
        cutdict["SR2sums"] = "isrJetPt>325.&&type1phiMet>300."
        cutdict["SR2sumsSB"] = "!(isrJetPt>325.&&type1phiMet>300.)"

        cutdict["ETA15"] = "abs(muEta[{0}])<1.5".format(mindx)

        cutdict["SR1"] = ["SR1sums","BV","ETA15","CHn"]
        cutdict["SR2"] = ["SR2sums","Bsr2"]
        cutdict["SR1sb"] = ["SR1sumsSB","BV","ETA15","CHn"]

        cutdict["MTR1"] = self.var("mt")+"<60."
        cutdict["MTR2"] = self.var("mt")+">=60.&&"+self.var("mt")+"<88."
        cutdict["MTR3"] = self.var("mt")+">=88."
        cutdict["MTR11"] = self.var("mt")+"<30."
        cutdict["MTR12"] = self.var("mt")+">=30.&&"+self.var("mt")+"<60."

        cutdict["SM"] = "muPt[{0}]<20.".format(mindx)
        cutdict["SML"] = "muPt[{0}]<12.".format(mindx)
        cutdict["SMH"] = "muPt[{0}]>=12.&&muPt[{0}]<20.".format(mindx)
        cutdict["HM"] = "muPt[{0}]>30.".format(mindx)

        cutdict["W0"] = "Sum$((abs(gpPdg)<6||gpPdg==21)&&gpMo1==4&&gpMo2==5)==0"
        cutdict["W1"] = "Sum$((abs(gpPdg)<6||gpPdg==21)&&gpMo1==4&&gpMo2==5)==1"
        cutdict["W2"] = "Sum$((abs(gpPdg)<6||gpPdg==21)&&gpMo1==4&&gpMo2==5)==2"
        cutdict["W3"] = "Sum$((abs(gpPdg)<6||gpPdg==21)&&gpMo1==4&&gpMo2==5)==3"
        cutdict["W4"] = "Sum$((abs(gpPdg)<6||gpPdg==21)&&gpMo1==4&&gpMo2==5)==4"

        cutdict["GPp"] = "muIgpMatch[{0}]>-1&&gpTag[muIgpMatch[{0}]]==1".format(mindx)
        cutdict["GPt"] = "muIgpMatch[{0}]>-1&&gpTag[muIgpMatch[{0}]]==2".format(mindx)
        
        cutdict["Mt00t30"] = "muMT<30"
        cutdict["Mt30t60"] = "muMT>30&&muMT<60"
        cutdict["Mt60t90"] = "muMT>60&&muMT<90"
        cutdict["Mt90tE"] = "muMT>90"
        
        cutdict["Pt05t30"] = "muPt>5&&muPt<30"
        cutdict["Pt30t60"] = "muPt>30&&muPt<60"
        cutdict["Pt60t90"] = "muPt>60&&muPt<100"
        cutdict["Pt90tE"] = "muPt>100"
        cutdict["Pt30t200"] = "muPt>30&&muPt<200"
        cutdict["Pt30t400"] = "muPt>30&&muPt<400"
        
        cutdict["GENHTlt170"] = "Sum$(gpPt*(Iteration$>5&&gpSta==3&&(abs(gpPdg)<6||gpPdg==21)))<170."
        return cutdict
        
    def initweight(self):
        weightdict = {}
        weightdict["BV"] = "weightSBTag0_SF*weightHBTag0_SF"
        weightdict["B1"] = "((weightSBTag1_SF*weightHBTag0_SF)+(weightSBTag0_SF*weightHBTag1_SF))"
        weightdict["B1p"] = "(1.-(weightSBTag0_SF*weightHBTag0_SF))"
        weightdict["B2"] = "((weightSBTag2_SF*weightHBTag0_SF)+(weightSBTag1_SF*weightHBTag1_SF)+(weightSBTag0_SF*weightHBTag2_SF))"
        weightdict["Bsr2"] = "weightHBTag0_SF*weightSBTag1p_SF"
        weightdict["Bcrb0"] = "((weightSBTag1_SF*weightHBTag1_SF)+(weightSBTag0_SF*weightHBTag2_SF))"
        weightdict["Bcrb12"] = "weightHBTag1p_SF"
        weightdict["Bcrb02"] = "(weightHBTag1p_SF-(weightSBTag0_SF*weightHBTag1_SF))"
        weightdict["Bcrb01"] = "weightSBTag0_SF*weightHBTag1_SF"
        return weightdict
        
    def var(self,inpstring):
        var = inpstring

        if var in self.vardict.keys():
            var = self.vardict[var]
        elif var[:2]=="mu":
#            var = "{0}[{1}MuIndex]".format(var,self.wp)
            var = re.sub(r"(\w+)(.*)$",r"\1["+self.wp+r"MuIndex]\2",var)
        return var
        
    def cut(self,inp,vetoSR=True):
        cutlist = []
        if isinstance(inp,basestring):
            cutlist = inp.split(",")
        elif isinstance(inp,list):
            cutlist = inp
        else:
            print "wrong input to cut method"
        cutstringlist = []
        for cut in cutlist:
            cutval = cut
            if cut in self.cutdict.keys():
                cutval = self.cutdict[cut]
                if isinstance(cutval,list):
                    cutval = self.cut(cutval,False)
            
            if "mu" in cutval and "[" not in cutval:
                cutval = re.sub(r"(mu\w+)","\g<1>["+self.wp+"MuIndex]",cutval)
            cutstringlist.append(cutval)

        if self.vetoSR and vetoSR:
#            cutstringlist.append("!({0[0]}&&{0[1]}&&(({0[2]}&&({0[3]}||{0[4]}))||({0[5]})))".format([self.cut(x,False) for x in ["PRE","muPt<30","SR1","MTR1","MTR3","SR2"]]))
            cutstringlist.append("!({0[0]}&&{0[1]}&&(({0[2]})||({0[3]})))".format([self.cut(x,False) for x in ["PRE","muPt<30","SR1","SR2"]]))

        cutstring = "&&".join(cutstringlist)

        return cutstring
        
    def cutnobtag(self,inp):
        cutstring = self.cut(inp,vetoSR=False)
        cutstringlist = cutstring.split("&&")
        cutstringlistAUX = cutstring.split("&&")
        for cutitem in cutstringlistAUX:
            if cutitem.find("btags")>-1:
                cutstringlist.remove(cutitem)
        cutstring = "&&".join(cutstringlist)
        return cutstring
        
    def weightbtag(self,inp,suffix="_SF"):
        weightstring = "1."
        if isinstance(inp,basestring):
            cutlist = inp.split(",")
        elif isinstance(inp,list):
            cutlist = inp
        else:
            print "wrong input to weightbtag method"
        for cut in cutlist:
            if cut in self.cutdict.keys():
                if cut in self.weightdict.keys():
                    weightstring = self.weightdict[cut]
                    break
                cutval = self.cutdict[cut]
                if isinstance(cutval,list):
                    weightstring = self.weightbtag(cutval)
        weightstring = weightstring.replace("_SF",suffix)
        return weightstring
        
