# import xml.etree.ElementTree as ElementTree
from lxml import etree


magic_validator = etree.XMLParser(
    dtd_validation=True,
    resolve_entities=False,
    encoding='utf-8',
    recover=True)


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
    root = tree.getroot()
    try:
        pat_num = root.find(pat_num_path).text
    except Exception:
        pat_num = False
    if not pat_num:
        print('No patent number associated with ' + in_file)
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
