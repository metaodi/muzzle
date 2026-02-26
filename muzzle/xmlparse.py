import re
from typing import Optional, Union
from xml.etree.ElementTree import Element
import defusedxml.ElementTree as etree
import xmltodict
from . import errors


class XMLNone(object):
    def __nonzero__(self) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def iter(self) -> list:
        return []

    text: Optional[str] = None


class XMLParser(object):
    def __init__(self, namespaces: dict[str, str] = {}) -> None:
        self.namespaces = namespaces

    def parse(self, content: Union[str, bytes]) -> Element:
        try:
            return etree.fromstring(content)
        except Exception as e:
            raise errors.XMLParserError("Error while parsing XML: %s" % e)

    def find(
        self, xml: Element, path: Union[str, list[str]]
    ) -> Union[Element, XMLNone]:
        if isinstance(path, list):
            for p in path:
                elem = self.find(xml, p)
                if not isinstance(elem, XMLNone):
                    return elem
            return XMLNone()
        elem = xml.find(path, self.namespaces)
        if elem is None:
            return XMLNone()
        return elem

    def findall(self, xml: Element, path: str) -> list[Element]:
        return xml.findall(path, self.namespaces)

    def tostring(self, xml: Element) -> bytes:
        return etree.tostring(xml)

    def todict(
        self, xml: Union[Element, XMLNone, str, bytes], **kwargs
    ) -> Optional[dict]:
        if isinstance(xml, XMLNone):
            return None
        if isinstance(xml, Element):
            xml = self.tostring(xml)

        # reverse key/values for xmltodict
        dict_namespaces = {v: k for k, v in self.namespaces.items()}
        dict_args = {
            "dict_constructor": dict,
            "process_namespaces": True,
            "namespaces": dict_namespaces,
            "attr_prefix": "",
            "cdata_key": "text",
        }
        dict_args.update(kwargs)
        return dict(xmltodict.parse(xml, **dict_args))

    def namespace(self, element: Element) -> str:
        m = re.match(r"\{(.*)\}", element.tag)
        return m.group(1) if m else ""
