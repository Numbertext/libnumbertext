m4_define([numbertext_version_major],[1])
m4_define([numbertext_version_minor],[0])
m4_define([numbertext_version_micro],[10])
m4_define([numbertext_version],[numbertext_version_major.numbertext_version_minor.numbertext_version_micro])

AC_PREREQ([2.68])

AC_INIT([libnumbertext],[numbertext_version])
AC_CONFIG_MACRO_DIR([m4])

AM_INIT_AUTOMAKE([1.11 foreign dist-xz dist-bzip2])
AM_MAINTAINER_MODE
AC_CONFIG_HEADERS([src/config.h])
AM_SILENT_RULES([yes])

dnl Checks for programs.
AC_PROG_CXX
AC_PROG_CPP
AC_PROG_INSTALL
AC_PROG_LN_S
AC_PROG_LIBTOOL

dnl Checks for typedefs, structures, and compiler characteristics.
AC_LANG([C++])
CXXFLAGS="-Wall -std=c++11 $CXXFLAGS"

AC_CHECK_HEADERS([codecvt regex])

AC_ARG_ENABLE([boost],
	[AS_HELP_STRING([--enable-boost], [Use boost for regex operations instead of std, useful for old gcc])],
	[enable_boost="$enableval"],
	[enable_boost=no]
)

numbertext_boost=""
AS_IF([test "x$ac_cv_header_codecvt" != xyes -o "x$ac_cv_header_regex" != xyes], [
	AS_IF([test "x$enable_boost" != "xyes"], [
		AC_MSG_ERROR([Missing std::codecvt or std::regex support, use GCC 4.9 (or greater) or --enable-boost.])
	], [
		AX_BOOST_BASE([1.47.0])
		AX_BOOST_REGEX
		numbertext_boost="#define NUMBERTEXT_BOOST 1"
	])
])

dnl Checks for functions

# ================
# Check for cflags
# ================
AC_ARG_ENABLE([werror],
	[AS_HELP_STRING([--disable-werror], [Treat all warnings as errors, useful for development])],
	[enable_werror="$enableval"],
	[enable_werror=yes]
)
AS_IF([test x"$enable_werror" != "xno"], [
	CFLAGS="$CFLAGS -Werror"
	CXXFLAGS="$CXXFLAGS -Werror"
])
AS_IF([test x"$GCC" = xyes], [
	# Be tough with warnings and produce less careless code
	CFLAGS="$CFLAGS -Wall -pedantic"
	CXXFLAGS="$CXXFLAGS -Wall -pedantic"
])

AC_SUBST([NUMBERTEXT_MAJOR_VERSION],[numbertext_version_major])
AC_SUBST([NUMBERTEXT_MINOR_VERSION],[numbertext_version_minor])
AC_SUBST([NUMBERTEXT_MICRO_VERSION],[numbertext_version_micro])
AC_SUBST([NUMBERTEXT_VERSION],[numbertext_version])
AC_SUBST([NUMBERTEXT_BOOST],[${numbertext_boost}])

AC_CONFIG_FILES([
libnumbertext.pc
Makefile
data/Makefile
src/Makefile
src/numbertext-version.h
tests/Makefile
])
AC_OUTPUT

# ==============================================
# Display final informations about configuration
# ==============================================
AC_MSG_NOTICE([
==============================================================================
Build configuration:
	werror:          ${enable_werror}
	boost:           ${enable_boost}
==============================================================================
])
