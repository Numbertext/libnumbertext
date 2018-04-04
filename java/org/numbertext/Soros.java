/* Soros interpreter (see numbertext.org)
 * 2009-2010 (c) László Németh
 * License: LGPL/BSD dual license */

package org.numbertext;

import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.ArrayList;

public class Soros {
  private ArrayList<Pattern> patterns = new ArrayList<Pattern>();
  private ArrayList<String> values = new ArrayList<String>();
  private ArrayList<Boolean> begins = new ArrayList<Boolean>();
  private ArrayList<Boolean> ends = new ArrayList<Boolean>();

  private static String m = "\\\";#";
  private static String m2 = "$()|";
  private static String c = "\uE000\uE001\uE002\uE003";
  private static String c2 = "\uE004\uE005\uE006\uE007";
  private static String slash = "\uE000";
  private static String pipe = "\uE003";

  // pattern to recognize function calls in the replacement string

  private static Pattern func = Pattern.compile(translate(
	"(?:\\|?(?:\\$\\()+)?" +		// optional nested calls
	"(\\|?\\$\\(([^\\(\\)]*)\\)\\|?)" +	// inner call (2 subgroups)
	"(?:\\)+\\|?)?",			// optional nested calls
	m2, c, "\\"));				// \$, \(, \), \| -> \uE000..\uE003

  private boolean numbertext = false;

  public Soros(String source) {
    source = translate(source, m, c, "\\") 	// \\, \", \;, \# -> \uE000..\uE003
	.replaceAll("(#[^\n]*)?(\n|$)", ";");	// remove comments
    if (source.indexOf("__numbertext__") > -1) {
	numbertext = true;
	source = source.replace("__numbertext__", "0+(0|[1-9]\\d*) $1\n");
    }
    Pattern p = Pattern.compile("^\\s*(\"[^\"]*\"|[^\\s]*)\\s*(.*[^\\s])?\\s*$");
    for (String s : source.split(";")) {
	Matcher sp = p.matcher(s);
	if (!s.equals("") && sp.matches()) {
	    s = translate(sp.group(1).replaceFirst("^\"", "").replaceFirst("\"$",""),
		c.substring(1), m.substring(1), "");
	    s = s.replace(slash, "\\\\"); // -> \\, ", ;, #
	    String s2 = "";
	    if (sp.group(2) != null) s2 = sp.group(2).replaceFirst("^\"", "").replaceFirst("\"$","");
	    s2 = translate(s2, m2, c2, "\\"); 	// \$, \(, \), \| -> \uE004..\uE007
	    s2 = s2.replaceAll("(\\$\\d|\\))\\|\\$", "$1||\\$"); // $()|$() -> $()||$()
	    s2 = translate(s2, c, m, ""); 	// \uE000..\uE003-> \, ", ;, #
	    s2 = translate(s2, m2, c, ""); 	// $, (, ), | -> \uE000..\uE003
	    s2 = translate(s2, c2, m2, ""); 	// \uE004..\uE007 -> $, (, ), |
	    s2 = s2.replaceAll("[$]", "\\$")	// $ -> \$
		.replaceAll("\uE000(\\d)", "\uE000\uE001\\$$1\uE002") // $n -> $(\n)
		.replaceAll("\\\\(\\d)", "\\$$1") // \[n] -> $[n]
		.replace("\\n", "\n");		  // \n -> [new line]
	    patterns.add(Pattern.compile("^" + s.replaceFirst("^\\^", "")
		.replaceFirst("\\$$", "") + "$"));
	    begins.add(s.startsWith("^"));
	    ends.add(s.endsWith("$"));
	    values.add(s2);
	}
    }
  }

  public String run(String input) {
    if (!numbertext) return run(input, true, true);
    return run(input, true, true).trim().replaceAll("  +", " ");
  }

  private String run(String input, boolean begin, boolean end) {
    for (int i = 0; i < patterns.size(); i++) {
	if ((!begin && begins.get(i)) || (!end && ends.get(i))) continue;
	Matcher m = patterns.get(i).matcher(input);
	if (!m.matches()) continue;
	String s = m.replaceAll(values.get(i));
	Matcher n = func.matcher(s);
	while (n.find()) {
	    boolean b = false;
	    boolean e = false;
	    if (n.group(1).startsWith(pipe) || n.group().startsWith(pipe)) b = true;
	    else if (n.start() == 0) b = begin;
	    if (n.group(1).endsWith(pipe) || n.group().endsWith(pipe)) e = true;
	    else if (n.end() == s.length()) e = end;
	    s = s.substring(0, n.start(1)) + run(n.group(2), b, e) + s.substring(n.end(1));
	    n = func.matcher(s);
	}
        return s;
    }
    return "";
  }

  private static String translate(String s, String chars, String chars2, String delim) {
    for (int i = 0; i < chars.length(); i++) {
	s = s.replace(delim + chars.charAt(i), "" + chars2.charAt(i));
    }
    return s;
  }
}
