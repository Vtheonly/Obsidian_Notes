---
sources:
  - "[[XML Schema (Schéma XML)]]"
---
> [!question] What is the primary reason XML Schema (XSD) was developed to replace DTDs?
> a) DTDs have a complex syntax that is difficult to learn.
> b) DTDs offer extensive data typing capabilities, making them too complex.
> c) DTDs lack support for XML namespaces and have limited data typing.
> d) DTDs are written in XML, requiring different parsers than XML documents.
>> [!success]- Answer
>> c) DTDs lack support for XML namespaces and have limited data typing.

> [!question] Which of the following is NOT a limitation of DTDs compared to XSD?
> a) Limited data typing capabilities
> b) Lack of inherent XML namespace support
> c) Use of non-XML syntax
> d) Inability to define document models
>> [!success]- Answer
>> d) Inability to define document models

> [!question] In the provided `biblio.xsd` example, what data type is used for the 'reference' attribute of the 'livre' element?
> a) xs:string
> b) xs:integer
> c) CDATA
> d) xs:NCName
>> [!success]- Answer
>> b) xs:integer

> [!question] What is the purpose of the 'targetNamespace' attribute in an XML Schema?
> a) It specifies the URI of the XML Schema Instance namespace.
> b) It declares the default namespace for the XML Schema document itself.
> c) It defines the namespace to which elements and attributes defined in the schema belong.
> d) It indicates the location of the schema file for validation.
>> [!success]- Answer
>> c) It defines the namespace to which elements and attributes defined in the schema belong.

> [!question] What is the function of the 'xsi:schemaLocation' attribute?
> a) It specifies the location of an XML Schema to validate an instance document when the instance document's elements are not in any target namespace.
> b) It associates a target namespace with the corresponding XML Schema file for validation.
> c) It declares the XML Schema Instance namespace in the instance document.
> d) It defines the root element of the XML Schema document.
>> [!success]- Answer
>> b) It associates a target namespace with the corresponding XML Schema file for validation.

> [!question] What is the difference between 'xs:extension' and 'xs:restriction' when deriving simple types in XSD?
> a) `xs:extension` adds new elements to the base type, while `xs:restriction` constrains the values of existing elements.
> b) `xs:extension` constrains the value space of the base type, while `xs:restriction` adds new elements to it.
> c) `xs:extension` adds attributes to the base simple type, while `xs:restriction` constrains the base type's value space and can modify attributes.
> d) `xs:extension` derives complex types, while `xs:restriction` derives simple types.
>> [!success]- Answer
>> c) `xs:extension` adds attributes to the base simple type, while `xs:restriction` constrains the base type's value space and can modify attributes.

> [!question] Which compositor allows child elements to appear zero or one time in any order within a complex type?
> a) xs:sequence
> b) xs:choice
> c) xs:all
> d) xs:any
>> [!success]- Answer
>> c) xs:all

