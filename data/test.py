import re
from string import split
import sys

class Numeral:
	def name(self, num):
		return num + ": " + convert_numbertext(num, True, True)
		
def convert_numbertext(num, begin, end):
	# strip leading zeros
	num = num.lstrip("0")
	if num == "":
		num = "0"
	# search the first matching pattern
	for i in globconv:
		reb = "^"
		ree = "$"
		if i[0][0] ==  "^":
			if begin == False:
				continue
			reb = ""
		if i[0][-1] == "$":
			if end == False:
				continue
			ree = ""
		m = re.compile(reb + i[0] + ree).search(num)
		if (not m):
			continue
		if len(i) == 1:
			return m.group(0)
		sp = split(m.expand(i[1]), "$(")
		res = ""
		cut = 0
		lbegin = begin
		lend = False
		for j in range(0, len(sp)):
			if j == 0 and len(sp[j]) == 0:
				continue
			if j>0:
				parpos = sp[j].find(")")
				cut = parpos + 1
				if j == len(sp) - 1 and len(sp[j]) == cut:
					lend = end
				if sp[j][parpos+1:parpos+2] == "|":
					lend = True
					cut = cut + 1
				res = res + convert_numbertext(sp[j][0:parpos], lbegin, lend)
			if j < len(sp) - 1 and sp[j][-1:] == "|":
				res = res + sp[j][cut:-1]
				lbegin = True
			else:
				res = res + sp[j][cut:]
				lbegin = False
		return res.strip()
	return ""

def mysplit(s):
	if s[0:1] == '"':
	    try:
		i = s.rindex('"', 1)
	    except:
		print "Syntax error: " + s
    	    return [ s[1:i], re.sub("\$(\d)", r"$(\\\1)", s[i+1:].strip().replace('"',''))]
	else:
	    j = split(s.replace('"',''), None, 1)
	    if (len(j) > 1):
		j[1] = re.sub("\$(\d)", r"$(\\\1)", j[1])
		print j[1]
	    return j


f = open(sys.argv[1],'r')
r = re.compile("[\s#]")
globconv = [mysplit(unicode(i.strip(), "UTF-8")) for i in f.readlines() if not r.match(i)]
f.close()

n = Numeral()

for i in range(1,1):
    print i, n.name(str(i))

#for i in range(999999999999999999199999,1000000000000000000000005):

print n.name("0")
print n.name("61")
print n.name("2")
print n.name("3")
print n.name("2001")
print n.name("3333333")
print n.name("2002")
print n.name("1999")
print n.name("2222")
print n.name("2009")

print n.name("EUR 0")
print n.name("EUR 1")
print n.name("EUR 2")
print n.name("EUR 3")
print n.name("EUR 23")
print n.name("10000")
print n.name("EUR 10000")
print n.name("CAD 500000")
print n.name("HKD 5000000")
print n.name("EUR 61.65")
print n.name("EUR 61.60")
print n.name("HUF 45000000.60")
print n.name("HUF 45000000.06")
print n.name("EUR 61.00")
print n.name("EUR 0.01")
print n.name("THB 61")
print n.name("THB 61.00")


print n.name("12345678912")
print n.name("1234567891234")
print n.name("123456789123456789")
print n.name("20000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000066")
print n.name("USD 10000")
