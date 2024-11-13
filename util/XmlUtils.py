import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from lxml import etree
from io import StringIO, BytesIO
import os
from util.XMLConstants import XMLConstants


class ApiException(Exception):
    pass


class XmlUtils:

    XMLNS_XSI = "xmlns:xsi"
    XSI_SCHEMA_LOCATION = "xsi:schemaLocation"
    LOGIC_YES = "yes"
    DEFAULT_CHARSET = "UTF-8"

    @staticmethod
    def new_document():
        try:
            return ET.ElementTree()
        except Exception as e:
            raise ApiException(e)

    @staticmethod
    def get_document(file):
        try:
            tree = ET.parse(file)
            return tree
        except ET.ParseError as e:
            raise ApiException("XML_PARSE_ERROR", e)
        except IOError as e:
            raise ApiException("XML_READ_ERROR", e)

    @staticmethod
    def get_document_from_string(xml_string):
        try:
            root = ET.fromstring(xml_string)
            return ET.ElementTree(root)
        except ET.ParseError as e:
            raise ApiException("XML_PARSE_ERROR", e)

    @staticmethod
    def create_root_element(tag_name):
        try:
            root = ET.Element(tag_name)
            return ET.ElementTree(root)
        except Exception as e:
            raise ApiException(e)

    @staticmethod
    def get_root_element_from_file(file):
        tree = XmlUtils.get_document(file)
        return tree.getroot()

    @staticmethod
    def get_root_element_from_string(xml_string):
        tree = XmlUtils.get_document_from_string(xml_string)
        return tree.getroot()

    @staticmethod
    def get_elements(parent, tag_name):
        return parent.findall(tag_name)

    @staticmethod
    def get_element(parent, tag_name):
        elements = XmlUtils.get_elements(parent, tag_name)
        return elements[0] if elements else None

    @staticmethod
    def get_child_elements(parent, tag_name=None):
        if tag_name:
            return [child for child in parent if child.tag == tag_name]
        else:
            return list(parent)

    @staticmethod
    def get_child_element(parent, tag_name):
        children = XmlUtils.get_child_elements(parent, tag_name)
        return children[0] if children else None

    @staticmethod
    def get_element_value(parent, tag_name):
        element = XmlUtils.get_element(parent, tag_name)
        return element.text if element is not None else None

    @staticmethod
    def get_child_element_value(parent, tag_name):
        element = XmlUtils.get_child_element(parent, tag_name)
        return element.text if element is not None else None

    @staticmethod
    def get_element_text(element):
        return element.text if element is not None else None

    @staticmethod
    def get_attribute_value(element, attr_name):
        return element.get(attr_name)

    @staticmethod
    def append_element(parent, tag_name, value=None):
        child = ET.SubElement(parent, tag_name)
        if value:
            child.text = value
        return child

    @staticmethod
    def append_cdata_element(parent, tag_name, value):
        child = XmlUtils.append_element(parent, tag_name)
        if value is None:
            value = ""
        child.text = f"<![CDATA[{value}]]>"
        return child

    @staticmethod
    def node_to_string(node):
        try:
            xml_string = ET.tostring(node, encoding=XmlUtils.DEFAULT_CHARSET)
            dom = parseString(xml_string)
            return dom.toprettyxml(
                indent="  ", encoding=XmlUtils.DEFAULT_CHARSET
            ).decode(XmlUtils.DEFAULT_CHARSET)
        except Exception as e:
            raise ApiException("XML_TRANSFORM_ERROR", e)

    @staticmethod
    def save_to_xml(node, file, charset=DEFAULT_CHARSET):
        try:
            tree = ET.ElementTree(node)
            tree.write(file, encoding=charset, xml_declaration=True)
        except Exception as e:
            raise ApiException("XML_WRITE_FILE_ERROR", e)

    @staticmethod
    def validate_xml(xml, xsd):
        try:
            xmlschema_doc = etree.parse(xsd)
            xmlschema = etree.XMLSchema(xmlschema_doc)
            xml_doc = etree.parse(xml)
            xmlschema.assertValid(xml_doc)
        except etree.XMLSchemaError as e:
            raise ApiException("XML_VALIDATE_ERROR", e)
        except Exception as e:
            raise ApiException("XML_READ_ERROR", e)

    @staticmethod
    def xml_to_html(xml_string, xslt_file):
        try:
            dom = etree.fromstring(xml_string)
            xslt = etree.parse(xslt_file)
            transform = etree.XSLT(xslt)
            newdom = transform(dom)
            return str(newdom)
        except Exception as e:
            raise ApiException("XML_TRANSFORM_ERROR", e)

    @staticmethod
    def set_namespace(element, namespace, schema_location):
        element.set(f"{{{XMLConstants.XMLNS_ATTRIBUTE_NS_URI}}}xmlns", namespace)
        element.set(
            f"{{{XMLConstants.XMLNS_ATTRIBUTE_NS_URI}}}{XmlUtils.XMLNS_XSI}",
            XMLConstants.W3C_XML_SCHEMA_INSTANCE_NS_URI,
        )
        element.set(
            f"{{{XMLConstants.W3C_XML_SCHEMA_INSTANCE_NS_URI}}}{XmlUtils.XSI_SCHEMA_LOCATION}",
            schema_location,
        )

    @staticmethod
    def encode_xml(payload):
        root = ET.Element(XMLConstants.XML_NS_PREFIX)
        root.text = payload
        return XmlUtils.node_to_string(root)


# Example usage:
# xml_string = '<root><child>data</child></root>'
# root = XmlUtils.get_root_element_from_string(xml_string)
# print(XmlUtils.node_to_string(root))
