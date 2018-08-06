#!/usr/bin/env bash


function clean_dtds {
    # The DTD files need to be modified for the modified XML files we deal with
    # The first one works for 2005-present (as of 2014)
    # The rest work for 2002-2004
    sed -i -r 's_(<!ELEMENT us-patent-grant.*>)_<!--\1-->\n<!ELEMENT us-patent-grant (us-bibliographic-data-grant , abstract*, sequence-list-doc?)>_' $1
    sed -i -r 's_(<!ELEMENT PATDOC.*>)_<!--\1-->\n<!ELEMENT PATDOC (SDOBI,SDOAB?,SDODE,SDOCL*,SDODR?,SDOCR?)>_' $2
#    sed -i -r 's_(FILE[ ]*ENTITY)[ ]*(#REQUIRED)(.*)_\1 #IMPLIED \3_g' $2
#    sed -i -r 's_(<!ELEMENT CHEM-US.*>)_<!--\1-->\n<!ELEMENT CHEM-US \(CHEMCDX?,CHEMMOL?,EMI?\)>_' $2
#    sed -i -r 's_(<!ELEMENT MATH-US.*>)_<!--\1-->\n<!ELEMENT MATH-US \(MATHEMATICA?,MATHML?,EMI?\)>_' $2
#    sed -i -r 's_(<!ELEMENT BTEXT.*>)_<!--\1-->\n<!ELEMENT BTEXT \(H | PARA | CWU | IMG\)*>_' $2
}


cp -r ./rewriter/DTDs/* ./rewriter/cleaned_DTDs
clean_dtds ./rewriter/cleaned_DTDs/\*.dtd ./rewriter/cleaned_DTDs/ST32-US-Grant-025xml.dtd

NUM_PY_THREADS=4
python -m rewriter $NUM_PY_THREADS

# for FOLDER_NAME in ./rewriter/original_xml_files/*; do
#     zip -qr "$FOLDER_NAME"
# done
# for FOLDER_NAME in ./rewriter/modified_xml_files/*; do
#     zip -qr "$FOLDER_NAME"
# done