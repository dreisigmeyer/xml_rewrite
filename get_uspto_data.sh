#!/bin/bash

# This will download the data files from the USPTO

PATH_TO_XML=`dirname $(readlink -f $0)`
XML_END_YEAR=$1

for (( YEAR=2002; YEAR<=$XML_END_YEAR; YEAR++ ))
do
    NUM_FILES=`wget -qO- --no-parent -A '*_wk*.zip' "https://bulkdata.uspto.gov/data/patent/grant/redbook/bibliographic/$YEAR/" | grep -E "*_wk[0-9]{2}.zip" | wc -l`
    COUNT=`ls "$PATH_TO_XML"/rewriter/raw_xml_files/*pgb"$YEAR"*_wk*.zip 2> /dev/null | wc -l`
    while [ "$COUNT" -lt "$NUM_FILES" ]; do
        `wget -q -r -l1 -nd -P "$PATH_TO_XML"/rewriter/raw_xml_files/ --no-parent -A '*_wk*.zip' "https://bulkdata.uspto.gov/data/patent/grant/redbook/bibliographic/$YEAR/"`
        COUNT=`ls "$PATH_TO_XML"/rewriter/raw_xml_files/*pgb"$YEAR"*_wk*.zip 2> /dev/null | wc -l`
    done
done
