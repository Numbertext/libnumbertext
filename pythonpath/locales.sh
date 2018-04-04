#!/bin/sh
echo "$@" | sed 's/ /,/g' | sed "s/[a-zA-Z_]*/'&':1/g;s/^/locales = {/;s/$/ }/"
