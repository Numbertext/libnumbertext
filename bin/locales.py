import sys
print "locales = \"\"\""
for i in sys.argv[1:]:
    print i
print "\"\"\".strip().split(\"\\n\")"
