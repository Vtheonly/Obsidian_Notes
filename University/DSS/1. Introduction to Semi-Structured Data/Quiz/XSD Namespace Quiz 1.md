---
sources:
  - "[[Problèmes de DTD => schéma XML]]"
  - "[[Définition: Schéma XML]]"
  - "[[Exemple Introductif]]"
  - "[[Élément Racine]]"
  - "[[Espaces de noms (namespaces) et préfixes]]"
  - "[[Schema Walkthrough]]" # Assuming the last part of the text is a walkthrough/summary
---
> [!question] DTDs use standard XML syntax for their declarations.
>> [!success]- Answer
>> False

> [!question] XML Schemas (XSD) are written using XML syntax.
>> [!success]- Answer
>> True

> [!question] DTDs provide extensive built-in data types like 'integer', 'date', and 'boolean'.
>> [!success]- Answer
>> False

> [!question] XML Schemas offer richer data typing capabilities compared to DTDs.
>> [!success]- Answer
>> True

> [!question] DTDs have built-in, native support for XML Namespaces.
>> [!success]- Answer
>> False

> [!question] XML Schema was designed to be fully namespace-aware.
>> [!success]- Answer
>> True

> [!question] One of the main reasons for developing XML Schema was to overcome the limitations of DTDs.
>> [!success]- Answer
>> True

> [!question] XSD stands for XML Schema Document.
>> [!success]- Answer
>> False

> [!question] An XML Schema defines the structure, content, and data types for a class of XML documents.
>> [!success]- Answer
>> True

> [!question] The root element of every valid XML Schema document must be `<xs:schema>` (or `<schema>` with the appropriate namespace declaration).
>> [!success]- Answer
>> True

> [!question] The XML Schema namespace URI is `http://www.w3.org/2001/XMLSchema`.
>> [!success]- Answer
>> True

> [!question] The conventional prefix used for the XML Schema namespace is typically `xml`.
>> [!success]- Answer
>> False

> [!question] An XML Schema document itself is typically an XML document.
>> [!success]- Answer
>> True

> [!question] The `targetNamespace` attribute in `<xs:schema>` specifies the namespace that the schema *itself* belongs to (i.e., the schema language namespace).
>> [!success]- Answer
>> False

> [!question] The `targetNamespace` attribute defines the namespace for the elements and attributes being *defined* by the schema.
>> [!success]- Answer
>> True

> [!question] `elementFormDefault="qualified"` means that locally defined elements in the schema must belong to the target namespace when used in an instance document.
>> [!success]- Answer
>> True

> [!question] The default value for `elementFormDefault` is `"qualified"`.
>> [!success]- Answer
>> False

> [!question] If `elementFormDefault="unqualified"`, locally defined elements in an instance document belong to "no namespace" by default.
>> [!success]- Answer
>> True

> [!question] Globally defined elements in an XSD are always considered part of the `targetNamespace` in instance documents (if a `targetNamespace` is defined).
>> [!success]- Answer
>> True

> [!question] `attributeFormDefault` controls namespace qualification for attributes, similar to how `elementFormDefault` controls it for elements.
>> [!success]- Answer
>> True

> [!question] The default value for `attributeFormDefault` is `"unqualified"`.
>> [!success]- Answer
>> True

> [!question] Using a prefix in the instance document (e.g., `<msg:message xmlns:msg="...">`) is a valid way to qualify elements belonging to a `targetNamespace`.
>> [!success]- Answer
>> True

> [!question] Declaring a default namespace in the instance document (e.g., `<message xmlns="...">`) is another valid way to qualify elements belonging to a `targetNamespace`.
>> [!success]- Answer
>> True

> [!question] If a schema specifies a `targetNamespace` and `elementFormDefault="qualified"`, an instance document with unqualified elements (no prefix, no default namespace) will validate successfully.
>> [!success]- Answer
>> False

> [!question] Namespace declarations (like `xmlns:xs`) in the schema help distinguish between schema language constructs and the vocabulary being defined.
>> [!success]- Answer
>> True

> [!question] Validation errors can occur if the namespace usage in the instance XML does not match the expectations set by the schema's `targetNamespace` and `elementFormDefault`.
>> [!success]- Answer
>> True

> [!question] The `<xs:sequence>` element indicates that child elements must appear in any order.
>> [!success]- Answer
>> False

> [!question] In the provided XSD example (`biblio.xsd`), `xs:integer` and `xs:NCName` are examples of specific data types defined by XML Schema.
>> [!success]- Answer
>> True

> [!question] The DTD example (`biblio.dtd`) defines the `reference` attribute with a specific numeric type.
>> [!success]- Answer
>> False

> [!question] XML Schemas allow for defining complex types (`xs:complexType`) which can contain sequences of elements and attributes.
>> [!success]- Answer
>> True