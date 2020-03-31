/* See numbertext.org
 * 2009-2010 (c) László Németh
 * License: LGPL/BSD dual license */

package org.numbertext;

import static org.numbertext.MenuState.LANGUAGE;
import static org.numbertext.MenuState.PARAM;
import static org.numbertext.MenuState.PREFIX;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Numbertext {

	private static final Pattern LANG_PATTERN_NO = Pattern.compile("n[bn]([-_]NO)?");

	private static Map<String, Soros> modules = new HashMap<String, Soros>();

	private static Soros load(String langfile, String langcode) {
		final Soros s;
		try (InputStream input = Numbertext.class.getResourceAsStream("data/" + langfile + ".sor");
				BufferedReader f = new BufferedReader(new InputStreamReader(input, "UTF-8"));) {
			final StringBuilder builder = new StringBuilder();
			String line = null;
			while ((line = f.readLine()) != null) {
				builder.append(line);
				builder.append("\n");
			}

			s = new Soros(builder.toString(), langcode);
			if (modules != null && langfile != null) {
				modules.put(langcode, s);
			}
		} catch (Exception e) {
			return null;
		}
		return s;
	}

	public static String numbertext(String input, String lang) {
		Soros s = (Soros) modules.get(lang);
		if (s == null) {
			s = load(lang.replace('-', '_'), lang);
		}
		if (s == null) {
			s = load(lang.replaceFirst("[-_].*", ""), lang);
		}
		if (s == null) {
			// some exceptional language codes
			// Norwegian....
			Matcher m = LANG_PATTERN_NO.matcher(lang);
			if (m.find()) {
				s = load(m.replaceAll("no"), lang);
			}
		}
		if (s == null) {
			System.out.println("Missing language module: " + lang);
			return null;
		}
		return s.run(input);
	}

	public static String moneytext(String input, String money, String lang) {
		return numbertext(money + " " + input, lang);
	}

	private static void printHelp() {
		System.out.println("Usage: java soros [-l lang] [-p prefix_function] [par1 [par2...]]");
		System.out.println("Parameter: n: number; n-m: range; n-m~s: range with step");
		System.out.println("Example: java -jar numbertext.jar -l en_US 99 # spell out number 99 in English");
		System.out.println("         # spell out different ordinal numbers and number ranges");
		System.out.println("         java -jar numbertext.jar -l en_US -p ordinal 1-10 500 1000-10000~1000");
		System.out.println("         java -jar numbertext.jar -l en_US # print prefix functions of the language module");
		System.out.println("License: GNU LGPL/BSD dual-license");
	}

	public static void main(String[] args) {
		String lang = "en_US";
		if (args.length == 0) {
			printHelp();
			return;
		}

		MenuState state = PARAM;
		boolean missingNumbers = true;
		String prefix = "";
		for (int i = 0; i < args.length; i++) {
			switch (state) {
			case PARAM:
				if (args[i].equals("-l")) {
					state = LANGUAGE;
					break;
				} else if (args[i].equals("-p")) {
					state = PREFIX;
					break;
				} else {
					missingNumbers = false;
					int idx = args[i].indexOf('-', 1);
					if (idx > -1) {
						int b = Integer.parseInt(args[i].substring(0, idx));
						String e = args[i].substring(idx + 1);
						int step = e.indexOf('~', idx);
						int end;
						if (step > -1) {
							end = Integer.parseInt(e.substring(0, step));
							step = Integer.parseInt(e.substring(step + 1));
						} else {
							step = 1;
							end = Integer.parseInt(e);
						}
						for (int j = b; j <= end; j = j + step) {
							System.out.println(numbertext(prefix + j, lang));
						}
					} else {
						System.out.println(numbertext(prefix + args[i], lang));
					}
				}
				break;
			case LANGUAGE:
				lang = args[i];
				if (numbertext("1", lang) == null) {
					System.exit(1);
				}
				state= PARAM;
				break;
			case PREFIX:
				prefix = args[i] + " ";
				state = PARAM;
				break;
			}
		}
		if (missingNumbers) {
			System.out.println(numbertext("help", lang));
		}
	}
}
