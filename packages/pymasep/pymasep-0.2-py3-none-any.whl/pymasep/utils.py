"""
Miscellaneous utility functions
"""
import re
import shutil
from typing import Any, Union, List, Dict, Tuple, Set, Iterator
import logging
import importlib
import os
import fnmatch
from inspect import ismethod
import xml.etree.ElementTree as xmlET
from unidecode import unidecode

import pymasep.circular_head_list

native_xml_types = {
    None: None,
    'int': int,
    'str': str,
    'list': list,
    'tuple': tuple,
    'set': set,
    'dict': dict,
    'type': type,
    'bool': bool
}
"""
Corresponding string to python native types. {str->type}
"""

from_xml_types = {
    'CircularHeadList': pymasep.circular_head_list.CircularHeadList
}
"""
Pymas objects containing from_xml() method. Use to create object from an xml. {str->type}
"""


def import_from_dotted_path(dotted_names: str) -> Any:
    """
    Import a class from a string
    ``import_from_dotted_path('foo.bar')`` <=> ``from foo import bar; return bar``

    :param dotted_names: String representing a class inside a module
    :return: the class represented by `dotted_names`

    """
    module_name, class_name = dotted_names.rsplit('.', 1)
    module = importlib.import_module(module_name)
    handler_class = getattr(module, class_name)
    return handler_class


def classname(obj: Any) -> str:
    """
    Get the full name (with module) of an object's class

    License: ?

    Thanks clbarnes https://gist.github.com/clbarnes/edd28ea32010eb159b34b075687bb49e

    :param obj: The object from which to obtain the name
    :return: a string containing the full class name
    """

    cls = type(obj)
    module = cls.__module__
    name = cls.__qualname__
    if module is not None and module != "__builtin__":
        name = module + "." + name
    return name


def setup_logger(name: str, path: str, log_filename: str, level: Union[int, str] = logging.WARNING) -> logging.Logger:
    """
    To set up as many loggers as you want

    Licence: CC BY-SA 4.0

    Thanks eos87 https://stackoverflow.com/questions/11232230/logging-to-two-files-with-different-settings

    :param name: Name of the logger
    :param path: path to save the log_file
    :param log_filename: filename of the log file
    :param level: log level messages to log as str or int. Default is logging.WARNING.
    :return: An instance of a Logger
    """

    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s() - %(message)s'
    formatter = logging.Formatter(format_str)

    os.makedirs(path, exist_ok=True)
    handler = logging.FileHandler(os.path.join(path, log_filename), mode='w')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def close_logger(logger) -> None:
    """
    Close a logger instance by removing all handlers and close them.

    :param logger: Logger to close
    """
    handlers = logger.handlers[:]
    for handler in handlers:
        logger.removeHandler(handler)
        handler.close()


def remove_recursive_file(path: str, pattern: str) -> None:
    """
    Remove files with a certain pattern inside path and subdirectories

    Copyright © 2022 thisPointer

    Thanks https://thispointer.com/python-how-to-remove-files-by-matching-pattern-wildcards-certain-extensions-only/

    :param path: Path to recursively search in.
    :param pattern: The file patterns to delete.
    :raise PermissionError: In windows (file still open ?) TO REFACTOR
    :raise OSError: if error occurs during deletion
    """
    # Get a list of all files in directory
    for rootDir, subdirs, filenames in os.walk(path):
        # Find the files that match the given pattern.
        for subdir in fnmatch.filter(subdirs, pattern):
            try:
                shutil.rmtree(os.path.join(rootDir, subdir))
            except OSError as e:
                raise OSError("Error while deleting subdir") from e
        for filename in fnmatch.filter(filenames, pattern):
            try:
                os.remove(os.path.join(rootDir, filename))
            except PermissionError:
                print(os.path.join(rootDir, filename))
            except OSError as e:
                raise OSError("Error while deleting file") from e


def native_type_to_xml(native: Union[List, Set, Tuple, Dict, Any]) -> xmlET.Element:
    """
    Transform a python native type (simple (`int`, `float`, ...) or complex (`list`, `set`, `tuple`, `dict`)) to xml.
    Complex types are serialized with ``<complex_type><item [key="KEY1"]>...</item></complex_type>``.
    If the instance has a ``to_xml()`` method, this method is called .
    `dict` object are transformed to xml contains the attribute `key`.
    an empty string is represented by '<str content="empty" />

    :param native: the instance of a native type
    :return: the instance as xml
    """
    if method_exists(native, 'to_xml'):
        result = native.to_xml()
    else:
        result = xmlET.Element(type(native).__name__)
        if type(native) is list or type(native) is set or type(native) is tuple:
            for item in native:
                sub_element = xmlET.SubElement(result, 'item')
                sub_element.append(native_type_to_xml(item))
        else:
            if type(native) is dict:
                for item in native.items():
                    sub_element = xmlET.SubElement(result, 'item')
                    sub_element.attrib['key'] = item[0]
                    sub_element.append(native_type_to_xml(item[1]))
            else:
                if type(native) is str:
                    if native == '':
                        result.attrib['content'] = 'empty'
                result.text = str(native)
    return result


def native_type_to_xml_none(value_type: type) -> xmlET.Element:
    """
    transform a python type (simple (`int`, `float`, ...) or complex (`list`, `set`, `tuple`, `dict`)) to an empty XML

    :param value_type: a python type.
    :return: an XML instance with the format ``<'value_type' />``
    """
    return xmlET.Element(value_type.__name__)


def native_type_from_xml(xml_node: xmlET.Element) -> Tuple[Union[None, Any], type]:
    """
    Transform a xml to a python native type (simple (`int`, `float`, ...) or complex (`list`, `set`, `tuple`, `dict`)).
    The format for complex type is ``<complex_type><item [key="KEY1"]>...</item></complex_type>``.
    Note : an empty string is represented by '<str content="empty" />

    :param xml_node: the xml instance with expected format.
    :return: an instance of the python native type
    """
    value_type = native_xml_types.get(xml_node.tag, None)
    if value_type:
        if xml_node.text is None and len(list(xml_node)) == 0:
            if xml_node.tag not in ['list', 'tuple', 'set', 'dict']:
                if (xml_node.tag == 'str'
                        and 'content' in xml_node.attrib
                        and xml_node.attrib['content'] == 'empty'):
                    result = ''
                else:
                    result = None
            else:
                result = native_xml_types[xml_node.tag]()
        else:
            if xml_node.tag == 'list' or xml_node.tag == 'tuple' or xml_node.tag == 'set':
                result = []
                for item in xml_node:
                    if item.tag == 'item':
                        sub_value, _ = native_type_from_xml(xml_node=item[0])
                        result.append(sub_value)
                result = (native_xml_types[xml_node.tag])(result)
            else:
                if xml_node.tag == 'dict':
                    result = {}
                    for item in xml_node:
                        if item.tag == 'item':
                            sub_value, _ = native_type_from_xml(xml_node=item[0])
                            result[item.attrib['key']] = sub_value
                else:
                    if xml_node.text[0:6] == '<class':
                        substring = re.search("(?<=')[^']+(?=')", xml_node.text).group(0)
                        result = import_from_dotted_path(substring)
                    else:
                        result = (native_xml_types[xml_node.tag])(xml_node.text)
    else:
        result = xml_node
        value_type = xmlET.Element
    return result, value_type


def method_exists(instance: object, method: str) -> bool:
    """
    Test if a method exists for an object instance

    Licence: CC BY-SA 3.0.

    Thanks https://itqna.net/questions/15635/how-check-if-method-exists-class-python

    :param instance: The instance to search
    :param method: the method (as string) to search
    :return: True if the methode exists in the instance
    """
    return hasattr(instance, method) and ismethod(getattr(instance, method))


def gen_dict_extract(key: Any, var: dict) -> Iterator[Any]:
    """
    Traversing a dictionary to extract the values of every `key` key (at every level) and return values as a generator

    Licence: CC BY-SA 3.0.

    Thanks https://stackoverflow.com/questions/9807634/find-all-occurrences-of-a-key-in-nested-dictionaries-and-lists

    :param key: The key to search
    :param var: the dict in which to search
    :return: a generator returning all values associated to the key
    """
    if hasattr(var, 'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result


def rm_spc_acc(s: str) -> str:
    """
    remove space and accent from a string.

    :param s: the string where the space and accent will be removed
    :return: the string without space and accent
    """
    return unidecode(s.replace(' ', ''))


def cut_text_for_render(text: str, font_size: int, max_render_width: int) -> List[str]:
    """
    This function breaks a string into chunk which size depends on the rendered font size.
    Development in progress, the chunk should not break words in half.
    Not sure if this function is useful if we use UITextBox

    :param text: The text to be chunked
    :param font_size: the font size of the rendered text
    :param max_render_width: the maximum width of the rendered text
    :return: the list of chunk text
    """
    nb_char_per_line = max_render_width // font_size
    result = [text[idx: idx + nb_char_per_line] for idx in range(0, len(text), nb_char_per_line)]
    return result



class LazyXMLString:
    """
    This class allows an XML object to be lazily serialized

    Thanks, Claude.AI even if I am not sure about the license of this code
    """
    def __init__(self, element: xmlET.Element, encoding: str = 'unicode', method: str = 'xml'):
        """
        :param element: the xml element to be lazy serialized
        :param encoding: the encoding of serialization result
        :param method: the method used to serialize the element
        """
        self.element = element
        """ xml element """
        self.encoding = encoding
        """ encoding """
        self.method = method
        """ method used to serialize the element. see xml.etree.ElementTree.tostring()"""

    def __str__(self):
        return ''.join(self.lazy_tostring())

    def lazy_tostring(self) -> Iterator[str]:
        """
        serialize using iterator

        :return: an iterator of strings
        """
        # Convert the element to a string
        full_string = xmlET.tostring(self.element, encoding=self.encoding, method=self.method)

        # If the result is bytes, decode it
        if isinstance(full_string, bytes):
            full_string = full_string.decode(self.encoding)

        # Yield the string in chunks
        chunk_size = 1024
        for i in range(0, len(full_string), chunk_size):
            yield full_string[i:i+chunk_size]
