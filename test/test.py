import sys
import Soros
import codecs
fil = codecs.open(sys.argv[1], encoding="UTF-8")
inp = codecs.open(sys.argv[2], encoding="UTF-8")
out = codecs.open(sys.argv[3], "wb", encoding="UTF-8")
s = Soros.compile(fil.read())
for i in inp:
    try:
        print >>out, s.run(i.strip())
    except:
        print(s.run(i.strip()))

