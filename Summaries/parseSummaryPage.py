#
# Extract analysis information from the CMS SUS public summary page
#   and store it in pkl file
#
import os,sys,re,string
import urllib, urllib2
from urlparse import urljoin
from optparse import OptionParser
from HTMLParser import HTMLParser
# Use simple class holding basic analysis information
from AnalysisSummary import AnalysisSummary
#
# regexps used in html parsing
#
reVersion = re.compile(r"most recent version:")
reCMS = re.compile(r"CMS-SUS-[0-9][0-9]-[0-9][0-9][0-9]")
rePAS = re.compile(r"CMS-PAS-SUS-[0-9][0-9]-[0-9][0-9][0-9]")
#
# HTML parser class
#
class MyHTMLParser(HTMLParser):
  def __init__(self,baseurl):
    HTMLParser.__init__(self)
    self.baseUrl = baseurl
    self.inTR = False
    self.useTR = False
    self.nTD = 0
    self.inTD = False
    self.inA = False
    self.td = AnalysisSummary(self.baseUrl)
    self.Analyses = [ ]
  def getAttr(self,attrs,a):
    for x,y in attrs:
      if x==a:
        return y
    return None
  def handle_starttag(self, tag, attrs):
#    print "Start tag: ",tag,attrs,self.inTR,self.nTD
    if tag=="tr":
        assert not self.inTR
        self.inTR = True
        self.inTD = True
        self.useTR = False
        self.nTD = 0
        self.td = AnalysisSummary(self.baseUrl)
    elif tag=="td" and self.inTR:
        self.inTD = True
        self.nTD += 1
#    if tag=='a' and self.url==None and self.getUrl:
#      for a in attrs:
#        if len(a)==2 and a[0]=='onclick':
#          mUrl = re.search(reUrl,a[1])
#          if mUrl:  
#            self.url = mUrl.group(1)
#            print self.url
    elif tag=="a" and self.inTR:
      self.inA = True
      href = self.getAttr(attrs,'href')
      if href!=None:
        if self.nTD==1:
          self.td.setPAS(url=href)
#          print "Setting PAS url"
        elif self.nTD==3:
          self.td.setPaper(url=href)
#          print "Setting paper url"
      
  def handle_endtag(self, tag):
#    print "End tag: ",tag
    if tag=="tr":
        self.inTR = False
        self.useTR = False
        self.inTD = False
        self.inA = False
#        print "Total #Analyses = ",self.nTD
    elif tag=="td":
        self.inTD = False
        self.inA = False
#        print "td.name",self.td.name,self.useTR
        if self.useTR and self.nTD>=3:
#          print "Adding analysis ",self.td.name
          self.Analyses.append(self.td)
          self.useTR = False
          self.td = AnalysisSummary(self.baseUrl)
    elif tag=="a":
        self.inA = False
        
  def handle_data(self, data):
#    if self.url==None and ( not self.getUrl ) and re.search(reVersion,data):
#      self.getUrl = True
    if self.inTR:
      if self.nTD==1:
        if re.search(reCMS,data) or re.search(rePAS,data):
#          print "Setting PAS name to ",data
          self.td.setPAS(name=data)
          self.useTR = True
      elif self.nTD==2 and self.useTR and self.td.title==None:
        title = data.strip()
        if title!="":
          self.td.title = title
      elif self.nTD==3 and self.useTR and self.inA:
#        print "Setting paper name to ",data
        self.td.setPaper(name=data)
#    if self.inTR and self.nTD==3 and data!="":
#        print "Data:",self.nTD,len(data),":",data,":"

#
# Main part
#

#
# parse options (argument is the url of the summary page)
#
parser = OptionParser(usage="Usage: %prog [options] url_of_summary_page")
parser.add_option("--listAnalyses", dest="listAnalyses", action="store_true", \
                    help="print a list of analyses (default:False)", default=False)
parser.add_option("--pkl", dest="pkl", type="str", \
                    help="path of output pickle file (default:None)", default=None)
parser.add_option("--force", "-f", dest="force", action="store_true", \
                    help="overwrite output pickle file (default:False)", default=False)
(options, args) = parser.parse_args()

# get input url and prepare the request
url = args[0]
req = urllib2.Request(url)

# instantiate the parser and feed it some HTML
parser = MyHTMLParser(url)

# read data and feed it to the parser
data = ""
response = urllib2.urlopen(req)
data = response.read()
#print len(data)
parser.feed(data)

# list analyses, if requested
if options.listAnalyses:
  for a in parser.Analyses:
    print "{0:15s} {1:30s} {2:20s}  {3:20s} {4:20s}".format(a.pas['name'],a.title[:30],a.pas['url'],a.paper['name'],a.paper['url'])


# write pickle, if requested
if options.pkl!=None:
  if os.path.exists(options.pkl) and not options.force:
    print options.pkl,"exists"
    sys.exit(1)
  import pickle
  fpkl = open(options.pkl,"wb")
  pickle.dump(parser.Analyses,fpkl)
  fpkl.close()
  

