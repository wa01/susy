1) make sure you have python 2.7 or higher
2) python parseSummaryPage.py <url-of-new-style-list-of-CMS-SUS-results> --pkl publicAnalyses.pkl
3) mkdir Data (if it does not yet exist)
4) source loadAll.csh (or individual commands as in this file)

Show cadi lines with 
  python showResults.py
or show results for one line with
  python showResults.py <cadi>
or get limit values with
  python showResults.py <cadi> <result> --condition <condition>
where condition can be m1=X, m2=X, or dm=X
