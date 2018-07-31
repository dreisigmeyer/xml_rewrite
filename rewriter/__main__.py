import glob
import os
import rewriter


in_dir='original_xml_files'
out_dir = 'modified_xml_files'

for directory in glob.glob(in_dir + '/*'):
    for in_file in glob.glob(directory + '/*'):
        filename = os.path.basename(in_file)
        out_file = out_dir + filename
        rewriter.remove_inventors(in_file, out_file)
