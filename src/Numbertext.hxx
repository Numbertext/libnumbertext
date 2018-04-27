/* Soros interpreter (see numbertext.org)
 * 2018 (c) László Németh
 * License: LGPL/BSD dual license */

#ifndef NUMBERTEXT_HXX
#define NUMBERTEXT_HXX

#include "Soros.hxx"
#include <unordered_map>

class Numbertext
{
public:
    Numbertext();
    void set_prefix(std::string st) { prefix = st; };
    bool load(std::string lang, std::string filename = "");
    bool numbertext(std::wstring& number, std::string lang);
    // UTF-8 encoded input
    bool numbertext(std::string& number, std::string lang);
    std::string numbertext(int number, std::string lang);
    static std::wstring string2wstring(const std::string& s);
    static std::string wstring2string(const std::wstring& s);

private:
    std::string prefix;
    std::unordered_map<std::string, Soros> modules;
};

#endif
