import sys
import re
from string import split
f = open(sys.argv[1],'r')
m = {}
r2 = re.compile('"')
for i in f.readlines():
    a = split(unicode(i.strip(), "UTF-8"), "|", 1)
    m[a[0]] = re.sub(r2, "", a[1])
f.close()
print "titles = ", m
