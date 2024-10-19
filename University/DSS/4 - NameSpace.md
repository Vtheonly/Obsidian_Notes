**Definition:**

Namespace (NameSpace)

Namespaces were introduced in XML to mix multiple vocabularies within the same document. 

- A XML Vocabulary:
  - An XML vocabulary is a set of tag names and attributes with a specific meaning.

**Namespace XML: Problem**
Confusion about the "author" element in the XML document that reuses both XML1 and XML2.

```xml
<?xml version="1.0"?>
<cours>
  <titre>Theorie des langages</titre>
  <auteur>
    <nom>Boustil</nom>
    <prénom>Amel</prénom>
    <titre>Maitre de Conference</titre>
  </auteur>
</cours>
```

**XML Namespace: Introductory Example**

```xml
<?xml version="1.0"?>
<cours>
  <titre>Theorie des langages</titre>
  <specialité>licence informatique</specialité>
</cours>
```

**XML Namespaces**

Solution: Namespaces

- Distinguish elements and attributes from different XML applications that have the same name.
- Assign elements and attributes to a URI.
- Assign a prefix to this URI address.

```xml
<?xml version="1.0"?>
<crs:cours xmlns:crs="http://www.example.com/cours">
  <crs:titre>Theorie des langages</crs:titre>
  <personne:auteur xmlns:personne="http://www.example.com/individus">
    <personne:nom>Boustil</personne:nom>
    <personne:prenom>Amel</personne:prenom>
    <personne:titre>Maitre de conference</personne:titre>
  </personne:auteur>
</crs:cours>
```


---


**Namespace Declarations:**

Declaration

Namespaces are declared using attributes associated with an element, and two forms exist:
- `xmlns="uri"` which defines the default namespace.
- `xmlns:prefix="uri"` which defines a prefix representing a qualified namespace.

Some Remarks on Namespaces
- The scope of namespace declarations includes the tags of the containing element.
- Namespaces can be declared within the elements where they will be used or in the root element of XML.

Example:
```xml
<root xmlns:h="http://www.w3.org/TR/html4/"
      xmlns:f="http://www.example.com/personal">
  <h:table>
    <h:tr>
      <h:td>Apples</h:td>
      <h:td>Bananas</h:td>
    </h:tr>
  </h:table>
  <f:person>
    <f:name>Ali benAli</f:name>
    <f:age>80</f:age>
    <f:address>boumerdes</f:address>
  </f:person>
</root>
```


---

**Remarks on Namespaces:**

By defining a default namespace for an element, it avoids the need to use prefixes for all its children.

Example:
```xml
<person xmlns="http://www.namespacePerso">
  <name>Ali benAli</name>
  <age>80</age>
  <address>boumerdes</address>
</person>
```

We can change the default namespace even within child elements:

Example:
```xml
<person xmlns="http://www.namespacePerso">
  <address xmlns="http://www.anothernamespace.com">...</address>
</person>
```

Removing a Namespace

When there's no default namespace or prefix, no namespace is used. To remove a namespace, simply use an empty value `""`, which is equivalent to having no namespace.

Example:
```xml
<person xmlns="http://www.namespacePerso">
  <address xmlns="">boumerdes
    <country>12</country>
  </address>
</person>
```