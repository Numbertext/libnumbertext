/* Soros interpreter (see numbertext.org)
 * 2018 (c) László Németh
 * License: LGPL/BSD dual license */

#ifndef SOROS_HXX_
#define SOROS_HXX_

#include <iostream>
#include <iterator>
#include <string>

#include "numbertext-version.h"

#ifdef NUMBERTEXT_BOOST
  #include <boost/regex.hpp>
#else
  #include <regex>
#endif

class Soros {

public:
    Soros(std::wstring program, std::wstring filtered_lang);
    int run(std::wstring& input);
    static std::wstring translate(std::wstring s,
                std::wstring chars, const std::wstring& chars2, const std::wstring& delim);
private:
    void run(std::wstring& input, int& level, bool begin = true, bool end = true);
    static void replace(std::wstring& s, const std::wstring& search,
                const std::wstring& replace);

#ifdef NUMBERTEXT_BOOST
    std::vector<boost::wregex> patterns;
    static const boost::wregex func;
#else
    std::vector<std::wregex> patterns;
    static const std::wregex func;
#endif
    std::vector<std::wstring> values;
    std::vector<bool> begins;
    std::vector<bool> ends;

    static const std::wstring m, m2, c, c2, slash, pipe;
};

#endif
