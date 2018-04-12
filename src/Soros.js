function Soros(program, lang) {
    this.funcpat = /(\|?(\uE008\()+)?(\|?\uE008\(([^\(\)]*)\)\|?)(\)+\|?)?/
    this.meta = "\\\"$()|#;[]"
    this.enc = "\uE000\uE001\uE002\uE003\uE004\uE005\uE006\uE007\uE008\uE009"
    this.lines = []
    if (!/__numbertext__/.test(program))
        program = "__numbertext__;" + program

    program = program.replace("__numbertext__",
        // default left zero deletion
        "\"([a-z][-a-z]* )?0+(0|[1-9]\\d*)\" $(\\1\\2);" +
        // separator function
        "\"\uE00A(.*)\uE00A(.+)\uE00A(.*)\" \\1\\2\\3;" +
        // no separation, if subcall returns with empty string
        "\"\uE00A.*\uE00A\uE00A.*\"")

    // subclass for line data
    this.linetype = function (regex, repl, begin, end) {
        this.pat = regex
        this.repl = repl
        this.begin = begin
        this.end = end
    };

    // strip function
    this.strip = function (st, ch) {
        if (st == undefined) return ""
        return st.replace(new RegExp("^" + ch + "+"), "")
            .replace(new RegExp(ch + "+$"), "")
    };

    // character translation function
    this.tr = function (text, chars, chars2, delim) {
        for (var i = 0; i < chars.length; i++) {
            var s = delim + chars[i]
            while (text.indexOf(s) >= 0) {
                text = text.replace(s, chars2[i]);
            }
        }
        return text
    };

    // private run function
    this._run = function (data, begin, end) {
        for (var i in this.lines) {
            var l = this.lines[i]
            if (! ((!begin && l.begin) || (!end && l.end))) {
                var m = l.pat.exec(data)
                if (m != null) {
                    var s = data.replace(l.pat, l.repl)
                    var n = this.funcpat.exec(s)
                    while (n != null) {
                        var b = false
                        var e = false
                        if (n[3][0] == "|" || n[0][0] == "|") {
                            b = true
                        } else if (n.index == 0) {
                            b = begin
                        }
                        if (n[3][n[0].length - 1] == "|" || n[3][n[0].length - 1] == "|") {
                            e = true
                        } else if (n.index + n[0].length == s.length) {
                            e = end
                        }
                        s = s.substring(0, n.index + (n[1] == undefined ? 0 : n[1].length)) + this._run(n[4], b, e) +
                            s.substring(n.index + (n[1] == undefined ? 0 : n[1].length) + n[3].length)
                        n = this.funcpat.exec(s)
                    }
                    return s
                }
            }
        }
        return ""
    };

    // run with the string input parameter
    this.run = function (data) {
        data = this._run(this.tr(data, this.meta, this.enc, ""), true, true)
        return this.tr(data, this.enc, this.meta, "")
    };

    // constructor
//    program = program.replace(/\\\\/g, "\uE000")
//    program = program.replace(/\\[(]/g, "\uE003")
//    program = program.replace(/\\[)]/g, "\uE004")
//    program = program.replace(/\\[|]/g, "\uE005")
    program = this.tr(program, this.meta, this.enc, "\\")
    // switch off all country-dependent lines, and switch on the requested ones
    program = program.replace(/(^|[\n;])([^\n;#]*#[^\n]*[[]:[^\n:\]]*:][^\n]*)/g, "$1#$2")
        .replace(new RegExp("(^|[\n;])#([^\n;#]*#[^\n]*[[]:" + lang.replace("_", "-") + ":][^\n]*)", "g"), "$1$2")
    var l = program.replace(/(#[^\n]*)?(\n|$)/g, ";").split(";")
    var matchline = new RegExp(/^\s*(\"[^\"]*\"|[^\s]*)\s*(.*[^\s])?\s*$/)
    var prefix = ""
    for (var i in l) {
        var macro = /== *(.*[^ ]?) ==/.exec(l[i])
        if (macro != null) {
            prefix = macro[1]
            continue
        }
        var s = matchline.exec(l[i])
        if (prefix != "" && l[i] != "" && s != null) {
            s1 = this.strip(s[1], "\"")
            var empty = (s1 == "")
            var start = (!empty && s1[0] == '^')
            if (s[2] == undefined) s[2] = ""
            l2 = "\"" + (start ? "^" : "") + prefix + (empty ? "" : " ") +
                          s1.replace("^\^", "") + "\" " + s[2]
            s = matchline.exec(l2)
        }
        if (s != null) {
            s[1] = this.strip(s[1], "\"")
            if (s[2] == undefined) s[2] = ""; else s[2] = this.strip(s[2], "\"")
            var line = new this.linetype(
                new RegExp("^" + s[1].replace("^\^", "").replace("\$$", "") + "$"),
                s[2].replace(/\\n/g, "\n")
                    // call inner separator: [ ... $1 ... ] -> $(\uE00A ... \uE00A$1\uE00A ... )
                    .replace(/^[[]\$(\d\d?|\([^\)]+\))/g,"$(\uE00A\uE00A|$$$1\uE00A")
                    .replace(/[[]([^\$[\\]*)\$(\d\d?|\([^\)]+\))/g,"$(\uE00A$1\uE00A$$$2\uE00A")
                    .replace(/\uE00A]$/, "|\uE00A)") // add "|" in terminating position
                    .replace(/]/g, ")")
                    .replace(/(\$\d|\))\|\$/g,"$1||$$") // $(..)|$(..) -> $(..)||$(..)
                    .replace(/\$/g, "\uE008")
                    .replace(/\\0/g, "$$&")
                    .replace(/\\(\d)/g, "$$$1")
                    .replace(/\uE008(\d)/g, "\uE008($$$1)"),
                /^\^/.test(s[1]), /\$$/.test(s[1])
            )
            this.lines = this.lines.concat(line)
        }
    }
};
