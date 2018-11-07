import datetime
import glob
from lxml import etree
import os
import re
import shutil
import subprocess
import warnings


magic_validator = etree.XMLParser(
    dtd_validation=True,
    resolve_entities=False,
    encoding='utf-8',
    recover=True)


def iconvit_damnit(filename):
    """
    Run iconv on files that are being difficult...
    there was some latin-1 in a file so we strip it out.
    """
    iconv_args = [
        'iconv',
        '-f utf-8',
        '-t utf-8',
        '-c',
        '-o', filename + '.holder',
        filename]
    subprocess.run(iconv_args)
    mv_args = ['mv', filename + '.holder', filename]
    subprocess.run(mv_args)


def sedit_damnit(filename):
    """
    Comment out some annoying things in 2002-2004 patents.
    I had to make one big string otherwise sed wouldn't run...
    """
    sed_args = '''
        sed -i -r "s_(<!ENTITY .* SYSTEM .* NDATA .*>)_<!--\\1-->_g" {0}
        '''.format(filename).strip()
    subprocess.run(sed_args, shell=True)


def remove_inventors(in_file, out_file, grant_yr):
    """
    This strips out the inventor information from the USPTO XML files
    :param in_file: original XML file
    :param out_file: file to write to
    :param grant_yr: the grant year of the patent
    :return: the patent number associated with in_file
    """
    if 2002 <= grant_yr <= 2004:
        pat_num_path = './/B110/DNUM/PDAT'
        inventor_path = './/B720'
        applicants_paths = []
    elif 2005 <= grant_yr:
        pat_num_path = './/publication-reference//doc-number'
        inventor_path = './/inventors'
        applicants_paths = ['.//us-applicants', './/applicants']
    try:
        tree = etree.parse(in_file, parser=magic_validator)
    except Exception as etree_err:
        raise etree_err
    try:
        root = tree.getroot()
        pat_num = root.find(pat_num_path).text
    except Exception as e:
        pat_num = False
        print('No patent number associated with ' + in_file)
        print('Exception: ' + str(e))
        return pat_num
    try:
        root.find(inventor_path).clear()
    except AttributeError:  # root.find(inventor_path) is NoneType
        pass
    for applicants_path in applicants_paths:
        try:
            root.find(applicants_path).clear()
        except AttributeError:  # root.find(applicants_path) is NoneType
            pass
    tree.write(out_file, encoding='UTF-8', xml_declaration=True)
    return pat_num


def process_files(directories):
    mod_xml_path = 'rewriter/modified_xml_files/'
    orig_xml_path = 'rewriter/original_xml_files/'
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
        if not 2002 <= grant_year <= current_yr:
            warnings.warn(
                'Patent grant year ' + str(grant_year) +
                ' is not a valid year (currently 2002 to present).')
            continue
        out_directory = mod_xml_path + uspto_name
        shutil.rmtree(out_directory, ignore_errors=True)
        os.mkdir(out_directory)
        cp_args = '''
            cp -r ./rewriter/cleaned_DTDs/* {0}
            '''.format(out_directory).strip()
        subprocess.run(cp_args, shell=True)
        in_directory += '/'
        out_directory += '/'
        for in_file in glob.glob(in_directory + '*.xml'):
            filename = os.path.basename(in_file)
            if 2002 <= grant_year <= 2004:
                sedit_damnit(in_file)
            out_file = out_directory + filename
            pat_num = ''
            try:
                pat_num = remove_inventors(in_file, out_file, grant_year)
            except Exception as e:
                print('Problem in directory ' + in_directory + ':')
                print(e)
                print('Running iconv on the file...')
                try:
                    iconvit_damnit(in_file)
                    pat_num = remove_inventors(in_file, out_file, grant_year)
                    print('Success!')
                except Exception as e_xmllint:
                    print('iconv failed:')
                    print(e_xmllint)
            if pat_num:
                os.rename(in_file, in_directory + pat_num + '.xml')
                os.rename(out_file, out_directory + pat_num + '.xml')
        subprocess.run([
            'tar', '-cjf', orig_xml_path + uspto_name + '.tar.bz2',
            '--directory', orig_xml_path, uspto_name,
            '--remove-files'])
        subprocess.run([
            'tar', '-cjf', mod_xml_path + uspto_name + '.tar.bz2',
            '--directory', mod_xml_path, uspto_name,
            '--remove-files'])
