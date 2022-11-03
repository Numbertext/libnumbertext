#!/bin/bash

SPELLOUT=../src/spellout

TESTDIR="."

TEMPDIR="./testSubDir"

if [ ! -d $TEMPDIR ]; then
  mkdir $TEMPDIR
fi

$SPELLOUT -l $TESTDIR/../data/$1 $(sed -n 's/ #.*$//;/^[^#]/p' $2) >$TEMPDIR/test.out$$
diff -u $TEMPDIR/test.out$$ $TESTDIR/$3 || exit 1
