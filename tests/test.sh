#!/bin/bash

SPELLOUT=../src/spellout

TESTDIR="`dirname $0`"

TEMPDIR="./testSubDir"

if [ ! -d $TEMPDIR ]; then
  mkdir $TEMPDIR
fi

$SPELLOUT -l $MODULES/$1 $(sed -n 's/ #.*$//;/^[^#]/p' $TESTDIR/$2) >$TEMPDIR/test.out$$
diff -u $TEMPDIR/test.out$$ $TESTDIR/$3 || exit 1
