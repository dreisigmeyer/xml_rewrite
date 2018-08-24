#!/usr/bin/env bash


function clean_dtds {
    # The truncated XML files need to be edited.
    # The first one is for 2005-present (as of 2014).
    # The second one is for 2002-2004.
    sed -i -r 's_(<!ELEMENT us-patent-grant.*>)_<!--\1-->\n<!ELEMENT us-patent-grant (us-bibliographic-data-grant , abstract*, sequence-list-doc?)>_' $1
    sed -i -r 's_(<!ELEMENT PATDOC.*>)_<!--\1-->\n<!ELEMENT PATDOC (SDOBI,SDOAB?,SDODE,SDOCL*,SDODR?,SDOCR?)>_' $2
}

if [[ $# -eq 0 ]] ; then
	NUM_PY_THREADS=1
elif [[ $# -eq 1 ]] ; then
	NUM_PY_THREADS=$1
else
	echo 'Wrong number of parameters passed to xml_rewrite: only NUM_PY_THREADS needed.'
    exit 1
fi

cp -r ./rewriter/DTDs/* ./rewriter/cleaned_DTDs
clean_dtds ./rewriter/cleaned_DTDs/\*.dtd ./rewriter/cleaned_DTDs/ST32-US-Grant-025xml.dtd

python -m rewriter $NUM_PY_THREADS
