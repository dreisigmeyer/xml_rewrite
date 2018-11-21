import glob
from multiprocessing import Process
import random
from rewriter.rewriter import process_files
from shared_python_code.utility_functons import split_seq
import sys


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
