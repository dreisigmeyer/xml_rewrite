import datetime
import glob
from multiprocessing import Process
import os
import random
import re
from rewriter.rewriter import remove_inventors
import shutil
import subprocess
import sys
import warnings


def split_seq(seq, num_processes):
    """
    Slices a list into number_of_processes pieces
    of roughly the same size
    """
    num_files = len(seq)
    if num_files < num_processes:
        num_processes = num_files
    size = num_processes
    newseq = []
    splitsize = 1.0 / size * num_files
    for i in range(size):
        newseq.append(
            seq[int(round(i * splitsize)):int(round((i + 1) * splitsize))])
    return newseq


def xmllint_damnit(filename):
    """
    Run xmllint on files that are being difficult...
    there was some latin-1 in a file
    """
    split_args = [
        'xmllint',
        '--encode', 'utf8',
        '--output', filename,
        filename]
    subprocess.run(split_args)


def process_files(directories):
    mod_xml_path = 'rewriter/modified_xml_files/'
    grant_year_re = re.compile('i?pgb([0-9]{8})')
    now = datetime.datetime.now()
    current_yr = now.year + 1
    for raw_directory in directories:
        split_args = [
            './bash_functions.sh',
            'unzip_and_csplit',
            raw_directory]
        unzip_and_csplit = subprocess.run(split_args, stdout=subprocess.PIPE)
        in_directory = unzip_and_csplit.stdout.decode("ascii").strip()
        uspto_name = os.path.basename(in_directory)
        grant_year = int(grant_year_re.match(uspto_name).group(1)[:4])
        if grant_year not in range(2002, current_yr):
            warnings.warn(
                'Patent grant year ' + str(grant_year) +
                ' is not a valid year (currently 2002 to present).')
            continue
        out_directory = mod_xml_path + uspto_name
        shutil.rmtree(out_directory, ignore_errors=True)
        os.mkdir(out_directory)
        tar_orig = in_directory
        in_directory += '/'
        tar_mod = out_directory
        out_directory += '/'
        for in_file in glob.glob(in_directory + '*.xml'):
            filename = os.path.basename(in_file)
            out_file = out_directory + filename
            pat_num = ''
            try:
                pat_num = remove_inventors(in_file, out_file, grant_year)
            except Exception as e:
                print(e)
                print('Problem in directory ' + in_directory)
                print('Trying to xmllint the file...')
                try:
                    xmllint_damnit(in_file)
                    pat_num = remove_inventors(in_file, out_file, grant_year)
                except Exception as e_xmllint:
                    print('xmllint failed:')
                    print(e_xmllint)
            finally:
                print('\n')
            if pat_num:
                os.rename(in_file, in_directory + pat_num + '.xml')
                os.rename(out_file, out_directory + pat_num + '.xml')
        subprocess.run([
            'tar', '-cjf', tar_orig + '.tar.bz2', tar_orig, '--remove-files'])
        subprocess.run([
            'tar', '-cjf', tar_mod + '.tar.bz2', tar_mod, '--remove-files'])


number_of_processes = int(sys.argv[1])
in_dir_path = 'rewriter/raw_xml_files/'
in_directories = glob.glob(in_dir_path + '*')
random.shuffle(in_directories)  # Newer years have more granted patents
directories_list = split_seq(in_directories, number_of_processes)
procs = []
for chunk in directories_list:
    p = Process(target=process_files, args=(chunk,))
    procs.append(p)
    p.start()
