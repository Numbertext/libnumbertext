m4_define([numbertext_version_major],[1])
m4_define([numbertext_version_minor],[0])
m4_define([numbertext_version_micro],[1])
m4_define([numbertext_version],[numbertext_version_major.numbertext_version_minor.numbertext_version_micro])

AC_PREREQ([2.68])

AC_INIT([libnumbertext],[numbertext_version])
AC_CONFIG_MACRO_DIR([m4])
AC_LANG([C])

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

dnl Checks for headers
AC_HEADER_STDC
AC_CHECK_HEADERS([inttypes.h stdint.h string.h])

AC_DEFINE([BOOST_ALL_NO_LIB], [], [Disable boost autolink.])

dnl Checks for typedefs, structures, and compiler characteristics.
AC_LANG([C++])
CXXFLAGS='-Wall -std=c++11'

AC_CHECK_HEADER([codecvt])

AS_IF([test "x$ac_cv_header_codecvt" == xyes], [
     AS_IF([test "x$with_boost" != x], [
          BOOST_REQUIRE
          BOOST_LOCALE
     ])
     AS_IF([test "x$with_boost" == x], [
          AC_DEFINE([HAVE_CODECVT], [1], [Define if codecvt is enabled, but not --with-boost.])
     ])
])

AS_IF([test "x$ac_cv_header_codecvt" != "xyes"],
     [
	 BOOST_REQUIRE
         BOOST_LOCALE
])

dnl Checks for functions
AC_FUNC_VPRINTF
AC_CHECK_FUNCS([strdup strpbrk])

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

AC_SUBST([EXTTEXTCAT_MAJOR_VERSION],[numbertext_version_major])
AC_SUBST([EXTTEXTCAT_MINOR_VERSION],[numbertext_version_minor])
AC_SUBST([EXTTEXTCAT_MICRO_VERSION],[numbertext_version_micro])
AC_SUBST([EXTTEXTCAT_VERSION],[numbertext_version])

AC_CONFIG_FILES([
libnumbertext.pc
Makefile
data/Makefile
src/Makefile
src/numbertext-version.h
])
AC_OUTPUT

# ==============================================
# Display final informations about configuration
# ==============================================
AC_MSG_NOTICE([
==============================================================================
Build configuration:
	werror:          ${enable_werror}
==============================================================================
])
