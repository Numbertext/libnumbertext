#include "Numbertext.hxx"
#include "numbertext-version.h"
#include <cstring>

#ifdef _MSC_VER
#define HAVE_CODECVT

#else
#include "config.h"
#endif

#ifdef HAVE_BOOST_REGEX_HPP
#include <boost/regex.hpp>
using namespace boost;
#else
#include <regex>
using namespace std;
#endif

#define LANG "LANG"
#define PATH "NUMBERTEXTPATH"
#define DEFPATH "/usr/share/numbertext/"
#define DEFPATH2 "data/"

enum State { base, loaded, flag_lang, flag_prefix};

void error()
{
    std::cerr << "spellout: missing language module" << std::endl;
    std::exit(EXIT_FAILURE);
}

int main(int argc, char* argv[])
{
    if (argc == 1) {
        std::cout << "spellout " NUMBERTEXT_VERSION ": convert numbers to number names and money amounts" << std::endl;
        std::cout << "Usage: spellout [-l lang] [-p prefix] par1 [par2...]" << std::endl;
        std::cout << "Parameter: n: number; n-m: range; n-m~s: range with step" << std::endl;
        std::cout << "Examples: spellout 1-10 500 1000-10000~1000" << std::endl;
        std::cout << "          spellout -l en-GB -p ordinal 1-100" << std::endl;
        std::cout << "          spellout -l en -p ordinal-number 1-100" << std::endl;
        std::cout << "          spellout -l en -p USD 100.45" << std::endl;
        std::cout << "          spellout -l en -p \"money USD\" 100.45" << std::endl;
        std::cout << "Help of language module: spellout -l es help" << std::endl;
        std::cout << "License: GNU LGPL/BSD dual-license\n";
        return 0;
    }
    std::vector <std::string> paths;
    paths.push_back("");
    paths.push_back(DEFPATH);
    paths.push_back(DEFPATH2);

    if (getenv(PATH))
        paths.insert(paths.begin() + 1, std::string(getenv(PATH)) + "/");
    std::string lang;

    Numbertext nt;
    State state = State::base;
    std::string prefix = "";
    for (int i = 1; i < argc; i++)
    {
        if (state == State::flag_lang || state == State::flag_prefix)
        {
            if (state == State::flag_lang)
            {
                lang = argv[i];
            }
            else
            {
                prefix = argv[i];
                prefix += " ";
            }
            state = State::base;
            continue;
        }
        if (strcmp(argv[i], "-l") == 0)
        {
            state = State::flag_lang;
        }
        else if (strcmp(argv[i], "-p") == 0)
        {
            state = State::flag_prefix;
        }
        else
        {
            if (lang.empty()) {
                if (getenv(LANG)) {
                    lang = std::string(getenv(LANG));
                    lang = lang.substr(0, lang.find("."));
                }
                if (lang.empty())
                    lang = "en";
            }

            if (state != State::loaded) {
                for(auto const& path: paths) {
                    nt.set_prefix(path);
                    if (nt.load(lang))
                        break;
                }
                state = State::loaded;
            }

            std::string arg = argv[i];
            smatch n;
            if (regex_match(arg, n, regex("([0-9]+)-([0-9]+)~?([0-9]+)?")))
            {
                long long b = std::stoll(n[1].str());
                long long end = std::stoll(n[2].str());
                long long step = (n[3].length() == 0) ? 1 : std::stoll(n[3].str());
                for (int j = b; j <= end; j = j + step) {
                    std::string result = prefix + std::to_string(j);
                    if (!nt.numbertext(result, lang))
                        error();
                    std::cout << result << std::endl;
                }
            }
            else
            {
                std::string result = prefix + arg;
                if (!nt.numbertext(result, lang))
                    error();
                std::cout << result << std::endl;
            }
        }
    }
}
