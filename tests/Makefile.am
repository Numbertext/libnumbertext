## Process this file with automake to create Makefile.in

TESTS =	\
es.test

AM_TESTS_ENVIRONMENT = export MODULES=$(top_srcdir)/data;

clean-local:
	-rm -rf testSubDir
        
EXTRA_DIST = $(TESTS) \
es.in \
es.out \
test.sh
