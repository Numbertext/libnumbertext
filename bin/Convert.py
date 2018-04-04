import sys
f = open(sys.argv[1],'r')
print ("# -*- encoding: UTF-8 -*-")
print ("r\"\"\"")
sys.stdout.writelines([i.strip() + '\n' for i in f.readlines()])
print ("\"\"\"")
print ("from __future__ import unicode_literals")
