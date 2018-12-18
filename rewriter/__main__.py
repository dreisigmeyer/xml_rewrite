import glob
from multiprocessing import Process
import os
import random
from rewriter.rewriter import process_files
from shared_python_code.utility_functons import split_seq
import sys

THIS_DIR = os.path.dirname(__file__)

number_of_processes = int(sys.argv[1])
in_dir_path = THIS_DIR + '/raw_xml_files/'
in_directories = glob.glob(in_dir_path + '*')
random.shuffle(in_directories)  # Newer years have more granted patents
directories_list = split_seq(in_directories, number_of_processes)
procs = []
for chunk in directories_list:
    p = Process(target=process_files, args=(chunk,))
    procs.append(p)
    p.start()
