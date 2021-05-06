#!/bin/bash

TESTDIR="."

TEMPDIR="./testSubDir"

if [ ! -d $TEMPDIR ]; then
  mkdir $TEMPDIR
fi

PYTHONPATH=../src/ python test.py $TESTDIR/$1 $TESTDIR/$2 $TEMPDIR/test.out$$
diff -u $TEMPDIR/test.out$$ $TESTDIR/$3 || exit 1
