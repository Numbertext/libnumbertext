import Soros
import sys
import codecs

out = sys.stdout

state = ""
output = ""
prefix = ""
params = []
for i in sys.argv:
    if state != "":
        if state == "prefix":
            prefix = i + " "
        elif state == "output":
            output = i
        state = ""
        continue
    if i == "-p":
        state = "prefix"
    elif i == "-o":
        state = "output"
    else:
        params += [i]

if output != "":
    out = codecs.open(output, "wb", encoding="UTF-8")

if len(params) < 2:
    print ("Usage: soros [-o file_output] [-p prefix] soros_file number(s)")
    print ("numbers may be ranges (1-100) or ranges with steps (1-100~10)")
    sys.exit()

fil = codecs.open(params[1], encoding="UTF-8")
s = Soros.compile(fil.read())
for i in params[2:]:
    b = i[1:].split("-", 1)
    b[0] = i[0] + b[0]
    if len(b) > 1:
        step = 1
        c = b[1].split("~", 1)
        if len(c) > 1:
            b[1] = c[0]
            step = int(c[1])
        for j in range(int(b[0]), int(b[1]) + 1, step):
            try:
                print (s.run(prefix + str(j)))
            except:
                print >>out, s.run(prefix + str(j))

    else:
        try:
            print (s.run(prefix + i))
        except:
            print >>out, s.run(prefix + i)
