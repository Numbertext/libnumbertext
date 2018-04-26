AM_CXXFLAGS =	-D_THREAD_SAFE -D_GNU_SOURCE -DVERBOSE

libnumbertext_1_0_includedir = $(includedir)/libnumbertext
libnumbertext_1_0_include_HEADERS = \
	Soros.hxx Numbertext.hxx \
        $(builddir)/numbertext-version.h

lib_LTLIBRARIES =	libnumbertext-1.0.la
libnumbertext_1_0_la_SOURCES = \
	Soros.cxx Numbertext.cxx
libnumbertext_1_0_la_LDFLAGS = -no-undefined

bin_PROGRAMS =		spellout
spellout_SOURCES =	spellout.cxx
spellout_LDADD =	libnumbertext-1.0.la

EXTRA_DIST = numbertext-version.h  \
	numbertext-version.h.in
