# Soros interpreters for C++11, Java, JavaScript and Python

[![Build Status](https://travis-ci.org/Numbertext/libnumbertext.png?branch=master)](https://travis-ci.org/Numbertext/libnumbertext)

```
Language-neutral NUMBERTEXT and MONEYTEXT functions for LibreOffice Calc

version 1.0.10 (2022-04-02)

Numbertext LibreOffice extension,
Soros programming language specification (draft) and IDE*,
Soros interpreter in Python: pythonpath/Soros.py,
Soros interpreter in JavaScript: Soros.js*
Soros interpreter in Java: see NUMBERTEXT.org

* Not in LibreOffice Numbertext extension, see http://NUMBERTEXT.org.

Copyright: 2009-2021 (C) László Németh (nemeth at numbertext dot org)
License: LGPL-3+/Modified BSD dual-license

Numbertext language data (Soros programs):
License: LGPL-3+/Modified BSD dual-license (except Serbian)

Copyright: 2009-2021 (C) László Németh et al. (see AUTHORS)
Bulgarian: 2018 (C) Mihail Balabanov (m dot balabanov at gmail dot com)
Croatian: 2014 (C) Mihovil Stanić (mihovil dot stanic at gmail dot com)
Hebrew module: 2010 (C) Alex Bodnaru (alexbodn at 012 dot net dot il)
French (Belgian and Swiss): 2009 (C) Olivier Ronez
Galician: 2018 (C) Adrián Chaves (adrian at chaves dot io)
Indonesian: 2010 (C) Eko Prasetiyo (ekoprasetiyo at gmail)
Latvian: 2012 (C) Asterisks at OOo Wiki
Luganda: 2020 (C) Phillip Samuel <phillipsamuelk3 at gmail dot com>
Luxembourgish: 2009 (C) Michel Weimerskirch (michel at weimerskirch dot net)
Marathi: 2020 (C) Ankur Heramb Joshi
Portuguese: 2009 (C) Eduardo Moreno (emoreno at tokonhu dot com)
Turkish: 2009 (C) Randem

Serbian: 2009 (C) Goran Rakić (grakic at devbase dot net)
Korean: 2019 (C) DaeHyun Sung (sungdh86+git at gmail dot com)
License: CC BY-SA/LGPL-3+/Modified BSD tri-license


* Note: for full distribution with specifications, IDE and JavaScript
  implementation, see http://NUMBERTEXT.org

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied.

= Supported languages in this version =

af	Africaans
bg	Bulgarian
ca	Catalan
cs	Czech
da	Danish
de	German
de-CH	Swiss Standard German orthography (dreissig instead of dreißig)
de-LI	Swiss Standard German orthography (dreissig instead of dreißig)
el	Greek
en	English (one hundred one)
en-AU	English (one hundred and one)
en-GB	English (one hundred and one)
en-IE	English (one hundred and one)
en-IN	English with Indian numbering system (lakh = 100.000, crore = 10^7)
en-NZ	English (one hundred and one)
eo	Esperanto
es	Spanish
et	Estonian
fa	Persian (Farsi)
fi	Finnish
fr	French
fr-BE	Belgian French
fr-CH	Swiss French
ga	Irish
gl	Galician
he	Hebrew
hr	Croatian
hu	Hungarian
id	Indonesian
is	Icelandic
it	Italian
ja	Japanese
ko	Korean
ko-KR	Korean (South)
ko-KP	Korean (North)
lb	Luxembourgish
lg	Luganda
lt	Lithuanian
lv	Latvian
mr	Marathi
ms	Malaysian
mt	Maltese
mul	note symbols, e.g. \*, †, ‡, ... for multiple languages
nb	Norwegian Bokmål
nl	Dutch
nn	Norwegian Nynorsk
no	Norwegian (Bokmål)
pl	Polish
pt	Portuguese
pt-BR	Brazilian Portuguese
ro	Romanian
ru	Russian
sh	Serbian (Latin)
sl	Slovenian
sq	Albanian
sr	Serbian (Cyrillic)
sv	Swedish
th	Thai
tr	Turkish
uk	Ukrainian
vi	Vietnamese
zh	Chinese (simplified)

Old number systems:

hu-Hung		Old Hungarian Script (also word transliteration)
Roman		Roman numbers
Roman-large	Roman numbers for very large numbers
		using parenthesized syntax
Suzhou		Chinese Suzhou numerals

= Build C++11 =

autoreconf -i
./configure
make
make check

# test it

src/spellout -l en 123

= Build Java jar =

cd java
make

= Build and using LibreOffice Extension =

make -f Makefile.orig lo

and install the *.oxt package by
Tools->Extension Manager->Add of LibreOffice.

After restarting OpenOffice.org/LibreOffice, there are
two new Calc functions,
NUMBERTEXT() and MONEYTEXT().

Examples:

=NUMBERTEXT(25)
=NUMBERTEXT(25;"th-TH")
=MONEYTEXT(25)
=MONEYTEXT(25;"USD")
=MONEYTEXT(25;"CNY";"zh-ZH")

Module Help (enlarge the row to see all lines), containing
available prefix functions of the module:

= NUMBERTEXT("help")
= NUMBERTEXT("help";"de")

= Development =

See doc/addnewlocale.txt and doc/sorosspec.odt

For general Calc and (portable Excel) Add-In developments, see
Jan Holst Jensen's excellent Add-in example and documentation:

http://biochemfusion.com/doc/Calc_addin_howto.html

== Integrated development environment ==

There is a JavaScript/HTML IDE in this distribution. 

Use the online version: http://numbertext.org/Soros.html or
build it with

make -f Makefile.orig

and open web/webroot/Soros.html in a JavaScript capable browser,

= Test =

make -f Makefile.orig check

test/thaicheck.ods is a simple test of the equivalence of
the Soros implementation of Thai number to number name conversion
and BAHTTEXT function.
```
