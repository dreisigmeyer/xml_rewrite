#!/usr/bin/env bash

function clean_dtds {
    # The DTD files need to be modified for the modified XML files we deal with
    # The first one works for 2005-present (as of 2014)
    # The rest work for 2002-2004
    sed -i -r 's_(<!ELEMENT us-patent-grant.*>)_<!--\1-->\n<!ELEMENT us-patent-grant (us-bibliographic-data-grant , abstract*, sequence-list-doc?)>_' $1
    sed -i -r 's_(<!ELEMENT PATDOC.*>)_<!--\1-->\n<!ELEMENT PATDOC (SDOBI,SDOAB?,SDODE,SDOCL*,SDODR?,SDOCR?)>_' $2
    sed -i -r 's_(FILE[ ]*ENTITY)[ ]*(#REQUIRED)(.*)_\1 #IMPLIED \3_g' $2
    sed -i -r 's_(<!ELEMENT CHEM-US.*>)_<!--\1-->\n<!ELEMENT CHEM-US \(CHEMCDX?,CHEMMOL?,EMI?\)>_' $2
    sed -i -r 's_(<!ELEMENT MATH-US.*>)_<!--\1-->\n<!ELEMENT MATH-US \(MATHEMATICA?,MATHML?,EMI?\)>_' $2
    sed -i -r 's_(<!ELEMENT BTEXT.*>)_<!--\1-->\n<!ELEMENT BTEXT \(H | PARA | CWU | IMG\)*>_' $2
}

function unzip_and_csplit {
    # will get our USPTO XML files ready for processing
    OUTDIR='./rewriter/original_xml_files'
    INDIR="${1%_*}"
    FILENAME=$(basename -- "$INDIR")
    unzip -qq -o -j "$1" -d "$OUTDIR/$FILENAME"
    # there's HTML etc in the XML files
    perl -w gbd_cleaner.pl "$OUTDIR/$FILENAME/$FILENAME.xml"
    csplit -sz -f "$OUTDIR/$FILENAME/" -b '%d.xml' "$OUTDIR/$FILENAME/$FILENAME.xml" '/^<?xml/' '{*}'
    rm "$OUTDIR/$FILENAME/$FILENAME.xml"
    rm -f "$OUTDIR/$FILENAME/"*.txt
    rm -f "$OUTDIR/$FILENAME/"*.html
}

# downloads the USPTO data 2002-2017
#./get_uspto_data.sh

# run this in parallel with N processes
N=4
for FILE in ./rewriter/raw_xml_files/*.zip
do
    ((i=i%N)); ((i++==0)) && wait
    unzip_and_csplit "$FILE" &
done
wait

for FOLDER_NAME in ./rewriter/original_xml_files/*; do
    cp -r ./rewriter/DTDs/* "$FOLDER_NAME"
    clean_dtds "$FOLDER_NAME"/\*.dtd "$FOLDER_NAME"/ST32-US-Grant-025xml.dtd
done

python -m rewriter

for FOLDER_NAME in ./rewriter/original_xml_files/*; do
    zip -q -r "$FOLDER_NAME".zip "$FOLDER_NAME"
done

for FOLDER_NAME in ./rewriter/modified_xml_files/*; do
    cp -r ./rewriter/DTDs/* "$FOLDER_NAME"
    clean_dtds "$FOLDER_NAME"/\*.dtd "$FOLDER_NAME"/ST32-US-Grant-025xml.dtd
    zip -q -r "$FOLDER_NAME".zip "$FOLDER_NAME"
done