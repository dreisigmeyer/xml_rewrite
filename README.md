## Getting the data
The included script _get\_uspto\_data.sh_ will download all the required zip files from the USPTO website.


## Setting up the Python environment
A standard Anaconda Python (https://www.anaconda.com/download/) install was used to develop the code.
The code was developed using Python 3.6.


## xmllint
You'll need to have xmllint installed.
Some of the XML files have latin-1 encoded characters.

## Running the code
From this directory issue  
`nohup ./run_it.sh &`  
and it will put correctly formatted (zipped) XML files in the 
_rewriter/original\_xml\_files_ directory
and correctly formatted (zipped) XML files without inventor information in the 
_rewriter/modified\_xml\_files_ directory.