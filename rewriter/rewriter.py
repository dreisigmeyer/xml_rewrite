# import xml.etree.ElementTree as ElementTree
from lxml import etree
import warnings

invalid_validator = etree.XMLParser(
    dtd_validation=True,
    resolve_entities=False)
magic_validator = etree.XMLParser(
    dtd_validation=True,
    resolve_entities=False,
    recover=True)


def remove_inventors_2002_to_2004(in_file, out_file):
    """
    This strips out the inventor information from the USPTO XML files
    :param in_file: original XML file
    :param out_file: file to write to
    :return: the patent number associated with in_file
    """
    pat_num_path = './/B110/DNUM/PDAT'
    inventor_path = './/B720'
    try:
        tree = etree.parse(in_file, parser=invalid_validator)
    except Exception as e:
        print(e + '==> Trying the magic parser...')
        try:
            tree = etree.parse(in_file, parser=magic_validator)
        except Exception as e:
            print(e)
            raise
    root = tree.getroot()
    pat_num = root.find(pat_num_path).text
    if not pat_num:
        warnings.warn('No patent number associated with ' + in_file)
        return False
    try:
        root.find(inventor_path).clear()
    except AttributeError:  # root.find(inventor_path) is NoneType
        pass
    tree.write(out_file, encoding='UTF-8', xml_declaration=True)
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
    try:
        tree = etree.parse(in_file, parser=invalid_validator)
    except Exception as e:
        print(e + '==> Trying the magic parser...')
        try:
            tree = etree.parse(in_file, parser=magic_validator)
        except Exception as e:
            print(e)
            raise
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
    tree.write(out_file, encoding='UTF-8', xml_declaration=True)
    return pat_num
