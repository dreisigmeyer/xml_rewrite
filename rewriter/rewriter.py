import xml.etree.ElementTree as ElementTree
import warnings


def remove_inventors_2002_to_2004(in_file, out_file):
    """
    This strips out the inventor information from the USPTO XML files
    :param in_file: original XML file
    :param out_file: file to write to
    :return: the patent number associated with in_file
    """
    pat_num_path = './/B110/DNUM/PDAT'
    inventor_path = './/B720'
    tree = ElementTree.parse(in_file)
    root = tree.getroot()
    pat_num = root.find(pat_num_path).text
    if not pat_num:
        warnings.warn('No patent number associated with ' + in_file)
        return False
    try:
        root.find(inventor_path).clear()
    except AttributeError:  # root.find(inventor_path) is NoneType
        pass
    tree.write(out_file, encoding="UTF-8", xml_declaration=True)
    return pat_num


def remove_inventors_2005_to_present(in_file, out_file):
    """
    This strips out the inventor information from the USPTO XML files
    :param in_file: original XML file
    :param out_file: file to write to
    :return: the patent number associated with in_file
    """
    pat_num_path = './/publication-reference//doc-number'
    inventor_path = './/inventors'
    applicants_paths = ['.//us-applicants', './/applicants']
    tree = ElementTree.parse(in_file)
    root = tree.getroot()
    pat_num = root.find(pat_num_path).text
    if not pat_num:
        warnings.warn('No patent number associated with ' + in_file)
        return False
    try:
        root.find(inventor_path).clear()
    except AttributeError:  # root.find(inventor_path) is NoneType
        pass
    for applicants_path in applicants_paths:
        try:
            root.find(applicants_path).clear()
        except AttributeError:  # root.find(applicants_path) is NoneType
            pass
    tree.write(out_file, encoding="UTF-8", xml_declaration=True)
    return pat_num
