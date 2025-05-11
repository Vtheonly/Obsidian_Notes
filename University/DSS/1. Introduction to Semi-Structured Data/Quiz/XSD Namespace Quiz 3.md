---
sources:
  - "[[Conversation about XML Namespaces]]"
---
---
sources:
  - "[[XML Namespaces Clarification Chat]]"
---
> [!question] The primary purpose of an XML namespace URI is to point to a downloadable schema or definition file on the web.
>> [!success]- Answer
>> False

> [!question] XML namespaces solve name collisions by fundamentally changing the local name of the tag (e.g., changing `<titre>` to `<crs:titre>`).
>> [!success]- Answer
>> False

> [!question] The namespace URI itself contains the rules and structure definition for the elements belonging to that namespace.
>> [!success]- Answer
>> False

> [!question] The namespace prefix (like `crs:` in `crs:titre`) is the actual unique identifier that distinguishes the element.
>> [!success]- Answer
>> False

> [!question] XML processors typically try to fetch or resolve the resource located at the namespace URI when parsing the document.
>> [!success]- Answer
>> False

> [!question] A key characteristic of a namespace URI is that it must be globally unique to effectively prevent collisions.
>> [!success]- Answer
>> True

> [!question] The concept of XML namespaces is analogous to variable or function scoping in programming languages.
>> [!success]- Answer
>> True

> [!question] An XML document can only use namespace URIs that correspond to an existing XSD or DTD file.
>> [!success]- Answer
>> False

> [!question] XML namespaces, by themselves, define the allowed attributes, child elements, and data types for an element.
>> [!success]- Answer
>> False

> [!question] An XSD file uses the `targetNamespace` attribute to declare which specific namespace it is providing definitions for.
>> [!success]- Answer
>> True

> [!question] In an XML document, `xmlns` attributes are used to associate prefixes (or the default namespace) with specific namespace URIs.
>> [!success]- Answer
>> True

> [!question] XML validation tools determine if an element is valid based solely on its local name (e.g., `titre`).
>> [!success]- Answer
>> False

> [!question] Using a namespace prefix (like `pers:titre`) makes the element logically distinct from an unprefixed element (`titre`) if the prefix maps to a namespace URI and the unprefixed element is in no namespace or a different default namespace.
>> [!success]- Answer
>> True

> [!question] If two elements have the same local name (`titre`) but are associated with different namespace URIs via prefixes, the XML processor treats them as completely different kinds of elements.
>> [!success]- Answer
>> True

> [!question] Any URI used in an `xmlns` declaration must be an active, resolvable HTTP URL.
>> [!success]- Answer
>> False

> [!question] The declaration `xmlns:crs="http://www.example.com/courses"` primarily serves as a command for the parser to download definitions from that URL.
>> [!success]- Answer
>> False

> [!question] An XML document can be "well-formed" even if it declares and uses a namespace URI for which no corresponding schema (XSD/DTD) exists.
>> [!success]- Answer
>> True

> [!question] An XML document can be successfully "validated" against a schema only if the namespaces used in the document have corresponding schema definitions available.
>> [!success]- Answer
>> True

> [!question] The XML Schema Definition (XSD) associated with a namespace URI is responsible for defining the element's meaning, structure, and validation constraints.
>> [!success]- Answer
>> True

> [!question] The collision between `<crs:titre>` and `<pers:titre>` is resolved primarily because the prefixes `crs` and `pers` are different strings.
>> [!success]- Answer
>> False

> [!question] A namespace URI's main function is to act as a unique identifier, not necessarily as a locator for resources.
>> [!success]- Answer
>> True

> [!question] Mixing XML elements from different vocabularies (like HTML and MathML) in one document without using namespaces is likely to cause name conflicts.
>> [!success]- Answer
>> True

> [!question] In an XSD schema, the `targetNamespace` attribute specifies the namespace that the schema itself *belongs* to, rather than the namespace it *defines*.
>> [!success]- Answer
>> False

> [!question] To create a well-formed XML document, any namespace URI used must first be officially registered with a central authority.
>> [!success]- Answer
>> False

> [!question] Checking if an element has the correct attributes or child elements (semantic validation) requires a schema (like XSD) associated with the element's namespace URI.
>> [!success]- Answer
>> True

> [!question] The "fully qualified name" of an XML element used by processors to uniquely identify it consists of its local name combined with its namespace URI.
>> [!success]- Answer
>> True

> [!question] The declaration `xmlns:prefix="URI"` creates a mandatory, document-wide alias; the prefix cannot be redefined later in the document.
>> [!success]- Answer
>> False

> [!question] An element like `<titre>` automatically belongs to the namespace defined by an `xmlns="some-URI"` attribute on one of its ancestor elements, unless explicitly prefixed.
>> [!success]- Answer
>> True

> [!question] If no namespace (default or prefixed) is declared or in scope for an element like `<titre>`, it is considered to be part of a special, implicit "null" namespace.
>> [!success]- Answer
>> False (It's in "no namespace")

> [!question] Changing only the namespace prefix (e.g., from `crs:` to `c:`) but keeping the associated URI (`http://www.example.com/courses`) the same changes the fundamental identity of the element `<c:titre>` compared to `<crs:titre>`.
>> [!success]- Answer
>> False