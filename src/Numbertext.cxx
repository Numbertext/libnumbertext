/* Soros interpreter (see numbertext.org)
 * 2018 (c) László Németh
 * License: LGPL/BSD dual license */

#include <sstream>
#include <fstream>

#include "Numbertext.hxx"

#ifdef NUMBERTEXT_BOOST
  #include <boost/locale/encoding_utf.hpp>
  using namespace boost;
#else
  #include <codecvt>
  #include <locale>
  using namespace std;
#endif

#define MODULE_DIR ""
#define SOROS_EXT ".sor"

bool readfile(std::string filename, std::wstring& result)
{
    std::wifstream wif(filename);
    if (wif.fail())
        return false;
#ifdef _MSC_VER
    wif.imbue(std::locale(std::locale(), new std::codecvt_utf8<wchar_t>));
#else
    wif.imbue(std::locale("en_US.UTF-8"));
#endif
    std::wstringstream wss;
    wss << wif.rdbuf();
    result = wss.str();
    return true;
}

Numbertext::Numbertext():
    prefix(MODULE_DIR),
    modules(0)
{
}

bool Numbertext::load(std::string lang, std::string filename)
{
    std::wstring module;
    if (filename.length() == 0)
        filename = prefix + regex_replace(lang,
                regex("-"), "_") + SOROS_EXT;
    if (!readfile(filename, module))
    {
        // try to load without the country code
        filename = regex_replace(filename,
                regex("[-_].." SOROS_EXT "$"), SOROS_EXT);
        if (!readfile(filename, module))
            return false;
    }
    modules.insert(std::make_pair(lang, Soros(module, string2wstring(lang))));
    return true;
}

bool Numbertext::numbertext(std::wstring& number, std::string lang)
{
    auto module = modules.find(lang);
    if (module == modules.end())
    {
        if (!load(lang))
            return false;
        module = modules.find(lang);
    }
    module->second.run(number);
    return true;
}

bool Numbertext::numbertext(std::string& number, const std::string& lang)
{
    std::wstring wnumber = string2wstring(number);
    bool result = numbertext(wnumber, lang);
    number = wstring2string(wnumber);
    return result;
}

std::string Numbertext::numbertext(int number, const std::string& lang)
{
    std::wstring wnumber = std::to_wstring(number);
    numbertext(wnumber, lang);
    return wstring2string(wnumber);
}

std::wstring Numbertext::string2wstring(const std::string& st)
{
#ifndef NUMBERTEXT_BOOST
    typedef std::codecvt_utf8<wchar_t> convert_type;
    std::wstring_convert<convert_type, wchar_t> converter;
    return converter.from_bytes( st );
#else
    return ::locale::conv::utf_to_utf<wchar_t>(st.c_str(), st.c_str() + st.size());
#endif
}

std::string Numbertext::wstring2string(const std::wstring& st)
{
#ifndef NUMBERTEXT_BOOST
    typedef std::codecvt_utf8<wchar_t> convert_type;
    std::wstring_convert<convert_type, wchar_t> converter;
    return converter.to_bytes( st );
#else
    return ::locale::conv::utf_to_utf<char>(st.c_str(), st.c_str() + st.size());
#endif
}
