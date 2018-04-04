# use this on linux with ooo build env
idlc -I $SOLARVER/$INPATH/idl XNumberText.idl
regmerge ../rdb/sample.rdb /UCR  XNumberText.urd

rem use this on windows with ooo build env
rem guw.pl idlc -I $SOLARVER/$INPATH/idl XNumberText.idl
rem guw.pl regmerge ../rdb/sample.rdb /UCR  XNumberText.urd
