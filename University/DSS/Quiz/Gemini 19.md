---
sources:
  - "[[XML Element Trees and Attributes]]"
---
> [!question] Match the XML tree component with its description.
>> [!example] Group A
>> a) Racine (Root)
>> b) Branches (Internal Nodes)
>> c) Feuilles (Leaf Nodes)
>
>> [!example] Group B
>> n) Elements containing other elements or text.
>> o) The single top-level node.
>> p) Elements with only text, empty elements, text nodes, comments, PIs, attribute nodes.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the relationship type with its definition in an XML tree.
>> [!example] Group A
>> a) Parent-Child Relationship
>> b) Sibling Relationship
>
>> [!example] Group B
>> n) Established by elements that are children of the same parent and appear sequentially.
>> o) Established when an element is contained directly within another element.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the attribute concept with its description.
>> [!example] Group A
>> a) Attribute Purpose
>> b) Attribute Structure
>> c) Attribute Occurrence
>
>> [!example] Group B
>> n) Always name-value pairs.
>> o) Provide additional information or metadata about an element.
>> p) Zero, one, or multiple per element; names must be unique within the tag.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the component of the example `<Etudiant mat="001">ali Benali</Etudiant>` with its role.
>> [!example] Group A
>> a) `Etudiant`
>> b) `mat`
>> c) `"001"`
>> d) `ali Benali`
>
>> [!example] Group B
>> n) Attribute Name
>> o) Element Content
>> p) Element Name
>> q) Attribute Value
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)

> [!question] Match the predefined XML attribute with its primary purpose.
>> [!example] Group A
>> a) `xml:lang`
>> b) `xml:space`
>> c) `xml:base`
>> d) `xml:id`
>
>> [!example] Group B
>> n) Signal intent regarding whitespace handling.
>> o) Define a base URI for resolving relative URIs.
>> p) Assign a unique identifier to an element.
>> q) Specify the human language of the element's content.
>
>> [!success]- Answer
>> a) -> q)
>> b) -> n)
>> c) -> o)
>> d) -> p)

> [!question] Match the `xml:lang` attribute aspect with its detail.
>> [!example] Group A
>> a) Purpose
>> b) Value Type
>> c) Inheritance
>
>> [!example] Group B
>> n) Applies to the element and descendants unless overridden.
>> o) Specifies human language of content.
>> p) Language code (e.g., from ISO 639).
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the `xml:space` attribute value with its meaning.
>> [!example] Group A
>> a) `default`
>> b) `preserve`
>
>> [!example] Group B
>> n) Application should preserve all whitespace characters.
>> o) Application can use its default whitespace handling (e.g., collapsing).
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the `xml:base` attribute aspect with its detail.
>> [!example] Group A
>> a) Purpose
>> b) Value Type
>> c) Resolution Scope
>
>> [!example] Group B
>> n) An absolute or relative URI.
>> o) Defines base URI for resolving relative URIs within the element's scope.
>> p) Element itself, or nearest ancestor with `xml:base`, or document URI.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the `xml:id` attribute aspect with its detail.
>> [!example] Group A
>> a) Purpose
>> b) Value Constraint
>> c) Uniqueness Scope
>
>> [!example] Group B
>> n) Must conform to XML Name rules.
>> o) Assign a unique identifier directly.
>> p) Within the entire document.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the predefined attribute feature with its description.
>> [!example] Group A
>> a) Namespace Prefix
>> b) Namespace URI
>> c) Declaration Requirement
>
>> [|example] Group B
>> n) `http://www.w3.org/XML/1998/namespace`
>> o) Not needed; implicitly known.
>> p) `xml:`
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the term related to XML structure with its definition.
>> [!example] Group A
>> a) Element Tree
>> b) Metadata
>> c) Well-formed Document
>
>> [!example] Group B
>> n) A document that can be represented as a tree structure.
>> o) Additional information provided by attributes.
>> p) The tree structure representation of an XML document.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the attribute syntax component with its description.
>> [!example] Group A
>> a) Location
>> b) Format
>> c) Value Delimiter
>
>> [!example] Group B
>> n) `name="value"`
>> o) Single or double quotes.
>> p) Within the element's start tag.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the node type with its potential location in an XML tree.
>> [!example] Group A
>> a) Root Element Node
>> b) Attribute Node
>> c) Text Node
>
>> [!example] Group B
>> n) Can be a leaf node or part of a branch node.
>> o) Associated with an element node, often visualized as a leaf.
>> p) The single top-level node.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the concept with its related predefined attribute.
>> [!example] Group A
>> a) Language Identification
>> b) Whitespace Handling Control
>> c) Base URI Specification
>> d) Element Identification
>
>> [!example] Group B
>> n) `xml:base`
>> o) `xml:id`
>> p) `xml:lang`
>> q) `xml:space`
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] Match the example attribute usage with the attribute being used.
>> [!example] Group A
>> a) `<p xml:lang="fr">Bonjour</p>`
>> b) `<code xml:space="preserve">...</code>`
>> c) `<section xml:id="sec1">...</section>`
>> d) `<book xml:base="http://example.com/">...</book>`
>
>> [!example] Group B
>> n) `xml:id`
>> o) `xml:base`
>> p) `xml:space`
>> q) `xml:lang`
>
>> [!success]- Answer
>> a) -> q)
>> b) -> p)
>> c) -> n)
>> d) -> o)

> [!question] Match the characteristic with the corresponding tree component.
>> [!example] Group A
>> a) Single top-level element
>> b) Contains other elements
>> c) Contains only text or is empty
>
>> [!example] Group B
>> n) Branch Node characteristic
>> o) Leaf Node characteristic
>> p) Root Node characteristic
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the term with its role in attribute definition.
>> [!example] Group A
>> a) Name
>> b) Value
>> c) Quotes
>
>> [!example] Group B
>> n) The identifier for the attribute within the tag.
>> o) Delimit the attribute value.
>> p) The specific piece of metadata assigned to the attribute name.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the standard/rule with the predefined attribute it relates to.
>> [!example] Group A
>> a) ISO 639
>> b) URI Resolution Rules
>> c) XML Name Rules
>
>> [!example] Group B
>> n) `xml:id` (value format)
>> o) `xml:lang` (value source)
>> p) `xml:base` (purpose)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the inheritance behavior with the correct predefined attribute.
>> [!example] Group A
>> a) Affects language down the tree
>> b) Affects whitespace handling down the tree
>> c) Affects relative URI resolution down the tree
>
>> [!example] Group B
>> n) `xml:space`
>> o) `xml:base`
>> p) `xml:lang`
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the description with the relevant XML concept.
>> [!example] Group A
>> a) Representation of any well-formed document
>> b) How sequential child elements relate
>> c) How nested elements relate
>
>> [!example] Group B
>> n) Parent-Child Relationship
>> o) Sibling Relationship
>> p) Element Tree
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)