## Getting the data
The included script _get\_uspto\_data.sh_ will download all the required zip files from the USPTO website.


## Setting up the Python environment
A standard Anaconda Python (https://www.anaconda.com/download/) install was used to develop the code.
The code was developed using Python 3.6.


## Running the code
This requires _sed_ (developed with v4.5) and _iconv_ (developed with v2.27).
From this directory issue  
`nohup ./run_it.sh &`  
and it will put correctly formatted (zipped) XML files in the 
_rewriter/original\_xml\_files_ directory
and correctly formatted (zipped) XML files without inventor information in the 
_rewriter/modified\_xml\_files_ directory.
Within each zip file is all of the granted patents for that term named as prdn.xml.
There is also all of the required DTD, etc files.