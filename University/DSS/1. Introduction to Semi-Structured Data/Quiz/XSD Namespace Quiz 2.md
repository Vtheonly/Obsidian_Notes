---
sources:
  - "[[Problèmes de DTD => schéma XML]]"
  - "[[Définition: Schéma XML]]"
  - "[[Exemple Introductif]]"
  - "[[Élément Racine]]"
  - "[[Espaces de noms (namespaces) et préfixes]]"
  - "[[Schema Walkthrough]]" # Assuming the last part of the text is a walkthrough/summary
---
> [!question] Declaring a `targetNamespace` in an XSD automatically means all elements defined within it are qualified in the instance document.
>> [!success]- Answer
>> False

> [!question] The `elementFormDefault` attribute's setting directly impacts whether globally defined elements need qualification in the instance document.
>> [!success]- Answer
>> False

> [!question] If `elementFormDefault="qualified"`, even elements defined *locally* within a complex type in the schema must be namespace-qualified in the instance document.
>> [!success]- Answer
>> True

> [!question] Using `elementFormDefault="unqualified"` prevents globally defined elements from belonging to the `targetNamespace`.
>> [!success]- Answer
>> False

> [!question] The `xmlns:xs` declaration in a schema file defines the namespace for the elements *being defined* by that schema (like `<message>`).
>> [!success]- Answer
>> False

> [!question] If a schema has a `targetNamespace` and `elementFormDefault="qualified"`, an instance document *must* use either a default namespace declaration matching the `targetNamespace` or prefixes for all elements defined by the schema.
>> [!success]- Answer
>> True

> [!question] Declaring a prefix for the `targetNamespace` within the schema itself (e.g., `xmlns:monN="https://..."`) changes which namespace the defined elements belong to.
>> [!success]- Answer
>> False

> [!question] The `ref` attribute used within an `<xs:element>` declaration (e.g., `<xs:element ref="livre"/>`) means the element definition is being imported from a different schema file.
>> [!success]- Answer
>> False

> [!question] An XML document can be valid according to an XSD even if it doesn't use the exact same prefix for the target namespace as shown in schema examples (e.g., using `<msg:message>` instead of `<monN:message>` if both `msg` and `monN` map to the correct `targetNamespace`).
>> [!success]- Answer
>> True

> [!question] Setting `elementFormDefault="qualified"` affects how attributes defined in the schema must be qualified in the instance document.
>> [!success]- Answer
>> False

> [!question] `attributeFormDefault` defaults to `"qualified"`, meaning locally defined attributes must be namespace-qualified by default.
>> [!success]- Answer
>> False

> [!question] If `attributeFormDefault="unqualified"` (the default), locally defined attributes in the instance document belong to no namespace, even if the element containing them belongs to the `targetNamespace`.
>> [!success]- Answer
>> True

> [!question] An XSD file *must* start with an XML declaration (`<?xml ... ?>`) to be valid.
>> [!success]- Answer
>> False

> [!question] DTDs can simulate namespace usage by declaring attributes named `xmlns` with `#FIXED` values, providing true namespace validation.
>> [!success]- Answer
>> False

> [!question] The primary advantage of XSD using XML syntax is simply aesthetic preference.
>> [!success]- Answer
>> False

> [!question] An `<xs:complexType>` must always contain an `<xs:sequence>` element.
>> [!success]- Answer
>> False

> [!question] In the `biblio.xsd` example, `<xs:element name="titre" type="xs:string"/>` defines a local element named `titre`.
>> [!success]- Answer
>> False

> [!question] Using `<xs:element ref="titre"/>` within the definition of the `livre` element refers to the globally defined `titre` element.
>> [!success]- Answer
>> True

> [!question] The presence of `targetNamespace="URI"` in the schema mandates the use of prefixes in the instance document.
>> [!success]- Answer
>> False

> [!question] An instance document using a default namespace (`xmlns="URI"`) effectively qualifies all unprefixed elements within its scope with that URI.
>> [!success]- Answer
>> True

> [!question] If an XSD does *not* declare a `targetNamespace`, then elements defined by it belong to "no namespace".
>> [!success]- Answer
>> True

> [!question] An instance document can simultaneously use a default namespace for one vocabulary and prefixes for other vocabularies (including the XML Schema Instance namespace `xsi`).
>> [!success]- Answer
>> True

> [!question] The `xs:` prefix is mandatory; you cannot use `xsd:` or any other prefix for the XML Schema namespace `http://www.w3.org/2001/XMLSchema`.
>> [!success]- Answer
>> False

> [!question] If `elementFormDefault` is `unqualified`, validation against the schema will fail if the instance document uses prefixes for locally defined elements.
>> [!success]- Answer
>> False

> [!question] The value `CDATA` in a DTD provides the same level of data type constraint as `xs:string` in an XSD.
>> [!success]- Answer
>> False

> [!question] The choice between prefix (`<msg:to>`) and default namespace (`<to>`) qualification in the instance document primarily affects validation logic.
>> [!success]- Answer
>> False

> [!question] `xs:NCName` (used for `auteur` in `biblio.xsd`) is a data type that restricts the value to be a non-colonized name, which is stricter than `xs:string`.
>> [!success]- Answer
>> True

> [!question] Defining a `targetNamespace` is essential for achieving namespace validation using XSD.
>> [!success]- Answer
>> True

> [!question] An XSD can define elements that are allowed to contain mixed content (both text and child elements) similar to `#PCDATA` usage in DTDs. (While not explicitly shown in detail, the context implies XSDs are more powerful, making this likely true).
>> [!success]- Answer
>> True

> [!question] The `elementFormDefault` and `attributeFormDefault` settings apply schema-wide unless overridden locally (though local overriding isn't shown in the context).
>> [!success]- Answer
>> True