import sys
f = open(sys.argv[1],'r')
print "# -*- encoding: UTF-8 -*-"
print "ur\"\"\""
sys.stdout.writelines(f.readlines())
print "\"\"\""
