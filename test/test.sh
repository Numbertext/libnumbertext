#!/bin/bash

if [ -d ../../_build/../tests ]; then
  TESTDIR="../../tests"
else
  TESTDIR="."
fi

TEMPDIR="./testSubDir"

if [ ! -d $TEMPDIR ]; then
  mkdir $TEMPDIR
fi

PYTHONPATH=../pythonpath python test.py $TESTDIR/$1 $TESTDIR/$2 $TEMPDIR/test.out$$
diff $TEMPDIR/test.out$$ $TESTDIR/$3 || exit 1
