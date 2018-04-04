#!/bin/sh
# Extract language data for default decimal places from OpenOffice.org language resources
$OODIR=$1
#############
cat `ls $OODIR/i18npool/source/localedata/data/*.xml | sort` | awk '/<Currency .*default/{if($0~/default=.true/)def=1;else def=0}{if(match($0,"<(CurrencyID|DecimalPlaces)>([^<]*)<",a)){b[a[1]]=a[2];if(a[1]=="DecimalPlaces")print "\"" b["CurrencyID"]"\":" a[2]}}' | sort | uniq | awk 'NR==1{printf "places = { %s", $0; next}{print ","; printf "%s", $0}END{print "}"}'>src/places.py 
