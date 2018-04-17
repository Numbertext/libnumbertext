#include "Numbertext.hxx"

void error()
{
    std::cerr << "numbertext: missing language module" << std::endl;
    std::exit(EXIT_FAILURE);
}

int main(int argc, char* argv[])
{
    std::string lang = "en_US";
    if (argc == 1) {
        std::cout << "Usage: numbertext [-l lang] [-p prefix] par1 [par2...]" << std::endl;
        std::cout << "Parameter: n: number; n-m: range; n-m~s: range with step" << std::endl;
        std::cout << "Example: numbertext -l en_US -p ord 1-10 500 1000-10000~1000" << std::endl;
        std::cout << "Help of language module: numbertext -l es_ES help" << std::endl;
        std::cout << "License: GNU LGPL/BSD dual-license\n";
        return 0;
    }
    int state = 0;
    Numbertext nt;
    std::string prefix = "";
    for (int i = 1; i < argc; i++)
    {
        if (state != 0)
        {
            if (state == 1)
            {
                lang = argv[i];
            }
            else
            {
                prefix = argv[i];
                prefix += " ";
            }
            state = 0;
            continue;
        }
        if (strcmp(argv[i], "-l") == 0)
        {
            state = 1;
        }
        else if (strcmp(argv[i], "-p") == 0)
        {
            state = 2;
        }
        else
        {
            std::string arg = argv[i];
            std::smatch n;
            if (std::regex_match(arg, n, std::regex("([0-9]+)-([0-9]+)~?([0-9]+)?")))
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
