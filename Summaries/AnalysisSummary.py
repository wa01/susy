#
# simple class holding basic analysis information (from summary)
#
from urlparse import urljoin

class AnalysisSummary:
  # instantiate with base url (summary page)
  def __init__(self,baseurl):
    self.baseUrl = baseurl
    self.name = None                              # cadi line (summary page uses 2 formats ...)
    self.title = None                             # title
    self.pas = { 'url' : None, 'name' : "" }      # PAS: url of public page and name
    self.paper = { 'url' : None, 'name' : "" }    # paper: url of public page and name

  # set PAS info (url and/or name)
  def setPAS(self,url=None,name=None):
    if url!=None:
      assert self.pas['url']==None
      self.pas['url'] = urljoin(self.baseUrl,url)
#      print "PAS url",url
    if name!=None and name.strip()!="":
      if self.name==None or self.name=="":
        self.name = name.strip()
        idx = self.name.find("SUS-")
        self.name = self.name[idx:]
        self.pas['name'] = self.name
#      print "PAS name",name,self.pas['name']
      
  # set paper info (url and/or name)
  def setPaper(self,url=None,name=None):
    if url!=None:
      assert self.paper['url']==None
      self.paper['url'] = urljoin(self.baseUrl,url)
#      print "Paper url",url
    if name!=None and name.strip()!="":
      if self.paper['name']==None or self.paper['name']=="":
        self.paper['name'] = name.strip()
#      print "Paper name",name,self.paper['name']
      

