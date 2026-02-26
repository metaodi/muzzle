"""A tiny xmlparser"""

__version__ = "0.0.1"
__all__ = ["xmlparse", "errors"]

from typing import Optional, Union
from xml.etree.ElementTree import Element

from .errors import MuzzleError  # noqa
from .xmlparse import XMLParser  # noqa
from .xmlparse import XMLNone  # noqa


def parse(content: Union[str, bytes], namespaces: dict[str, str] = {}) -> Element:
    parser = XMLParser(namespaces=namespaces)
    return parser.parse(content)


def find(
    xml: Element, path: Union[str, list[str]], namespaces: dict[str, str] = {}
) -> Union[Element, XMLNone]:
    parser = XMLParser(namespaces=namespaces)
    return parser.find(xml, path)


def findall(xml: Element, path: str, namespaces: dict[str, str] = {}) -> list[Element]:
    parser = XMLParser(namespaces=namespaces)
    return parser.findall(xml, path)


def tostring(xml: Element) -> bytes:
    parser = XMLParser()
    return parser.tostring(xml)


def todict(xml: Union[Element, XMLNone, str, bytes], **kwargs) -> Optional[dict]:
    params = ["namespaces"]
    parser = XMLParser(namespaces=kwargs.get("namespaces", {}))
    dict_args = {k: v for k, v in kwargs.items() if k not in params}
    return parser.todict(xml, **dict_args)
