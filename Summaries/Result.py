#
# Single SUSY result
#
import sys,os,re
from math import sqrt
from urlparse import urlparse
import ROOT

# regexps for parsing
reCADI = re.compile(r"SUS-[0-9][0-9]-[0-9][0-9][0-9]")
reNameChars = re.compile(r"^[a-zA-Z0-9\._-]+$")

#
# helper class for intersection finding
#
class Line:
    def __init__(self):
        self.x = None
        self.y = None
        self.dx = None
        self.dy = None

    def reset(self):
        self.x = None
        self.y = None
        self.dx = None
        self.dy = None
        
    # calculate line from two points
    def setFromPoints(self,x1,y1,x2,y2):
        self.x = x1
        self.y = y1
        dx = x2 - x1
        dy = y2 - y1
        dl = sqrt(dx*dx+dy*dy)
        if dl>0.:
            self.dx = dx #/dl
            self.dy = dy #/dl
            return True
        else:
            self.reset()
            return False

    # calculate line from condition:
    #   can be "m1=<value>", "m2=<value>" or "dm=<value>"
    def setFromCondition(self,condition):
        fields = condition.split("=")
        assert len(fields)==2
        fields[0] = fields[0].lower()
        value = float(fields[1])
        if fields[0].startswith("dm"):
            self.x = 0.
            self.y = self.x - value
            self.dx = 1.
            self.dy = 1.
        elif fields[0].startswith("m1"):
            self.x = value
            self.y = 0.
            self.dx = 0.
            self.dy = 1.
        elif fields[0].startswith("m2"):
            self.x = 0.
            self.y = value
            self.dx = 1.
            self.dy = 0.
        if self.x==None:
            raise ValueError
#        assert self.x!=None

    # return list of intersects with "other" line
    #   optionally restrict results to a range of path lengths
    #   in units of sqrt(dx**2+dy**2)
    def intersect(self,other,lambdaMin=None,lambdaMax=None):
        l = self.dx*other.dy - self.dy*other.dx
        if abs(l)<1.e-10:
            return None
        l = ((other.x-self.x)*other.dy-(other.y-self.y)*other.dx)/l
        if lambdaMin!=None and l<lambdaMin:
            return None
        if lambdaMax!=None and l>lambdaMax:
            return None
#        print "FOUND INTERSECT",l,self.x,self.y,self.dx,self.dy,self.x+l*self.dx,self.y+l*self.dy
        return (self.x+l*self.dx,self.y+l*self.dy)
    
    # conversion to string
    def __str__(self):
        return "x={0:6.1f} y={1:6.1f} dx={2:5.1f} dy={3:5.1f} mag={4:6.1f}".format(self.x,self.y,self.dx,self.dy,sqrt(self.dx**2+self.dy**2))

#
# class holding an analysis result
#
class Result:

    def __init__(self,cadi,figure,name,sublabel,url=None,fname=None,canvas=None,gobs=None,is1D=False):
        # cadi: CADI number
        self.cadi = cadi
        # figure: figure number (free format, should match public page)
        self.figure = figure
        # name: process description
        self.name = name
        # sublabel: additional process info
        self.sublabel = sublabel
        # url to root file
        self.url = url
        # path to root file
        self.fname = fname
        # canvas name
        self.canvas = canvas
        # name for graph with observed limits
        self.gObsName = gobs
        # cache for results (limit values)
        self.limits = { }
        # internals
        self.gotGraphs = False
        self.tf = None
        self.gobs = None
        self.is1D = is1D
        
    # load file from url, if necessary
    def getFile(self):
        assert self.url!=None or self.fname!=None
        if self.fname==None:
#            self.fname = "~/Downloads/"+os.path.split(self.url)[-1]
            urlComponents = urlparse(self.url)
            self.fname = "Data/"+self.name+"/"+urlComponents.path.split("/")[-1]
#            self.fname = "Data/"+os.path.split(self.url)[-1]
            if not os.path.exists(self.fname):
                status = os.system("curl "+self.url+" -o "+self.fname)
                assert status==0

    # list file contents
    def listFile(self):
        self.getFile()
        tf = ROOT.TFile(self.fname)
        tf.ls()
        tf.Close()

    # retrieve graph
    def getGraphs(self):
        self.getFile()
        self.tf = ROOT.TFile(self.fname)
        if self.canvas==None:
#            print "Trying to get ",self.gObsName
            self.gobs = self.tf.Get(self.gObsName)
            assert self.gobs.InheritsFrom(ROOT.TGraph.Class())
        self.gotGraphs = True

    # "manually" add a limit
    def addLimit(self,condition,value):
        assert not condition in self.limits
        self.limits[condition] = value

    # compute limits for a condition
    def computeLimit(self,condition):
        if condition in self.limits:
            return self.limits[condition]
        if not self.gotGraphs:
            self.getGraphs()
        result = [ ]
        condLine = Line()
        condLine.setFromCondition(condition)
#        print condLine
        xs = self.gobs.GetX()
        ys = self.gobs.GetY()
        x1 = xs[0]
        y1 = ys[0]
        gline = Line()
        for i in range(1,self.gobs.GetN()):
            x2 = xs[i]
            y2 = ys[i]
            if gline.setFromPoints(x1,y1,x2,y2):
#                print gline
                intersect = gline.intersect(condLine,0.,1.)
                if intersect!=None:
                    result.append(intersect)
            x1 = x2
            y1 = y2
        self.limits[condition] = result
        result.sort(reverse=True)
        return result
        
