function Soros(program) {
    this.funcpat = /(\|?(\uE008\()+)?(\|?\uE008\(([^\(\)]*)\)\|?)(\)+\|?)?/
    this.meta = "\\\"$()|#;"
    this.enc = "\uE000\uE001\uE002\uE003\uE004\uE005\uE006\uE007"
    this.lines = []
    if (/__numbertext__/.test(program)) {
	this.numbertext = true
	program = "0+(0|[^0]\\d*) $1\n" + program.replace("__numbertext__", "")
    } else this.numbertext = false

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
	    text = text.replace(delim + chars[i], chars2[i])
	}
	return text
    };

    // private run function
    this._run = function (data, begin, end) {
	for (i in this.lines) {
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
	if (this.numbertext) data = this.strip(data, " ").replace(/  +/g, " ")
	return this.tr(data, this.enc, this.meta, "")
    };
    
    // constructor
    program = this.tr(program, this.meta, this.enc, "\\")
    var l = program.replace(/(#[^\n]*)?(\n|$)/g, ";").split(";")
    for (var i in l) {
	var s = /^\s*(\"[^\"]*\"|[^\s]*)\s*(.*[^\s])?\s*$/.exec(l[i])
	if (s != null) {
	    s[1] = this.strip(s[1], "\"")
	    if (s[2] == undefined) s[2] = ""; else s[2] = this.strip(s[2], "\"")
	    var line = new this.linetype(
		new RegExp("^" + s[1].replace("^\^", "").replace("\$$", "") + "$"),
		s[2].replace(/\\n/g, "\n")
		    .replace(/\)\|\$/g,")||$$") // $(..)|$(..) -> $(..)||$(..)
		    .replace(/\$/g, "\uE008")
		    .replace(/\\(\d)/g, "$$$1")
		    .replace(/\uE008(\d)/g, "\uE008($$$1)"),
		/^\^/.test(s[1]), /\$$/.test(s[1])
	    )
	    this.lines = this.lines.concat(line)
	}
    }
};
