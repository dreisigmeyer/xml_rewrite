import glob
from multiprocessing import Process
import random
from rewriter.rewriter import process_files
import sys


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
