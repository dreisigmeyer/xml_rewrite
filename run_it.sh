#!/usr/bin/env bash
#source $HOME/perl5/perlbrew/etc/bashrc
#perlbrew use perl-5.28.0

# will get our USPTO XML files ready for processing
unzip_and_csplit(){
    OUTDIR='./rewriter/original_xml_files'
    INDIR="${1%_*}"
    FILENAME=$(basename -- "$INDIR")
    unzip -qq -o -j "$1" -d "$OUTDIR/$FILENAME"
    # there's HTML etc in the XML files
    perl -w gbd_cleaner.pl "$OUTDIR/$FILENAME/$FILENAME.xml"
    csplit -sz -f "$OUTDIR/$FILENAME/" -b '%d.xml' "$OUTDIR/$FILENAME/$FILENAME.xml" '/^<?xml/' '{*}'
    rm "$OUTDIR/$FILENAME/$FILENAME.xml"
    rm "$OUTDIR/$FILENAME/"*.txt
}

# downloads the USPTO data 2002-2017
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