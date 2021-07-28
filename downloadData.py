import os
from ContentUtil import ContentUtil
from analysePages import ParseWebPages

print("Start download data!!!!")
pwg = ParseWebPages()
cate = {"AI":"Artificial_intelligence","Bio":"Biology","Art":"Art"}
for cat,val in cate.items():
	pwg.getSubCategory(val,cate)
	pwg.getPagesLink(cate)
dl = DownloadPages("datasets")
dl.readfile(writeToFile=True)
print("Finished download data!!!!")