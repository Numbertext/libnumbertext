/* Soros interpreter (see numbertext.org)
 * 2018 (c) László Németh
 * License: LGPL/BSD dual license */

#include "Soros.hxx"

#ifdef NUMBERTEXT_BOOST
  using namespace boost;
#else
  using namespace std;
#endif

#define ITERATION_LIMIT 250
#define SEP L"\uE00A"

#ifdef NUMBERTEXT_BOOST
#define FIX L"\\"
#else
#define FIX L""
#endif

const std::wstring Soros::m = L"\\\";#";
const std::wstring Soros::m2 = L"$()|[]";
const std::wstring Soros::c = L"\uE000\uE001\uE002\uE003";
const std::wstring Soros::c2 = L"\uE004\uE005\uE006\uE007\uE008\uE009";
const std::wstring Soros::slash = L"\uE000";
const std::wstring Soros::pipe = L"\uE003";
// pattern to recognize function calls in the replacement string
const wregex Soros::func ( Soros::translate (
    L"(?:\\|?(?:\\$\\()+)?"           // optional nested calls
    "(\\|?\\$\\(([^\\(\\)]*)\\)\\|?)" // inner call (2 subgroups)
    "(?:\uE00A?\\)+\\|?)?",           // optional nested calls
    Soros::m2.substr(0, 4), Soros::c, L"\\"));  // \$, \(, \), \| -> \uE000..\uE003

void Soros::replace(std::wstring& s, const std::wstring& search,
                          const std::wstring& replace) {
    size_t pos = 0;
    while ((pos = s.find(search, pos)) != std::wstring::npos) {
         s.replace(pos, search.length(), replace);
         pos += replace.length();
    }
}

Soros::Soros(std::wstring program, std::wstring filtered_lang):
    begins(0),
    ends(0)
{
    program = translate(program, m, c, L"\\");     // \\, \", \;, \# -> \uE000..\uE003
    // switch off all country-dependent lines, and switch on the requested ones
    program = regex_replace(program, wregex(L"(^|[\n;])([^\n;#]*#[^\n]*\\[:[^\n:\\]]*:\\][^\n]*)"), L"$1#$2");
    replace(filtered_lang, L"_", L"-");
    program = regex_replace(program, wregex(L"(^|[\n;])#([^\n;#]*#[^\n]*\\[:" + filtered_lang + L":\\][^\n]*)"), L"$1$2");
    program = regex_replace(program, wregex(L"(#[^\n]*)?(\n|$)"), L";"); // remove comments
    // __numbertext__ sets the place of left zero deletion rule
    if (program.find(L"__numbertext__") == std::wstring::npos)
        program.insert(0, L"__numbertext__;");
    program = regex_replace(program, wregex(L"__numbertext__"),
                        // default left zero deletion
                        L"\"([a-z][-a-z]* )?0+(0|[1-9]" FIX L"\\d*)\" $$(" FIX L"\\1" FIX L"\\2);"
                        // separator function
                        SEP L"(.*)" SEP L"(.+)" SEP L"(.*) " FIX L"\\1" FIX L"\\2" FIX L"\\3;"
                        // no separation, if subcall returns with empty string
                        SEP L".*" SEP SEP L".*");

    wregex p(L"^\\s*(\"[^\"]*\"|[^\\s]*)\\s*(.*[^\\s])?\\s*$");
    wregex macro(L"== *([^ ]*) *==");
    size_t pos = 0;
    size_t old_pos = 0;
    wregex quoteStart(L"^\"");
    wregex quoteEnd(L"\"$");
    std::wstring smacro;
    while ((pos = program.find(L";", pos)) != std::wstring::npos) {
        wsmatch sp;
        std::wstring linOrig = program.substr(old_pos, pos - old_pos);
        // pattern extension after == macro ==:
        // foo bar -> "macro foo" bar
        // "foo bar" baz -> "macro foo bar" baz
        // "^foo bar" baz -> "^macro foo bar" baz
        std::wstring lin = linOrig;
        if (smacro.length() > 0 && linOrig.length() > 0 && regex_search(linOrig, sp, p))
        {
            std::wstring s = regex_replace(sp[1].str(), quoteStart, L"");
            s = regex_replace(s, quoteEnd, L"");
            std::wstring sEmpty = (s.length() == 0) ? L"" : L" ";
            if (s[0] == L'^') {
               s = regex_replace(s, wregex(L"^\\^"), L"");
               lin = L"\"^" + smacro + sEmpty + s + L"\" " + sp[2].str();
            } else
               lin = L"\"" + smacro + sEmpty + s + L"\" " + sp[2].str();
        }
        if (linOrig.length() > 0 && regex_match(linOrig, sp, macro))
        {
            smacro = sp[1].str();
        }
        else if (lin.length() > 0 && regex_search(lin, sp, p))
        {
            std::wstring s = regex_replace(sp[1].str(), quoteStart, L"");
            s = regex_replace(s, quoteEnd, L"");
            s = translate(s, c.substr(1), m.substr(1), L"");
            replace(s, slash, L"\\\\"); // -> \\, ", ;, #
            begins.push_back(!s.empty() && s[0] == L'^');
            ends.push_back(!s.empty() && s[s.length()-1] == L'$');
            s = L"^" + regex_replace(s, wregex(L"^\\^"), L"");
            s = regex_replace(s, wregex(L"\\$$"), L"") + L"$";
            try
            {
                patterns.emplace_back(s);
            } catch (...)
            {
                std::wcout << L"Soros: bad regex in \"" << sp[1].str() << "\"" << std::endl;
                break;
            }
            std::wstring s2;
            if (sp.size() > 1)
            {
                s2 = regex_replace(sp[2].str(), quoteStart, L"");
                s2 = regex_replace(s2, quoteEnd, L"");
            }
            s2 = translate(s2, m2, c2, L"\\");  // \$, \(, \), \|, \[, \]  -> \uE004..\uE009
            // call inner separator: "[ ... $1 ... ]" -> "$(" SEP " ... " SEP "$1" SEP "... )"
            s2 = regex_replace(s2, wregex(L"^\\[[$](\\d\\d?|\\([^\\)]+\\))"),
                            L"$$(" SEP SEP L"|$$$1" SEP); // add "|" in terminating position
            s2 = regex_replace(s2, wregex(L"\\[([^$\\[\\\\]*)[$](\\d\\d?|\\([^\\)]+\\))"),
                            L"$$(" SEP L"$1" SEP L"$$$2" SEP);
            s2 = translate(s2, L"]", L")", L"");
            s2 = regex_replace(s2, wregex(L"([$]\\d|\\))\\|[$]"), L"$1||$$"); // $()|$() -> $()||$()
            s2 = translate(s2, c, m, L"");   // \uE000..\uE003-> \, ", ;, #
            s2 = translate(s2, m2.substr(0, 4), c, L"");  // $, (, ), | -> \uE000..\uE003
            s2 = translate(s2, c2, m2, L""); // \uE004..\uE007 -> $, (, ), |
            s2 = regex_replace(s2, wregex(L"[$]"), L"\\$$");    // $ -> \$
            s2 = regex_replace(s2, wregex(L"\uE000(\\d)"), L"\uE000\uE001$$$1\uE002"); // $n -> $(\n)
            s2 = regex_replace(s2, wregex(L"\\\\([1-9])"), L"$$0$1"); // \[n] -> $[n]
            s2 = regex_replace(s2, wregex(L"\\\\0"), L"$$0"); // \0 -> $0
            s2 = regex_replace(s2, wregex(L"\\\\n"), L"\n"); // \n -> [new line]
            values.push_back(s2);
        }
        pos++;
        old_pos = pos;
    }
}

int Soros::run(std::wstring& input)
{
    int level = 0;
    run(input, level);
    return level;
}

void Soros::run(std::wstring& input, int& level, bool begin, bool end)
{
    if (level == -1)
        return;
    if (++level > ITERATION_LIMIT)
    {
        std::wcout << "Soros: iteration limit exceeded at the input \"" << input << "\"" << std::endl;
        input = L"";
        level = -1;
        return;
    }
    for (size_t i = 0; i < patterns.size(); i++)
    {
        if ((!begin && begins[i]) || (!end && ends[i]))
            continue;
        if (!regex_match(input, patterns[i]))
            continue;
        input = regex_replace(input, patterns[i], values[i]);
        wsmatch n;
        while (regex_search(input, n, func))
        {
            bool b = false;
            bool e = false;
            if (n[1].str()[0] == pipe[0] || n[0].str()[0] == pipe[0])
            {
                b = true;
            }
            else if (n.position() == 0)
            {
                b = begin;
            }
            if (n[1].str().back() == pipe[0] || n[0].str().back() == pipe[0])
            {
                e = true;
            }
            else if (n.position() + n[0].length() == (signed) input.length())
            {
                e = end;
            }
            std::wstring piece = n[2].str();
            run(piece, level, b, e);
            input.replace(n.position(1), n[1].length(), piece);
        }
        level--;
        return;
    }
    level--;
    input = L"";
}

std::wstring Soros::translate(
        std::wstring s,
        const std::wstring& chars,
        const std::wstring& chars2,
        const std::wstring& delim)
{
    int i = 0;
    for(const wchar_t& ch : chars)
        replace(s, delim + ch, chars2.substr(i++, 1));
    return s;
}
