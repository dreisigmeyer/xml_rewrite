See also the README for **shared_python_code**.

## Getting the data
The included script _get\_uspto\_data.sh_ will download all the required zip files from the USPTO website.

## Setting up the Python environment
A standard Anaconda Python (https://www.anaconda.com/download/) install was used to develop the code.
The code was developed using Python 3.6.

## Running the code
This requires _sed_ (developed with v4.5) and _iconv_ (developed with v2.27).
From this directory issue  
`nohup ./run_it.sh NUM_THREADS_TO_USE &`  
and it will put correctly formatted (zipped) XML files in the 
_rewriter/original\_xml\_files_ directory
and correctly formatted (zipped) XML files without inventor information in the 
_rewriter/modified\_xml\_files_ directory.
Within each zip file is all of the granted patents for that term named as prdn.xml.
There is also all of the required DTD, etc files.

## Files
**rewriter.py :**  
This gives the Python functions to process the XML files.  
```
iconvit_damnit(filename):
	Run iconv on files that are being difficult...
	there was some latin-1 in a file so we strip it out.

	filename -- name of the file to run iconv on
```
```
sedit_damnit(filename):
	Comment out some annoying things in 2002-2004 patents.
	I had to make one big string otherwise sed wouldn't run.

	filename -- name of the file to run sed on
```
```
remove_inventors(in_file, out_file, grant_yr):
	This strips out the inventor information from the USPTO XML files

	in_file -- original XML file
	out_file -- file to write to
	grant_yr -- the grant year of the patent
```
```
process_files(directories):
	The main function that preprocessing the raw USPTO XML files.
	It splits the concatenated files into single valid XML files,
	name them after the PRDN and creates a new, separate file with
	the inventor names removed.

	directories -- the directory list containing 
```