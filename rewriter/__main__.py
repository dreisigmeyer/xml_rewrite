import datetime
import glob
import os
import re
from rewriter.rewriter import remove_inventors_2002_to_2004
from rewriter.rewriter import remove_inventors_2005_to_present
import shutil
import warnings

in_dir_path = 'rewriter/original_xml_files/'
out_dir_path = 'rewriter/modified_xml_files/'
grant_year_re = re.compile('i?pgb([0-9]{8})')  # To get the grant year from the GBD file name

now = datetime.datetime.now()
current_yr = now.year + 1
for in_directory in glob.glob(in_dir_path + '*'):
    uspto_name = os.path.basename(in_directory)
    grant_year = int(grant_year_re.match(uspto_name).group(1)[:4])
    if grant_year not in range(2002, current_yr):
        warnings.warn('Patent grant year ' + str(grant_year) + ' is not a valid year (currently 2002 to present).')
        continue
    out_directory = out_dir_path + uspto_name
    shutil.rmtree(out_directory)  # if directory is already there
    os.mkdir(out_directory)
    in_directory += '/'
    out_directory += '/'
    for in_file in glob.glob(in_directory + '*'):
        filename = os.path.basename(in_file)
        out_file = out_directory + filename
        if 2002 <= grant_year <= 2004:
            pat_num = remove_inventors_2002_to_2004(in_file, out_file)
        else:
            pat_num = remove_inventors_2005_to_present(in_file, out_file)
        os.rename(in_file, in_directory + pat_num + '.xml')
        os.rename(out_file, out_directory + pat_num + '.xml')
