#!/usr/bin/env bash

# will get our USPTO XML files ready for processing
unzip_and_csplit(){
    OUTDIR="${1%_*}"
    FILENAME=$(basename -- "$OUTDIR")
#    echo "$1"
#    echo "$OUTDIR"
#    echo "$FILENAME"
    unzip -qq -o -j "$1" -d "$OUTDIR"
    csplit -sz -f "$OUTDIR/" -b '%d.xml' "$OUTDIR/$FILENAME.xml" '/^<?xml/' '{*}'
}
#./get_uspto_data.sh

# run this in parallel with N processes
N=4
(
for FILE in ./rewriter/raw_xml_files/*.zip
do
    ((i=i%N)); ((i++==0)) && wait
    unzip_and_csplit "$FILE" &
done
)

#python -m rewriter