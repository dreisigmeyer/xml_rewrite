import xml.etree.ElementTree as ET


def remove_inventors(in_file, out_file):
    """
    This strips out the inventor information from the USPTO XML files
    :param in_file: original XML file
    :param out_file: file to write to
    :return: outputs rewritten XML file to out_file
    """
    tree = ET.parse(in_file)

    tree.write(out_file)
