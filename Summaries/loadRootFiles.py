#
# Parse public page for a single analysis, retrieve root files
#   and/or show file information
#
import os,sys,re,string,pickle
import urllib, urllib2
from urlparse import urlparse,urljoin
from optparse import OptionParser
from HTMLParser import HTMLParser
# simple class holding basic analysis information
from AnalysisSummary import AnalysisSummary

# character class allowed in names
reNameChars = re.compile(r"^[a-zA-Z0-9\._-]+$")

#
# HTML parser
#
class MyHTMLParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.inTR = False
    self.inTD = False
    self.inA = False
    self.rootFiles = { }
  def getAttr(self,attrs,a):
    for x,y in attrs:
      if x==a:
        return y
    return None
  def handle_starttag(self, tag, attrs):
    if tag=="tr":
        self.inTR = True
        self.inTD = False
    elif tag=="td" and self.inTR:
        self.inTD = True
    elif tag=="a" and self.inTR and self.inTD:
      self.inA = True
      href = self.getAttr(attrs,'href')
      if href!=None and href.find(".root")>=0:
        comps = urlparse(href)
        assert comps.netloc=="" and comps.params=="" and comps.query=="" and comps.fragment==""
        name = comps.path.split("/")[-1]
        if name.endswith(".root"):
          print "Found root file",name,href
          if name in self.rootFiles:
            assert href==self.rootFiles[name]
          self.rootFiles[name] = href
      
  def handle_endtag(self, tag):
#    print "End tag: ",tag
    if tag=="tr":
        self.inTR = False
        self.inTD = False
        self.inA = False
    elif tag=="td":
        self.inTD = False
        self.inA = False
    elif tag=="a":
        self.inA = False
        
  def handle_data(self, data):
    pass

#
# main section
#
usage = "Usage: %prog [options]\n"
usage += "          list analyses\n"
usage += "     : %prog [options] CADI_number\n"
usage += "          download files and/or show files in cache\n"
usage += "     : %prog [options] CADI_number root_file\n"
usage += "          list objects in file"
parser = OptionParser(usage=usage)
parser.add_option("--listFiles", dest="listFiles", action="store_true", \
                    help="list root files found on public page (default:False)", default=False)
parser.add_option("--loadFiles", dest="loadFiles", action="store_true", \
                    help="load files to cache (default=False)", default=False)
parser.add_option("--force", "-f", dest="force", action="store_true", \
                    help="overwrite existing files (default=False)", default=False)
parser.add_option("--listObjects", dest="listObjects", action="store_true", 
                    help="list objects in a root file (default=False)", default=False)
parser.add_option("--objectTypes", dest="objectTypes", type="str", \
                    help="comma-separated list of object types to be used with listObjects (default:all)", \
                    default=None)
parser.add_option("--ls", dest="ls", action="store_true", \
                    help="show result of ls() on file (default=False)", default=False)
parser.add_option("--pkl", dest="pkl", type="str", \
                    help="path to input pickle file (default=publicAnalyses.pkl)", \
                    default="publicAnalyses.pkl")
(options, args) = parser.parse_args()
# list of object types for listObjects
types = None
if options.objectTypes!=None:
  types = options.objectTypes.split(",")
if len(args)>1 and not ( options.listObjects or options.ls ):
  options.ls = True

#
# load list of analyses
#
allAnalyses = pickle.load(file(options.pkl,"rb"))

#
# no arguments: list analyses and exit
#
if len(args)==0:
  for a in allAnalyses:
    print "{0:15s} {1:30s} {2:20s}  {3:20s} {4:20s}".format(a.pas['name'],a.title[:30],a.pas['url'],a.paper['name'],a.paper['url'])
  sys.exit(0)
#
# 1st argument: CADI number
#
name = args[0]
assert re.match(reNameChars,name)
# now look for the analysis
analysis = None
for a in allAnalyses:
  if a.name==name:
    analysis = a
    break
assert analysis!=None
# get url to public page (give priority to paper version)
url = analysis.paper['url']
if url==None or url=="" or analysis.paper['name']==None or analysis.paper['name']=="":
  url = analysis.pas['url']

#
# handle cache area
#
dataDir = "Data/" + name
# if loadFiles : download all root files linked from the public page to the cache
if options.loadFiles:
  # instantiate the request
  req = urllib2.Request(url)

  # instantiate the parser
  parser = MyHTMLParser()
  # read data and feed it to the parser
  data = ""
  response = urllib2.urlopen(req)
  data = response.read()
  #print len(data)
  parser.feed(data)

  # create cache directory, if necessary, and download files
  #dataDir = "Data/" + name
  if not os.path.exists(dataDir):
    os.mkdir(dataDir,0700)
  for n in parser.rootFiles:
    assert re.match(reNameChars,n)
    if not os.path.exists(dataDir+"/"+n) or options.force:
      # links in public page are relative: create absolute url and download
      urlf = urljoin(url,parser.rootFiles[n])
      os.system("curl "+urlf+" -o "+dataDir+"/"+n)
    else:
      print "File",dataDir+"/"+n,"exists"

#
# list all files (available in cache)
#
if options.listFiles:
  for f in os.listdir(dataDir):
    print f
#
# Second argument: list objects
#
if len(args)>1:
  import ROOT
  tf = ROOT.TFile(dataDir+"/"+args[1])
  if options.listObjects:
    for k in tf.GetListOfKeys():
      o = k.ReadObj()
      showObj = True
      if types!=None:
        showObj = False
        for t in types:
          if o.InheritsFrom(t):
            showObj = True
            break
      if showObj:
        print o.ClassName(),k.GetName(),k.GetTitle(),o.GetName(),o.GetTitle()
  if options.ls:
    tf.ls()
  tf.Close()
  
