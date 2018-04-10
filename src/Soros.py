"Soros interpreter (see http://numbertext.org)"
from __future__ import unicode_literals
from __future__ import print_function
import re, sys

def run(program, data):
    return compile(program).run(data)

def compile(program):
    return _Soros(program)

# conversion function
def _tr(text, chars, chars2, delim):
    for i in range(0, len(chars)):
        text = text.replace(delim + chars[i], chars2[i])
    return text

# string literals for metacharacter encoding
_m = "\\\";#$()|[]"
_c = u"\uE000\uE001\uE002\uE003\uE004\uE005\uE006\uE007\uE008\uE009" # Unicode private area
_pipe = u"\uE003"
# separator prefix = \uE00A

# pattern to recognize function calls in the replacement string
_func = re.compile(_tr(r"""(?:\|?(?:\$\()+)?  # optional nested calls
                (\|?\$\(([^\(\)]*)\)\|?)      # inner call (2 subgroups)
                (?:\)+\|?)?""",               # optional nested calls
                _m[4:8], _c[:4], "\\"), re.X)  # \$, \(, \), \| -> \uE000..\uE003

class _Soros:
    def __init__(self, prg):
        self.lines = []
        if prg.find("__numbertext__") == -1:
            prg = "__numbertext__;" + prg
        # default left zero deletion
        # and separator function (no separation, if subcall returns with empty string)
        prg = prg.replace("__numbertext__", u"""0+(0|[1-9]\\d*) $1
\"([a-z][-a-z]* )0+(0|[1-9]\\d*)\" $(\\1\\2)
\"\uE00A(.*)\uE00A(.+)\uE00A(.*)\" \\1\\2\\3
\"\uE00A.*\uE00A\uE00A.*\"
""")
        prg = _tr(prg, _m[:4], _c[:4], "\\") # \\, \", \;, \# -> \uE000..\uE003
        matchline = re.compile("^\s*(\"[^\"]*\"|[^\s]*)\s*(.*[^\s])?\s*$")
        prefix = ""
        for s in re.sub("(#[^\n]*)?(\n|$)", ";", prg).split(";"):
            macro = re.match("== *(.*[^ ]?) ==", s)
            if macro != None:
                prefix = macro.group(1)
                continue
            m = matchline.match(s)
            if prefix != "" and s != "" and m != None:
                s = m.group(1).strip("\"")
                space = " " if s != "" else ""
                caret = ""
                if s[0:1] == "^":
                    s = s[1:]
                    caret = "^"
                s2 = m.group(2) if m.group(2) != None else ""
                s = "\"" + caret + prefix + space + s + "\" " + s2
                m = matchline.match(s)
            if m != None:
                s = _tr(m.group(1).strip("\""), _c[1:4], _m[1:4], "") \
                    .replace(_c[_m.find("\\")], "\\\\") # -> \\, ", ;, #
                if m.group(2) != None:
                    s2 = m.group(2).strip("\"")
                else:
                    s2 = ""
                s2 = _tr(s2, _m[4:], _c[4:], "\\") # \$, \(, \), \|, \[, \] -> \uE004..\uE009
                # call inner separator: [ ... $1 ... ] -> $(\uE00A ... \uE00A$1\uE00A ... )
                s2 = re.sub(r"[[]\$(\d\d?|\([^\)]+\))",u"$(\uE00A\uE00A|$\\1\uE00A", s2)
                s2 = re.sub(r"[[]([^\$[\\]*)\$(\d\d?|\([^\)]+\))",u"$(\uE00A\\1\uE00A$\\2\uE00A", s2)
                s2 = re.sub(r"\uE00A]$","|\uE00A)", s2) # add "|" in terminating position
                s2 = re.sub(r"]",")", s2)
                s2 = re.sub(r"(\$\d|\))\|\$", r"\1||$", s2) # $()|$() -> $()||$()
                s2 = _tr(s2, _c[:4], _m[:4], "")   # \uE000..\uE003-> \, ", ;, #
                s2 = _tr(s2, _m[4:8], _c[:4], "")   # $, (, ), | -> \uE000..\uE003
                s2 = _tr(s2, _c[4:], _m[4:], "") # \uE004..\uE009 -> $, (, ), |, [, ]
                s2 = re.sub(r"\\(\d?\d)", r"\\g<\1>",
                    re.sub(r"\uE000(\d?\d)", "\uE000\uE001\\\\g<\\1>\uE002", s2))
                try:
                    self.lines = self.lines + [[
                        re.compile("^" + s.lstrip("^").rstrip("$") + "$"),
                        s2, s[:1] == "^", s[-1:] == "$"]]
                except:
                    print("Error in following regex line: " + s, file=sys.stderr)
                    raise

    def run(self, data):
        return self._run(data, True, True)

    def _run(self, data, begin, end):
        for i in self.lines:
            if not ((begin == False and i[2]) or (end == False and i[3])):
                m = i[0].match(data)
                if m:
                    try:
                        s = m.expand(i[1])
                    except:
                        print("Error for the following input: " + data, file=sys.stderr)
                        raise
                    n = _func.search(s)
                    while n:
                        b = False
                        e = False
                        if n.group(1)[0:1] == _pipe or n.group()[0:1] == _pipe:
                            b = True
                        elif n.start() == 0:
                            b = begin
                        if n.group(1)[-1:] == _pipe or n.group()[-1:] == _pipe:
                            e = True
                        elif n.end() == len(s):
                            e = end
                        s = s[:n.start(1)] + self._run(n.group(2), b, e) + s[n.end(1):]
                        n = _func.search(s)
                    return s
        return ""
