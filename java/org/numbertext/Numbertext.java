/* See numbertext.org
 * 2009-2010 (c) László Németh
 * License: LGPL/BSD dual license */

package org.numbertext;

import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import org.numbertext.Soros;
import java.net.URL;
import java.util.HashMap;

public class Numbertext {
  static HashMap<String, Soros> modules = new HashMap<String, Soros>();

  private static Soros load(String lang, String code) {
    Soros s;
    try {
        URL url = Numbertext.class.getResource("data/" + lang + ".sor");
        BufferedReader f = new BufferedReader(new InputStreamReader(url.openStream(), "UTF-8"));
        StringBuffer st = new StringBuffer();
        String line = null;
        while (( line = f.readLine()) != null) {
            st.append(line);
            st.append(System.getProperty("line.separator"));
        }
        s = new Soros(new String(st));
        if (modules != null && lang != null) modules.put(code, s);
    } catch(Exception e) {
        return null;
    }
    return s;
  }

  public static String numbertext(String input, String lang) {
    Soros s = (Soros) modules.get(lang);
    if (s == null) s = load(lang.replaceFirst("-", "_"), lang);
    if (s == null) s = load(lang.replaceFirst("[-_].*", ""), lang);
    if (s == null) {
        System.out.println("Missing language module: " + lang);
        return null;
    }
    return s.run(input);
  }

  public static String moneytext(String input, String money, String lang) {
    return numbertext(money + " " + input, lang);
  }

  public static void main (String[] args) {
        String lang = "en_US";
        if (args.length == 0) {
            System.out.println("Usage: java soros [-l lang] [-p prefix_function] [par1 [par2...]]");
            System.out.println("Parameter: n: number; n-m: range; n-m~s: range with step");
            System.out.println("Example: java -jar numbertext -l en_US -p ord 1-10 500 1000-10000~1000");
            System.out.println("         java -jar numbertext -l en_US # print prefix functions of the language module");
            System.out.println("License: GNU LGPL/BSD dual-license");
            return;
        }
        int state = 0;
        boolean missingNumbers = true;
        String prefix = "";
        for (int i = 0; i < args.length; i++) {
            if (state != 0) {
                if (state == 1) {
                    lang = args[i];
                        if (numbertext("1", lang) == null)
                            System.exit(1);
                } else if (state == 2) prefix = args[i] + " ";
                state = 0;
                continue;
            }
            if (args[i].equals("-l")) {
                state = 1;
            } else if (args[i].equals("-p")) {
                state = 2;
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
                } else System.out.println(numbertext(prefix + args[i], lang));
            }
        } if (missingNumbers)
            System.out.println(numbertext("help", lang));
  }
}
