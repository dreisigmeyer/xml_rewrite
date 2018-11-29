#!/usr/bin/env bash

# Function use in rewriter/rewriter.py/process_files

function unzip_and_csplit {
    # will get our USPTO XML files ready for processing
    OUTDIR='./rewriter/original_xml_files'
    INDIR="${1%_*}"
    FILENAME=$(basename -- "$INDIR")
    unzip -qq -o -j "$1" -d "$OUTDIR/$FILENAME"
    # there's HTML etc in the XML files
    csplit -sz -f "$OUTDIR/$FILENAME/" -b '%d.xml' "$OUTDIR/$FILENAME/$FILENAME.xml" '/^<?xml/' '{*}'
    rm "$OUTDIR/$FILENAME/$FILENAME.xml"
    rm -f "$OUTDIR/$FILENAME/"*.txt
    rm -f "$OUTDIR/$FILENAME/"*.html
    cp -r ./rewriter/cleaned_DTDs/* "$OUTDIR/$FILENAME/"
    echo "$OUTDIR/$FILENAME"
}

"$@"