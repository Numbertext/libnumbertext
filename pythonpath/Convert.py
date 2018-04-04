import sys
import re
from string import split
f = open(sys.argv[1],'r')
r = re.compile("[\s#]")

def mysplit(s):
	if s[0:1] == '"':
	    try:
		i = s.rindex('"', 1)
	    except:
		print "Syntax error: " + s
    	    return [ s[1:i], s[i+1:].strip().replace('"','')]
	else:
	    return split(s.replace('"',''), None, 1)

dic = [mysplit(unicode(i.strip(), "UTF-8")) for i in f.readlines() if not r.match(i)]
f.close()
print "dic =", dic
