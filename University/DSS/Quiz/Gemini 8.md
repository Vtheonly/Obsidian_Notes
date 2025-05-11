---
sources:
  - "[[XML Exams - UMBB]]"
---
> [!question] An XML document must always have a DTD to be considered well-formed.
>> [!success]- Answer
>> False

> [!question] Which attribute in the `<album>` element (from the CD exam) is defined with an IDREF type in the DTD to link to an artiste?
> a) annee
> b) type
> c) ref
> d) titre
>> [!success]- Answer
>> c) ref

> [!question] According to the provided DTD example for CDs, which of the following child elements are required within an `<artiste>` element? (Select all that apply)
> a) nom
> b) ville
> c) prenom
> d) chansons
> e) ref-artiste
> f) titre
>> [!success]- Answer
>> a) nom
>> b) ville

> [!question] Match the XML technology (Group A) with its primary purpose (Group B).
>> [!example] Group A
>> a) DTD
>> b) XPath
>> c) XSLT
>> d) XML Schema
>
>> [!example] Group B
>> n) Defining the structure and data types of an XML document using XML syntax.
>> o) Transforming XML documents into other formats (e.g., HTML, other XML).
>> p) Defining the structure of an XML document using a non-XML syntax.
>> q) Navigating and querying elements and attributes within an XML document.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> o)
>> d) -> n)

> [!question] The `EMPTY` keyword in a DTD ELEMENT declaration means the element cannot contain any text content, but it can contain attributes.
>> [!success]- Answer
>> True

> [!question] In XML Schema, what construct allows elements to appear in any order?
> a) xs:sequence
> b) xs:choice
> c) xs:all
> d) xs:group
>> [!success]- Answer
>> c) xs:all

> [!question] Which of the following XPath expressions correctly selects the names (`nom`) of all artistes located in 'Constantine' according to the CD exam structure? (Select all valid options)
> a) /CD/artiste[ville='Constantine']/nom
> b) //artiste[ville='Constantine']/nom
> c) //nom[../ville='Constantine']
> d) /CD/artiste[@ville='Constantine']/nom
> e) //artiste/ville[.='Constantine']/../nom
> f) //artiste[contains(ville,'Constantine')]/nom
>> [!success]- Answer
>> a) /CD/artiste[ville='Constantine']/nom
>> b) //artiste[ville='Constantine']/nom
>> c) //nom[../ville='Constantine']
>> e) //artiste/ville[.='Constantine']/../nom

> [!question] Match the XPath concept (Group A) with its description (Group B).
>> [!example] Group A
>> a) `count()`
>> b) `starts-with()`
>> c) `//`
>> d) `@`
>
>> [!example] Group B
>> n) Selects nodes anywhere in the document matching the criteria, regardless of absolute path.
>> o) Checks if a string value begins with a specific substring.
>> p) Prefixes an attribute name.
>> q) Returns the number of nodes in a node-set.
>
>> [!success]- Answer
>> a) -> q)
>> b) -> o)
>> c) -> n)
>> d) -> p)