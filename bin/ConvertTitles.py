import sys
import re
try:
    unicode
except:
    unicode = lambda i, j: i

f = open(sys.argv[1],'r')
m = {}
r2 = re.compile('"')
for i in f.readlines():
    a = unicode(i.strip(), "UTF-8").split("|", 1)
    m[a[0]] = re.sub(r2, "", a[1])
f.close()
print ("titles = " + str(m))
