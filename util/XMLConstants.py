class XMLConstants:
    """XML-related constants for namespace URIs and other settings."""

    # Commonly used XML namespace URIs
    NULL_NS_URI = (
        ""  # Represents a null URI when namespace processing is not being performed.
    )
    DEFAULT_NS_PREFIX = ""  # Represents the default namespace prefix.
    XML_NS_URI = "http://www.w3.org/XML/1998/namespace"  # URI for the XML namespace.
    XML_NS_PREFIX = "xml"  # Prefix for the XML namespace.
    XMLNS_ATTRIBUTE_NS_URI = (
        "http://www.w3.org/2000/xmlns/"  # URI for the xmlns attribute namespace.
    )
    XMLNS_ATTRIBUTE = "xmlns"  # Represents the xmlns attribute.
    W3C_XML_SCHEMA_NS_URI = (
        "http://www.w3.org/2001/XMLSchema"  # URI for the XML Schema namespace.
    )
    W3C_XML_SCHEMA_INSTANCE_NS_URI = "http://www.w3.org/2001/XMLSchema-instance"  # URI for the XML Schema instance namespace.
    W3C_XPATH_DATATYPE_NS_URI = "http://www.w3.org/2003/11/xpath-datatypes"  # URI for the XPath datatypes namespace.
    RELAXNG_NS_URI = (
        "http://relaxng.org/ns/structure/1.0"  # URI for RELAX NG namespace.
    )

    # Feature for secure processing, often used in XML parsers to prevent XXE attacks.
    FEATURE_SECURE_PROCESSING = (
        "http://javax.xml.XMLConstants/feature/secure-processing"
    )


# Example usage
# print(XMLConstants.XML_NS_URI)  # 输出: http://www.w3.org/XML/1998/namespace
# print(XMLConstants.FEATURE_SECURE_PROCESSING)  # 输出: http://javax.xml.XMLConstants/feature/secure-processing
