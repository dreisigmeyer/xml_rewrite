#!/bin/bash

# This will download the data files from the USPTO

PATH_TO_XML=`dirname $(readlink -f $0)`
for YEAR in {2002..2017}
do
    COUNT=`ls rewriter/raw_xml_files/*pgb"$YEAR"*_wk*.zip 2> /dev/null | wc -l`
    while [ "$COUNT" -lt 52 ]; do
        `wget -q -r -l1 -nd -P "$PATH_TO_XML"/rewriter/raw_xml_files/ --no-parent -A '*_wk*.zip' "https://bulkdata.uspto.gov/data/patent/grant/redbook/bibliographic/$YEAR/"`
        COUNT=`ls rewriter/raw_xml_files/*pgb"$YEAR"*_wk*.zip 2> /dev/null | wc -l`
    done
done
