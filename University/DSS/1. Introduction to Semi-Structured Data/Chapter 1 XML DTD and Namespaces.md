### Le Web : HTML

#tags: #web #HTML #markup_language #hypertext #URI #browser

*   **HTML (HyperText Markup Language):** The standard markup language for creating web pages. It uses tags (`<tag>`) to structure content and suggest how it should be displayed by a web browser.
*   **Navigateur Web (Web Browser):** The software application used by users to access and view web pages (e.g., Chrome, Firefox, Safari).
*   **URI (Uniform Resource Identifier):** A string of characters used to identify a resource (e.g., a document, image, service) on the internet or a network. URLs (Uniform Resource Locators) are a common type of URI.
*   **HyperTexte (HyperText):** Text which contains links (hyperlinks) to other texts or resources. It allows structuring information by enabling documents to reference other documents or specific parts of documents, creating a non-linear way of accessing information.
*   **Stockage Web (Web Storage):** Information on the Web can be stored in various ways:
    *   Static files (e.g., `.html`, `.css`, `.js`, images).
    *   Databases (increasingly common for dynamic content).
    *   XML documents (for data representation and exchange).

### XML : Extensible Markup Language

#tags: #XML #markup_language #SGML #HTML #data_structure #presentation #metalanguage

*   **XML (Extensible Markup Language):** Like HTML, XML is a markup language using tags. However, its primary focus is on **describing the structure and meaning of data**, not its presentation.
*   **Key Distinction from HTML:** XML separates the **structure/content** of a document from its **presentation/display**. HTML mixes structure and presentation hints.
*   **Origin:** XML is a simplified subset derived from **SGML (Standard Generalized Markup Language)**, incorporating simplicity lessons from HTML. It retains SGML's power for defining custom markup languages while being much easier to parse and use.
*   **Advantages:** XML aims to combine the flexibility of SGML with the simplicity of HTML.

**Comparison Table:**

| Feature             | Comparaison avec SGML                  | Comparaison avec HTML                   |
| :------------------ | :------------------------------------- | :-------------------------------------- |
| **Nature**          | Métalangage, orienté structure       | Simple                                  |
| **Complexity**      | Moins complexe que SGML               | Plus strict que HTML                     |
| **Focus**           | Structure                             | Presentation (historically)             |
| **Error Tolerance** | Non tolérant aux erreurs (strict)     | Tolérant aux erreurs (historically)     |

### Données Structurées vs Semi Structurées (Structured vs. Semi-Structured Data)

#tags: #structured_data #semistructured_data #XML #database #flexibility #information_exchange

*   **Structured Data:** Data that conforms to a predefined, rigid model (e.g., tables in a relational database). Relations in a BDD contain structured data.
*   **Semi-Structured Data:** Data that has some organizational properties (e.g., tags, nesting) but doesn't fit a fixed, rigid schema like relational data. XML documents contain semi-structured data.
    *   **Flexibility:** XML documents can adhere to a general hierarchical structure but allow for variations in details (e.g., optional elements, repeated elements).
    *   **Schema:** XML *can* use a schema (like DTD or XSD) to define structure, but it remains a text file, not inherently optimized for storage space or complex database manipulations like native BDDs.
    *   **Information Circulation:** XML is often viewed as a crucial format for data exchange and information flow between different systems, acting as a common, understandable language.
    *   **XML Databases:** Specialized databases exist (Native XML Databases or XML-enabled databases) with powerful query languages (like XQuery, XPath) for efficient storage and retrieval of XML data.

### Utilisation de XML (Uses of XML)

#tags: #XML_usage #data_storage #data_processing #data_exchange #configuration #web_services #document_format

XML usage has expanded significantly. Key applications include:

1.  **Data Storage & Processing:** Providing a framework for storing and processing semi-structured data. Often used for configuration files, intermediate data representation.
2.  **Data Exchange:** Facilitating the exchange of information between different applications, platforms, or organizations due to its vendor-neutral, text-based format. Common in Web Services (SOAP), APIs, and data feeds.
3.  **Document Formats:** Defining specialized document types (see XML Dialects).

### XML: premier exemple (First Example)

#tags: #XML_example #XML_syntax #XML_declaration #processing_instruction #XML_comment #root_element #XML_element #XML_attribute

```xml
<?xml version="1.0" encoding="UTF-8"?>  <!-- XML Declaration -->
<?xml-stylesheet href="des.css" type="text/css"?> <!-- Processing Instruction (links CSS) -->

<charge> <!-- Root Element -->
  <cours> <!-- Element -->
    <designation>Web sémantique</designation> <!-- Element with text content -->
    <auteur>Boustil Amel</auteur>
    <Specialite>Systèmes d'information</Specialite>
  </cours>
  <cours>
    <designation>Theorie des langages</designation>
    <auteur>Boustil Amel</auteur>
    <Specialite>Licence Informatique</Specialite>
  </cours>
  <cours>
    <designation>Données sémie structurées</designation>
    <auteur>Boustil Amel</auteur>
    <Specialite>ISIL</Specialite> <!-- Highlighted in slide -->
  </cours>
  
  <!--ceci est un commentaire--> <!-- XML Comment -->
  
</charge>
```

*   This example shows a root element `<charge>` containing multiple `<cours>` elements.
*   Each `<cours>` has child elements describing the course (`<designation>`, `<auteur>`, `<Specialite>`).
*   It includes an XML declaration, a processing instruction for styling, and a comment.

### Galaxie XML (XML Ecosystem / Stack)

#tags: #XML_stack #XML_Schema #XPath #XSL #XSLT #XQuery #XLink #XPointer #DOM #SAX #API

XML is more than just the markup language; it's surrounded by a set of related standards and technologies:

*   **XML Schema (XSD):** A language for defining the structure, content, and data types of XML documents (an alternative/successor to DTDs). Provides more powerful validation capabilities.
*   **XPath:** A language for navigating through elements and attributes in an XML document (like file paths for XML). Used by XSLT and XQuery.
*   **XSL (Extensible Stylesheet Language):** A family of languages for transforming and presenting XML documents.
    *   **XSLT (XSL Transformations):** Used to transform XML documents into other formats (XML, HTML, text).
    *   **XSL-FO (XSL Formatting Objects):** Used to specify formatting for print or PDF output (less common now).
*   **XQuery:** A language designed for querying collections of XML data (like SQL for XML).
*   **XLink & XPointer:** Standards for creating more complex and specific links within and between XML documents (more powerful than HTML's `<a>` tag).
*   **DOM (Document Object Model):** A programming interface (API) that represents an XML document as a tree structure in memory, allowing navigation and manipulation by code. Tree-based, loads entire document.
*   **SAX (Simple API for XML):** An event-based programming interface (API) for processing XML documents sequentially. More memory-efficient for large documents as it doesn't load everything at once.

### XML Dialectes (XML Dialects)

#tags: #XML_dialect #metalanguage #vocabulary #XHTML #SVG #XSLT #SMIL #MathML #RSS #WSDL #XUL #XML_Signature #SAML

*   **XML as a Metalanguage:** XML itself doesn't define specific tags (beyond `xml:` namespace). It's a *metalanguage* used to create other specialized markup languages, called XML dialects or vocabularies.
*   **Purpose:** These dialects apply the syntax rules of XML to specific domains, defining a set of tags and attributes meaningful within that domain.
*   **Benefits:**
    *   Leverage the strict syntax and parsing rules of XML.
    *   Use standard XML tools (parsers, editors, validators, transformers) to work with documents in these dialects.

**Common XML Dialects:**

*   **RSS (Really Simple Syndication):** For syndicating web content updates (news feeds, blog posts).
*   **SVG (Scalable Vector Graphics):** For describing two-dimensional vector graphics.
*   **SMIL (Synchronized Multimedia Integration Language):** For describing multimedia presentations (timing, layout).
*   **MathML (Mathematical Markup Language):** For describing mathematical notation.
*   **WSDL (Web Services Description Language):** For describing the interface of web services.
*   **XUL (XML User Interface Language):** For defining user interfaces (used notably by Mozilla).
*   **XML Signature:** For creating digital signatures within XML documents.
*   **SAML (Security Assertion Markup Language):** For exchanging authentication and authorization data (e.g., for Single Sign-On).
*   **XHTML (Extensible HyperText Markup Language):** HTML reformulated as a strict XML application.

### XML Dialectes : Exemple (MathML)

#tags: #MathML #MathML_example #W3C #XML_dialect_example

*   **MathML:** A W3C recommendation (see `http://www.w3.org/Math/`) for encoding mathematical expressions in XML.
*   **Key MathML Elements (Presentation Markup):**
    *   `<mi>`: Identifier (variable, function name, e.g., x)
    *   `<mn>`: Number (e.g., 2, 4)
    *   `<mo>`: Operator (e.g., +, *, =)
    *   `<mrow>`: Groups sub-expressions horizontally (forms a row).
    *   `<msup>`: Superscript (base followed by exponent).
    *   `<mfrac>`: Fraction (numerator followed by denominator).
    *   *(Many others exist)*

**Example Code (representing x² + 4*x + 4):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<math xmlns="http://www.w3.org/1998/Math/MathML"> <!-- Note the namespace -->
  <mrow> <!-- Row for the whole expression -->
    <msup> <!-- x squared -->
      <mi>x</mi> 
      <mn>2</mn> 
    </msup>
    <mo>+</mo> <!-- Plus operator -->
    <mrow> <!-- Row for 4*x -->
      <mn>4</mn> 
      <mo>*</mo> <!-- Times operator -->
      <mi>x</mi> 
    </mrow>
    <mo>+</mo> <!-- Plus operator -->
    <mn>4</mn> 
  </mrow>
</math>

<!-- Ici nous avons décrit l'expression : x² + 4 * x + 4. -->
```

### Introduction - Récapitulatif (Summary)

#tags: #XML_summary #W3C #metalanguage #data_exchange #markup_language

*   **XML (eXtended Markup Language):** A W3C-recommended **metalanguage** using **markup (tags)**, designed primarily to facilitate **data exchange**, especially over the Web (since 1998).
*   **Content, Not Presentation:** XML describes the **structure and meaning** of data, separating it from how it should be displayed.
*   **Text-Based & Structured:** It's a human-readable, text-based format using **tags** to organize data hierarchically.
*   **Key Uses:** Data **storage**, document **sharing**, and data **exchange** between diverse applications.
*   **Characteristics:** **Simple** syntax rules, **flexible** in defining structures, relatively **easy to use**, an **open standard**, and **normalized**.
*   **Automation & Tools:** Well-suited for **automatic processing** by software. A wide range of generic **parsing** and **transformation** tools are available.

---

## Structure XML

### XML c'est donc... (What XML is...)

#tags: #XML_structure #XML_tag #XML_element #XML_attribute #XML_tree #root_element

*   **Balise (Tag/Label):** Markers indicating the start and end of an element. They delimit textual data or other elements.
    *   **Syntax:** Start tag: `<elementName>`, End tag: `</elementName>`. Empty element tag: `<elementName/>`.
*   **Élément (Element):** The fundamental building block, consisting of a start tag, content (text, other elements, or mixed), and an end tag, or just an empty-element tag. Elements represent a piece of data and its context. Tags give *meaning* to the enclosed data section.
*   **Racine (Root Element):** Every well-formed XML document must have exactly one top-level element that contains all other elements.
*   **Imbrication (Nesting):** Elements can be nested inside other elements, forming a hierarchical **Arbre (Tree)** structure.
*   **Attribut (Attribute):** A name-value pair specified *inside the start tag* of an element, providing additional information or metadata about the element.
    *   **Syntax:** `attributeName="value"` (value must be enclosed in single or double quotes).

### Structure d'un document XML (XML Document Structure)

#tags: #XML_document_structure #XML_prologue #XML_declaration #processing_instruction #DTD #XML_comment #root_element #XML_tree

An XML document generally consists of:

1.  **Prologue (Optional):** Contains instructions for XML parsers and applications. It can include:
    *   **XML Declaration:** `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` Specifies XML version, character encoding, and external dependency information. (Technically optional but strongly recommended).
    *   **Instructions de Traitement (Processing Instructions / PIs):** `<?target data?>` Pass information to specific applications (e.g., `<?xml-stylesheet ... ?>` to link a stylesheet).
    *   **Déclaration de Type de Document (Document Type Declaration / DOCTYPE):** `<!DOCTYPE ...>` Links to or contains a DTD for validation.
    *   **Commentaires (Comments):** `<!-- comment text -->` Ignored by parsers but useful for humans.
2.  **Élément Racine (Root Element):** The single element that encloses all other content elements in the document.
3.  **Arbre d'Éléments et Attributs (Tree of Elements and Attributes):** The main content, structured hierarchically with elements, attributes, and text.
4.  **Commentaires (Comments):** Can appear within the element tree as well.

**XML Exemple Détaillé:**

*(See Slide 34 for the visual breakdown matching the XML example from Slide 14 with labels: Déclaration, Type document, Racine, Élément, Attribut, Balise fermante, Commentaire)*

### Le Prologue : XML Declaration

#tags: #XML_prologue #XML_declaration #XML_version #XML_encoding #XML_standalone #UTF-8 #ISO-8859-1

The XML Declaration `<?xml ... ?>` provides meta-information about the document itself.

*   **`version`:** Specifies the XML version being used. Typically `"1.0"`. (`"1.1"` exists but is less common).
*   **`encoding`:** Specifies the character encoding used for the document's content (e.g., `"UTF-8"`, `"ISO-8859-1"`).
    *   Default (if omitted and no other external hints): UTF-8.
    *   Crucial for correct interpretation of characters.
*   **`standalone`:** Indicates whether the document relies on external markup declarations (like an external DTD).
    *   `"yes"`: The document is self-contained; no external declarations are needed to parse it correctly (though an external DTD might still exist for validation).
    *   `"no"` (Default): The document may depend on external declarations defined, for example, in an external DTD. The parser might need to fetch these for correct interpretation (e.g., default attribute values, entity definitions).

### Le Prologue : Les instructions de traitement (Processing Instructions)

#tags: #processing_instruction #XML_stylesheet #XSLT #CSS

*   **Purpose:** Processing Instructions (PIs) are used to pass information from the XML document to an application that will process it. They are application-specific.
*   **Syntax:** `<?target instruction_data?>`
    *   `target`: Identifies the application the instruction is intended for.
    *   `instruction_data`: The information being passed.
*   **Common Example:** `xml-stylesheet` PI is used to link an external stylesheet (CSS or XSLT) to the XML document.
    ```xml
    <?xml-stylesheet href="list.xsl" type="text/xsl" title="En liste"?>
    <?xml-stylesheet href="style.css" type="text/css"?>
    ```
    *   `href`: URI of the stylesheet file.
    *   `type`: MIME type of the stylesheet (`text/xsl`, `text/css`).
    *   `title`, `media`, `charset`, `alternate`: Other optional pseudo-attributes.

### Arbre d'éléments (Element Tree)

#tags: #XML_tree #XML_element #parent_child_relationship #sibling_relationship #root_node #branch_node #leaf_node

*   **Representation:** Every well-formed XML document can be represented as a tree structure.
*   **Tree Components:**
    *   **Racine (Root):** The single top-level node corresponding to the root element.
    *   **Branches (Internal Nodes):** Elements that contain other elements or text.
    *   **Feuilles (Leaf Nodes):** Elements containing only text, empty elements, text nodes, comments, PIs, attribute nodes.
*   **Structure:**
    *   **Nesting (Parent-Child):** An element contained directly within another element establishes a parent-child relationship in the tree.
    *   **Adjacency (Siblings):** Elements that are children of the same parent and appear sequentially are siblings.
*   *(See Slide 40 for a visual example mapping the XML from Slide 14 to a tree diagram, showing elements, attributes (Id=ws), and text content as nodes).*

### Les Attributs (Attributes)

#tags: #XML_attribute #attribute_syntax #metadata

*   **Purpose:** Attributes provide additional information or metadata about an element. They are part of the element itself, specified within its start tag.
*   **Occurrence:** Elements can have zero, one, or multiple attributes. Each attribute name must be unique within a single element tag.
*   **Structure:** Attributes are always name-value pairs.
*   **Syntax:**
    *   Within the start tag: `<ElementName attr1="value1" attr2="value2">`
    *   Attribute format: `name="value"` (Value must be enclosed in single or double quotes).
*   **Example:**
    ```xml
    <Etudiant mat="001">ali Benali</Etudiant> 
    ```
    *   Element: `Etudiant`
    *   Attribute Name: `mat`
    *   Attribute Value: `"001"`
    *   Element Content: `ali Benali`

### Les attributs prédéfinis (Predefined Attributes)

#tags: #XML_attribute #predefined_attributes #xml_namespace #xml_lang #xml_space #xml_base #xml_id #whitespace_handling #URI #base_URI #relative_URI #ISO639

XML defines a few special attributes that reside in the `xml:` namespace (`http://www.w3.org/XML/1998/namespace`). This namespace URI and the `xml:` prefix are implicitly known and do not need to be declared.

1.  **`xml:lang`:**
    *   **Purpose:** Specifies the human language of the element's content.
    *   **Value:** A language code, typically from ISO 639 (e.g., `"en"`, `"fr"`, `"es"`).
    *   **Example:** `<p xml:lang="fr">Bonjour</p>`
    *   **Inheritance:** Applies to the element it's on and all descendants unless overridden by another `xml:lang` attribute.

2.  **`xml:space`:**
    *   **Purpose:** Signals intent regarding whitespace handling within the element's content to the processing application.
    *   **Values:**
        *   `"default"`: The application can use its default whitespace handling (often involves collapsing multiple spaces, removing leading/trailing spaces).
        *   `"preserve"`: The application should preserve all whitespace characters as they appear in the document.
    *   **Example:** `<code xml:space="preserve"> function() { return true; } </code>`
    *   **Inheritance:** Applies to the element and descendants unless overridden.

3.  **`xml:base`:**
    *   **Purpose:** Defines a base URI for resolving relative URIs that appear within the scope of the element (e.g., in `href` attributes, `SYSTEM` identifiers).
    *   **Value:** An absolute or relative URI.
    *   **Resolution:** Relative URIs are resolved against the `xml:base` of the element they are in, or if absent, against the `xml:base` of the nearest ancestor, ultimately falling back to the document's URI.
    *   **Example:**
        ```xml
        <?xml version="1.0" encoding="iso-8859-1" standalone="yes"?>
        <book xml:base="http://www.somewhere.org/Teaching/index.html"> 
          <!-- Base is http://www.somewhere.org/Teaching/index.html -->
          <chapter xml:base="XML/chapter.html"> 
            <!-- Base is now http://www.somewhere.org/Teaching/XML/chapter.html -->
            <section xml:base="XPath/section.html"/> 
            <!-- Base is now http://www.somewhere.org/Teaching/XML/XPath/section.html -->
          </chapter>
          <section xml:base="/Course/section.html"/> 
            <!-- Base is http://www.somewhere.org/Course/section.html ('/' resolves from host) --> 
        </book>
        ```

4.  **`xml:id`:**
    *   **Purpose:** Allows assigning a unique identifier (ID) to an element directly within the XML, without necessarily relying on a DTD or Schema to declare it *as* type ID (though schema validation would enforce uniqueness and naming rules if present).
    *   **Value:** Must conform to XML Name rules. Should be unique within the document.
    *   **Example:** `<section xml:id="sec1">...</section>`

### Document bien formé et document valide (Well-formed vs. Valid)

#tags: #well_formed_XML #valid_XML #XML_syntax #DTD #XML_Schema #validation #grammar

*   **Document Bien Formé (Well-formed Document):**
    *   **Definition:** An XML document that adheres to all the fundamental XML syntax rules.
    *   **Rules include:** Proper tag nesting, all tags closed, attribute values quoted, exactly one root element, special characters handled correctly (`&lt;`, `&amp;`, etc.), proper declaration/PI/comment syntax.
    *   **Analogy:** Correct spelling and basic sentence structure in natural language. This is the *minimum requirement* for any XML document to be parsed.

*   **Document Valide (Valid Document):**
    *   **Definition:** A well-formed XML document that *also* conforms to a specific set of structural and content rules defined in a schema (like a DTD or an XML Schema Definition - XSD).
    *   **Purpose:** Ensures the document follows a predefined "grammar" or template for a particular application or data exchange context.
    *   **Analogy:** A document that not only has correct grammar but also follows the specific structure required for a business report or a scientific paper.

---

## DTD (Document Type Definition)

#tags: #DTD #DocumentTypeDefinition #XML_validation #internal_DTD #external_DTD #DOCTYPE #ELEMENT #ATTLIST #grammar

*   **Purpose:** A DTD defines the legal building blocks of an XML document. It specifies the structure, element types, attributes, and other constraints, essentially defining a "grammar" for a class of XML documents.
*   **Validation:** A validating XML parser can use a DTD to check if an XML document is **valid** according to the defined grammar.
*   **Location:** A DTD can be:
    *   **Interne (Internal):** Declared directly within the XML document inside the `<!DOCTYPE ... [...]>` declaration. Suitable for smaller, self-contained definitions.
        *   Syntax: `<!DOCTYPE RootElementName [ ... DTD declarations ... ]>`
    *   **Externe (External):** Defined in a separate `.dtd` file and referenced from the XML document. Better for reusable or complex definitions.
        *   Syntax (System): `<!DOCTYPE RootElementName SYSTEM "path/to/your.dtd">` (References a DTD file via a URI, often a local path).
        *   Syntax (Public): `<!DOCTYPE RootElementName PUBLIC "publicIdentifier" "uri/to/your.dtd">` (Uses a formal public identifier, often with a fallback URI).

*   **Key DTD Declarations:**
    *   `<!ELEMENT ...>`: Defines an element type and its allowed content.
    *   `<!ATTLIST ...>`: Defines the attributes allowed for an element type.
    *   `<!ENTITY ...>`: Defines reusable chunks of text or external resources.
    *   `<!NOTATION ...>`: Declares formats for non-XML data.

### DTD : Déclaration des éléments (`<!ELEMENT ...>`)

#tags: #DTD #ELEMENT #PCDATA #EMPTY #ANY #DTD_content_model #DTD_sequence #DTD_choice #DTD_occurrence_indicators #mixed_content

*   **Syntax:** `<!ELEMENT ElementName ContentModel>`
*   **`ElementName`:** The name of the element type being defined.
*   **`ContentModel`:** Specifies what content the element is allowed to contain.

**Content Model Types:**

1.  **`EMPTY`:** The element must have no content (no text, no child elements). Often used for elements carrying information solely through attributes.
    *   Example: `<!ELEMENT img EMPTY>` (XML: `<img src="logo.png"/>`)
2.  **`ANY`:** The element can contain any sequence of parsed character data (#PCDATA) and/or any declared child elements. (Discouraged as it weakens validation).
    *   Example: `<!ELEMENT notes ANY>`
3.  **`(#PCDATA)`:** Parsed Character Data. The element can only contain text; no child elements allowed.
    *   Example: `<!ELEMENT name (#PCDATA)>` (XML: `<name>John Doe</name>`) 
4.  **Element Content (Children):** Specifies allowed child elements using parentheses `()` and connectors:
    *   **Sequence (`,`)**: Elements must appear in the specified order.
        *   Example: `<!ELEMENT book (title, author, chapter+)>` (A title, then an author, then one or more chapters).
    *   **Choice (`|`)**: Exactly one of the listed elements must appear.
        *   Example: `<!ELEMENT shape (circle | square | polygon)>` (Must contain a circle OR a square OR a polygon).
    *   **Grouping `()`**: Parentheses group sequences or choices, allowing nesting and application of occurrence indicators to the group.
        *   Example: `<!ELEMENT item (description, (price | cost), quantity?)>`
5.  **Mixed Content (`(#PCDATA | Element1 | Element2)*`)**: Allows text interspersed with optional, repeatable child elements in any order. Must use the `*` indicator.
    *   Example: `<!ELEMENT paragraph (#PCDATA | emphasis | link)*>` (Allows text mixed with `emphasis` and `link` elements).

**Occurrence Indicators:** Appended to element names or groups to control repetition:
*   `?`: Zero or one occurrence.
*   `*`: Zero or more occurrences.
*   `+`: One or more occurrences.
*   (No indicator): Exactly one occurrence.


Below is a concise explanation of how `#PCDATA` and `CDATA` differ in a DTD context, followed by two concrete examples showing the DTD declarations and matching XML documents—one for an element whose content is parsed character data, and one for an attribute whose type is CDATA.

---

## Explanation

**`#PCDATA`**

- Stands for **Parsed Character Data**.
    
- Used **only** in element content models in a DTD (e.g. `<!ELEMENT title (#PCDATA)>`).
    
- The XML parser will interpret markup characters (`<`, `&`) inside that text, so you must escape them (`&lt;`, `&amp;`) if you want them as literal characters.
    
- You can mix `#PCDATA` with child elements in a “mixed” content model (e.g. `(#PCDATA | emph | link)*`).
    

**`CDATA`**

- In a DTD, **not** for element content but for **attribute types** (e.g. `<!ATTLIST product code CDATA #REQUIRED>`).
    
- Indicates the attribute value is taken as a literal string; the parser does **not** try to treat `<` or `&` inside that value as markup (though in the XML file itself you still escape `&` and the quote character delimiting the attribute).
    
- Completely separate from CDATA sections (`<![CDATA[ ... ]]>`) in XML document content.
    

---

## Example 1: Element with `#PCDATA`

### DTD (`catalog.dtd`)

```dtd
<!ELEMENT book (title, author, description)>
<!ELEMENT title (#PCDATA)>
<!ELEMENT author (#PCDATA)>
<!ELEMENT description (#PCDATA)>
```

### XML Document (`catalog.xml`)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE catalog [
  <!ELEMENT catalog (book*)>
  <!ENTITY copy "©">
  <!-- Include the external DTD -->
  <!ENTITY % bookDTD SYSTEM "catalog.dtd">
  %bookDTD;
]>
<catalog>
  <book>
    <title>Understanding XML &amp; DTDs</title>
    <author>Jane Doe</author>
    <description>
      This book explains how to write DTDs, use &lt;!ELEMENT&gt; declarations
      and work with entities like the copyright symbol (&copy;).
    </description>
  </book>
</catalog>
```

- In `<title>…</title>` and `<description>…</description>`, the parser resolves `&amp;`, `&lt;` and `&copy;` because they live within `#PCDATA` content.
    

---

## Example 2: Attribute of Type `CDATA`

### DTD (`product.dtd`)

```dtd
<!ELEMENT product EMPTY>
<!ATTLIST product
          code    CDATA   #REQUIRED
          name    CDATA   #IMPLIED
          url     CDATA   "http://example.com/default">
```

### XML Document (`products.xml`)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE products [
  <!ELEMENT products (product*)>
  <!-- Include the external DTD -->
  <!ENTITY % prodDTD SYSTEM "product.dtd">
  %prodDTD;
]>
<products>
  <product
    code="X100-&amp;-Z200"
    name="Widget <Deluxe>"
    url="http://example.com/page?id=1&amp;type=A"/>
  <product
    code="Y300"
    name="Gadget &quot;Pro&quot;"
    <!-- url will default to the DTD’s default attribute value -->
  />
</products>
```

- The `code`, `name` and `url` attributes are typed as `CDATA`. The parser treats their values as literal strings. Within the XML you still escape `&` and the quoting character for correctness, but you are not defining further parsing rules in the DTD beyond “any character data.”
    

---

By comparing these two patterns, you can see that:

- **`#PCDATA`** enforces parsed text inside element content, requiring escaping of markup.
    
- **`CDATA`** (as an attribute type) imposes no further parsing on the attribute value beyond standard XML escaping rules.
    

Use each in its proper context: elements for `#PCDATA`, attributes for `CDATA`.






[[1. DTD_Examples]]
### DTD : Déclaration des attributs (`<!ATTLIST ...>`)

#tags: #DTD #ATTLIST #attribute_type #CDATA #ID #IDREF #IDREFS #NMTOKEN #NMTOKENS #ENTITY #ENTITIES #Notation #Enumerated_attribute #REQUIRED #IMPLIED #FIXED #DEFAULT

*   **Syntax:** `<!ATTLIST ElementName AttributeName AttributeType Mode DefaultValue?>`
    *   Can define multiple attributes for the *same* `ElementName` within one `<!ATTLIST>` declaration or use separate declarations.
*   **`ElementName`:** The element type these attributes belong to.
*   **`AttributeName`:** The name of the attribute being defined.
*   **`AttributeType`:** Specifies the type of data the attribute value can hold:
    *   `CDATA`: Character Data (any string of text). Most common type.
    *   `ID`: The value must be a unique identifier within the document (conforms to XML Name rules, must be unique across all ID attributes).
    *   `IDREF`: The value must match the value of an `ID` attribute on some element elsewhere in the document.
    *   `IDREFS`: A space-separated list of `IDREF` values.
    *   `NMTOKEN`: Name Token (value must conform to XML Nmtoken rules - allows more characters than Name, like numbers at the start).
    *   `NMTOKENS`: A space-separated list of `NMTOKEN` values.
    *   `ENTITY`: Value must be the name of a declared *unparsed* general entity.
    *   `ENTITIES`: A space-separated list of `ENTITY` names.
    *   `NOTATION (notation1|notation2|...)`: Value must be the name of a declared `NOTATION`. (Attribute type is `NOTATION`, values are restricted to the list).
    *   `(option1|option2|...)`: Enumerated Type. The value must be one of the specified literal strings.
*   **`Mode`:** Specifies whether the attribute is required or optional, or has a fixed/default value:
    *   `#REQUIRED`: The attribute must be present on every instance of the element.
    *   `#IMPLIED`: The attribute is optional.
    *   `#FIXED "fixedValue"`: The attribute, if present, *must* have the specified `fixedValue`. If omitted, the parser often supplies it with this value.
    *   `"defaultValue"` (Implicitly `#DEFAULT`): If the attribute is omitted, the parser will supply this `defaultValue`. The user *can* override it if they include the attribute.

**Example ATTLIST:**
```dtd
<!ATTLIST person
    id ID #REQUIRED          <!-- Unique ID for the person, mandatory -->
    gender (male|female) "female" <!-- Gender, defaults to female if omitted -->
    status CDATA #IMPLIED        <!-- Optional status text -->
    photo ENTITY #IMPLIED       <!-- Optional reference to an unparsed photo entity -->
    clearance NMTOKEN #FIXED "level3" <!-- Clearance must be "level3" if present -->
    refs IDREFS #IMPLIED       <!-- Optional list of references to other IDs -->
>
```

### DTD : Exemple 1 de DTD

#tags: #DTD_example

This DTD corresponds to the XML structure shown in Slide 14.

```dtd
<!-- Defines the 'charge' element containing one or more 'cours' elements -->
<!ELEMENT charge (cours+)>

<!-- Defines the 'cours' element containing designation, auteur, Specialite in sequence -->
<!ELEMENT cours (designation, auteur, Specialite)>
  <!-- Defines attributes for 'cours': a required 'id' attribute of type CDATA -->
  <!ATTLIST cours 
      id CDATA #REQUIRED>

<!-- Defines 'designation' element containing only text -->
<!ELEMENT designation (#PCDATA)>

<!-- Defines 'auteur' element containing only text -->
<!ELEMENT auteur (#PCDATA)>

<!-- Defines 'Specialite' element containing only text -->
<!ELEMENT Specialite (#PCDATA)> 
```

### DTD : Exemple 2 de DTD (XML + DTD)

#tags: #DTD_example #external_DTD

**`message.xml` (Document Instance):**

```xml
<?xml version="1.0" encoding="ISO-8859-1" standalone="no"?> 
<!DOCTYPE message SYSTEM "message.dtd"> <!-- Link to external DTD -->
<message>
  <expediteur>
    <identite>
      <prenom>boustil</prenom>
      <nom age="23" sexe="f">amel</nom> <!-- Note attributes on 'nom' -->
      <email>boustil1710</email> 
    </identite>
  </expediteur>
  <destinataire>
    <identite>
      <prenom>Golbreich</prenom>
      <nom age="32" sexe="f">christine</nom> 
      <email>Golbreich.christine</email> 
    </identite>
  </destinataire>
  <objet>salut</objet>
</message>
```

**`message.dtd` (External DTD File):**

```dtd
<!ELEMENT message (expediteur, destinataire, objet)>
<!ELEMENT expediteur (identite)>
<!ELEMENT destinataire (identite)>
<!ELEMENT identite (prenom, nom, email?)> <!-- email is optional '?' -->
<!ELEMENT prenom (#PCDATA)>
<!ELEMENT nom (#PCDATA)>
  <!ATTLIST nom 
      age CDATA #IMPLIED        <!-- age is optional -->
      sexe (m|f) #REQUIRED>    <!-- sexe is required, must be 'm' or 'f' -->
<!ELEMENT email ANY>            <!-- Allows any content (discouraged) -->
<!ELEMENT objet ANY>            <!-- Allows any content (discouraged) -->
```
*   This shows how an external DTD (`message.dtd`) defines the structure validated in `message.xml`.

### DTD : Les entités dans les DTD (Entities in DTDs)
[[1. Entities Quiz]]
#tags: #DTD #XML_entity #general_entity #parameter_entity #character_entity #reusability

*   **Definition:** Entities are named placeholders for content. They allow you to define a piece of content once (text, markup, external resource) and reuse it by referencing its name.
*   **Purpose:** Promote reusability, manage repetitive data, include external content, and handle special characters.
*   **Types of Entities:**
    1.  **Entités générales (General Entities):** Used within the *XML document content*. Referenced using `&entity-name;`.
    2.  **Entités paramètres (Parameter Entities):** Used *only within the DTD itself* (markup declarations). Referenced using `%entity-name;`. Crucial for modularizing and reusing parts of DTDs.
    3.  **Entités caractères (Character Entities):** Predefined general entities for representing characters that have special meaning in XML syntax (e.g., `&lt;`, `&gt;`, `&amp;`, `&apos;`, `&quot;`). Also includes numeric character references (`&#nnn;` or `&#xhhh;`).

### DTD : Entités générales (General Entities)

#tags: #general_entity #ENTITY #internal_entity #external_entity #parsed_entity #unparsed_entity

*   **Purpose:** Define reusable content snippets or references to external resources to be included in the XML document instance.
*   **Declaration (in DTD):**
    *   **Interne (Internal):** `<!ENTITY entity-name "replacement text">`
        *   The `replacement text` is literal character data and markup. It is parsed along with the document content where referenced.
    *   **Externe (External Parsed):** `<!ENTITY entity-name SYSTEM "URI/to/external.xml">`
        *   The content is fetched from the external URI and *parsed* as XML content at the point of reference.
    *   **Externe (External Unparsed):** `<!ENTITY entity-name SYSTEM "URI/to/non-xml.dat" NDATA notationName>`
        *   References external non-XML data (e.g., image). Requires a `NOTATION` declaration (`notationName`) to identify the data type. The parser doesn't parse this data but makes the reference available to the application.
*   **Reference (in XML document content):** `&entity-name;`

**Exemple (Internal General Entity):**

```dtd
<!-- DTD Declaration -->
<!ENTITY website "http://www.monsite.com"> 
<!ENTITY copyright "&#169; 2024 Me, Inc."> <!-- Can contain character references -->
```

```xml
<!-- XML Usage -->
<url>Le site du cours DSS est : &website;</url>
<footer>&copyright;</footer> 
```

**Result after parsing:**

```xml
<url>Le site du cours DSS est : http://www.monsite.com</url>
<footer>© 2024 Me, Inc.</footer> 
```

### DTD : Entités paramètres (Parameter Entities)

#tags: #parameter_entity #ENTITY #DTD_reusability #internal_entity #external_entity

*   **Purpose:** Used exclusively *within the DTD* itself to achieve modularity and reusability of DTD declarations or parts of declarations. They help create more maintainable and flexible DTDs.
*   **Distinction:** Marked by the percent sign (`%`) in both declaration and reference.
*   **Declaration (in DTD):**
    *   **Interne (Internal):** `<!ENTITY % entity-name "declaration text">`
        *   `declaration text` contains DTD markup declarations or parts thereof.
    *   **Externe (External):** `<!ENTITY % entity-name SYSTEM "URI/to/external.dtd">`
        *   Fetches DTD declarations from an external file. Used to include shared DTD modules.
*   **Reference (only within DTD markup declarations):** `%entity-name;`

**Exemple (Internal Parameter Entity):**

```dtd
<!-- DTD Declarations -->

<!-- Define common attributes as a parameter entity -->
<!ENTITY % commonAttrs "
    id ID #IMPLIED
    class CDATA #IMPLIED
">

<!-- Define content model part as a parameter entity -->
<!ENTITY % shapeContent "(description?, notes?)">

<!-- Use the parameter entities in element declarations -->
<!ELEMENT rectangle (%shapeContent;)>
<!ATTLIST rectangle
    %commonAttrs; <!-- Reference common attributes -->
    width CDATA #REQUIRED
    height CDATA #REQUIRED
>

<!ELEMENT circle (%shapeContent;)>
<!ATTLIST circle
    %commonAttrs; <!-- Reference common attributes -->
    radius CDATA #REQUIRED
>

<!-- The DTD fragment from the slide -->
<!ENTITY % commun "niveau, couleur"> <!-- Defines %commun; -->

<!ELEMENT rectangle (%commun;, sommet+)> <!-- Equivalent to (niveau, couleur, sommet+) -->
<!ELEMENT triangle (%commun;, sommet+)> <!-- Equivalent to (niveau, couleur, sommet+) -->
<!ELEMENT disque (%commun;, centre, rayon)> <!-- Equivalent to (niveau, couleur, centre, rayon) -->
```

### DTD : Entités caractères (Character Entities)

#tags: #character_entity #predefined_entities #XML_special_characters #numeric_character_reference #Unicode

*   **Purpose:** Allow representation of characters that have special syntactic meaning in XML (like `<`, `&`) or characters not easily typable.
*   **Predefined Character Entities (General Entities):**
    *   `&amp;` → `&` (Ampersand)
    *   `&lt;` → `<` (Less-than sign)
    *   `&gt;` → `>` (Greater-than sign)
    *   `&apos;` → `'` (Apostrophe / Single quote)
    *   `&quot;` → `"` (Quotation mark / Double quote)
*   **Numeric Character References:** Allow representing *any* Unicode character using its code point number.
    *   **Decimal:** `&#decimal-code-point;` (e.g., `&#169;` for ©)
    *   **Hexadecimal:** `&#xhex-code-point;` (e.g., `&#x00A9;` for ©)
*   **Usage:** Used within element content and attribute values in the XML document instance.
*   **Example from Slide:**
    *   Using `&#960;` or `&#x03C0;` inserts the Greek letter pi (π).
    *   You *can* define a named entity using a numeric reference in the DTD: `<!ENTITY pi "&#x03C0;">`, then use `&pi;` in the XML.

### DTD : Les notations (`<!NOTATION ...>`)

#tags: #DTD #NOTATION #unparsed_entity #binary_data #helper_application #MIME_type

*   **Purpose:** Notations declare a name for a specific format of **non-XML (unparsed)** data. They provide metadata about the format, potentially linking it to a helper application or a standard identifier (like a MIME type).
*   **Usage:** Primarily used in conjunction with:
    *   **Unparsed External General Entities:** Declared with `NDATA notationName`.
    *   **Attributes of type `NOTATION`:** Restricting attribute values to declared notation names.
*   **Declaration Syntax:**
    ```dtd
    <!NOTATION NotationName SYSTEM "HelperApplicationURI_OR_FormatIdentifier"> 
    <!-- OR -->
    <!NOTATION NotationName PUBLIC "PublicIdentifier" ["SystemIdentifier"]>
    ```
    *   `NotationName`: The name used to refer to this format.
    *   `SYSTEM`: Provides a URI that might identify the format or a helper application.
    *   `PUBLIC`: Provides a Formal Public Identifier (FPI) for the format (e.g., MIME type like `"image/gif"` or standard IDs like `"-//CompuServe//NOTATION Graphics Interchange Format 89a//EN"`). A system identifier can be a fallback.

*   **Example:**
    ```dtd
    <!-- Declare notations for image formats -->
    <!NOTATION gif PUBLIC "image/gif"> 
    <!NOTATION jpeg PUBLIC "image/jpeg">
    <!NOTATION png SYSTEM "viewer.exe"> <!-- Associates png with a viewer app -->

    <!-- Declare an unparsed entity using a notation -->
    <!ENTITY companyLogo SYSTEM "logo.gif" NDATA gif>

    <!-- Declare an element with an attribute referencing notations -->
    <!ELEMENT image EMPTY>
    <!ATTLIST image
        src ENTITY #REQUIRED        <!-- Reference to an unparsed entity -->
        format NOTATION (gif|jpeg|png) #REQUIRED <!-- Value must be gif, jpeg, or png -->
    >
    ```
*   **Note on Slide 83 Example:** The slide shows `<xs:notation ...>` which is **XML Schema syntax**, not DTD. The DTD concept is as described above.

---

## NameSpace XML (XML Namespaces)

#tags: #XML_namespace #namespace #vocabulary #naming_conflict #URI #namespace_prefix #default_namespace #xmlns
[[1. Namespace Quiz]]
### Définition & Problème (Definition & Problem)

*   **Vocabulaire XML (XML Vocabulary):** A defined set of element and attribute names with specific meanings for a particular domain or application (e.g., the HTML vocabulary, the MathML vocabulary, a custom vocabulary for purchase orders).
*   **Problème (Problem):** When combining elements and attributes from different XML vocabularies within the same document, name collisions can occur. For example, `<title>` might mean "book title" in one vocabulary and "person's job title" in another. How does a processor distinguish them? (See Slide 85 for illustration).
*   **Solution:** XML Namespaces provide a mechanism to uniquely identify elements and attributes by associating them with a **namespace name** (a URI).

### Solution : les nameSpaces

*   **Mechanism:**
    1.  **Associate:** Elements and attributes are associated with a unique namespace name, which is syntactically a **URI**. The URI itself isn't typically fetched; it just serves as a unique identifier.
    2.  **Qualify:** Element and attribute names can be *qualified* with a namespace **prefix**, which acts as a short alias for the long URI.
*   **Result:** Names like `book:title` and `person:title` become distinct because the prefixes `book:` and `person:` are bound to different namespace URIs.

**Example (Resolving the problem from Slide 85):**

```xml
<?xml version="1.0"?>
<!-- Assume crs maps to course vocabulary URI, pers maps to person vocabulary URI -->
<document xmlns:crs="http://www.example.com/courses" 
          xmlns:pers="http://www.example.com/personnel">

  <crs:cours>
    <crs:titre>Theorie des langages</crs:titre> <!-- Course title -->
    <crs:specialite>Licence Informatique</crs:specialite>
  </crs:cours>
  
  <pers:auteur>
    <pers:nom>Boustil</pers:nom>
    <pers:prenom>Amel</pers:prenom>
    <pers:titre>Maitre de conférence</pers:titre> <!-- Person title -->
  </pers:auteur>

</document>
```

### Espaces de noms : Déclarations (Namespace Declarations)

#tags: #namespace_declaration #default_namespace #prefixed_namespace #xmlns #namespace_scope

Namespaces are declared using attributes starting with `xmlns`:

1.  **Default Namespace Declaration:**
    *   **Syntax:** `xmlns="URI"`
    *   **Effect:** Declares the default namespace for the element it appears on and all its descendants *that do not have a prefix*. Unprefixed element names are considered part of this default namespace. Unprefixed *attribute* names are *never* part of the default namespace; they are always in "no namespace".
    *   **Example:** `<html xmlns="http://www.w3.org/1999/xhtml">...</html>` (All unprefixed elements inside are XHTML elements).

2.  **Prefixed Namespace Declaration:**
    *   **Syntax:** `xmlns:prefix="URI"`
    *   **Effect:** Binds the chosen `prefix` to the specified namespace `URI`. Elements and attributes whose names start with `prefix:` belong to this namespace.
    *   **Example:** `<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform">...</xsl:stylesheet>`

**Scope:** A namespace declaration applies to the element where it is declared and all descendant elements, unless overridden by another declaration of the same prefix or the default namespace on a child element.

### Quelques remarques sur les espaces de noms (Remarks on Namespaces)

*   **Declaration Location:** Namespaces can be declared on the root element for document-wide scope or on any element where they are needed, providing scope for that element and its children.
*   **Default Namespace Benefit:** Using a default namespace avoids repetitive prefixing for elements belonging to the primary vocabulary of a document section. (See Slide 89 `<person>` example).
*   **Changing Defaults:** A default namespace declaration on a child element overrides the default namespace inherited from its parent for itself and its descendants. (See Slide 89 `<adress>` example).
*   **Mixing Namespaces:** Documents commonly mix default namespaces and prefixed namespaces. (See Slide 88 example mixing (implied) HTML and a custom `f:` namespace).

### La suppression d'un espace de noms (Undeclaring a Namespace)

#tags: #namespace_undeclaration #no_namespace #default_namespace

*   **"No Namespace":** Elements or attributes without a prefix and with no default namespace in scope are considered to be in "no namespace".
*   **Undeclaring the Default Namespace:** To revert to "no namespace" within a scope where a default namespace was previously declared, you can declare the default namespace with an empty string value:
    *   **Syntax:** `xmlns=""`
    *   **Effect:** This cancels the default namespace for the element it's on and its descendants (unless they use prefixes or redeclare a default namespace). Unprefixed elements within this scope will be in "no namespace".
*   **Example (Slide 90):**
    ```xml
    <person xmlns="http://www.namespacePerso"> <!-- Default is Perso -->
      <name>...</name> <!-- In Perso namespace -->
      <adress xmlns=""> <!-- Default is now NO namespace -->
        <street>...</street> <!-- In NO namespace -->
        <pays>12</pays> <!-- In NO namespace -->
      </adress>
    </person>
    ```
*   **Note:** You cannot "undeclare" a prefix in the same way. A prefix remains bound to its URI within its scope.

### Application d'un espace de noms sur un attribut (Namespaces on Attributes)

#tags: #namespace_attribute #prefixed_attribute #xml_namespace

*   **Unprefixed Attributes:** Are *never* associated with a default namespace. They are always in "no namespace".
*   **Prefixed Attributes:** Attributes can belong to a namespace if their names are qualified with a declared prefix.
    *   **Syntax:** `<element prefix:attributeName="value">`
    *   **Purpose:** Allows using attributes from different vocabularies on the same element without conflict (e.g., `html:class="..."` and `xlink:type="..."`).
*   **Example (Slide 91 corrected interpretation):**
    ```xml
    <person xmlns:im="http://www.example.com/imagemeta" 
            im:weight="50kg" 
            im:units="metric"> 
    <!-- The 'weight' and 'units' attributes belong to the 'im' namespace -->
      ... 
    </person>
    ```
*   **`xml:` Prefix:** The prefix `xml` is reserved for the XML namespace (`http://www.w3.org/XML/1998/namespace`) and is used for predefined attributes like `xml:lang`, `xml:space`, `xml:base`, `xml:id`. It does not need to be declared.

### Espaces de noms et DTD (Namespaces and DTD)

#tags: #DTD #XML_namespace #namespace_validation #fixed_attribute

*   **DTD Awareness:** DTDs are **not** inherently namespace-aware. They treat a prefixed name like `prefix:name` as a single, literal name.
*   **Validation:** To validate a namespace-using document with a DTD, the DTD must:
    *   Declare elements using their literal prefixed names (e.g., `<!ELEMENT xsl:stylesheet ...>`).
    *   Declare attributes using their literal prefixed names (e.g., `<!ATTLIST my:element other:attr ...>`).
    *   Declare the `xmlns` and `xmlns:prefix` attributes themselves, often using `#FIXED` to ensure the correct namespace URIs are associated.
*   **Example (Declaring `xmlns:svg` in DTD - Slide 92 corrected):**
    ```dtd
    <!-- In message.dtd -->
    <!ELEMENT svg:svg ... > <!-- Must declare prefixed element name -->
      <!ATTLIST svg:svg 
          xmlns:svg CDATA #FIXED "http://www.w3.org/2000/svg" <!-- Fix the prefix decl -->
          width CDATA #IMPLIED
          height CDATA #IMPLIED
          ... >
    <!ELEMENT svg:rect ... > <!-- Must declare prefixed element name -->
      <!ATTLIST svg:rect 
          x CDATA #IMPLIED
          y CDATA #IMPLIED 
          ... > 
    ```
    ```xml
    <!-- In message.xml -->
    <!DOCTYPE svg:svg SYSTEM "message.dtd"> <!-- Root element must match DTD -->
    <svg:svg width="10cm" height="5cm"> <!-- No xmlns:svg needed here -->
       <svg:rect x="1" y="1" width="8cm" height="3cm"/>
    </svg:svg>
    ```
*   **Limitation:** This approach is cumbersome and doesn't fully capture namespace semantics. XML Schema (XSD) is namespace-aware and preferred for validating namespace-using documents.

### Quelques espaces de noms célèbres (Common Namespaces)

#tags: #XHTML #MathML #SVG #XSLT #XML_Schema #RDF #Dublin_Core #common_namespaces #namespace_URI

*   **XHTML:** `http://www.w3.org/1999/xhtml`
*   **MathML:** `http://www.w3.org/1998/Math/MathML`
*   **SVG:** `http://www.w3.org/2000/svg`
*   **XSLT:** `http://www.w3.org/1999/XSL/Transform`
*   **XML Schema (Elements):** `http://www.w3.org/2001/XMLSchema` (Common prefix: `xs` or `xsd`)
*   **XML Schema (Instance):** `http://www.w3.org/2001/XMLSchema-instance` (Common prefix: `xsi`)
*   **RDF (Resource Description Framework):** `http://www.w3.org/1999/02/22-rdf-syntax-ns#` (Common prefix: `rdf`) *(Note: Slide 93 shows `http://www.w3.org/TR/REC-rdf-syntax#`)*
*   **Dublin Core:** `http://purl.org/dc/elements/1.1/` (Common prefix: `dc`) *(Note: Slide 93 shows `http://purl.org/dc/`)*

### Exemple d'utilisation d'un espace de noms existants SVG

#tags: #SVG #SVG_example #default_namespace #XML_rendering #browser

This example uses the SVG namespace as the **default namespace** to create a simple vector graphic.

```xml
<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200"> <!-- SVG is default -->
  <title>Rectangles</title> <!-- 'title' is an SVG element -->
  
  <!-- 'rect' and its attributes (width, height, x, y, fill) are all SVG elements/attributes -->
  <rect width="300" height="100" x="0" y="20" fill="green" /> 
  <rect width="80" height="150" x="20" y="30" fill="red" /> 
  <rect width="140" height="80" x="50" y="50" fill="blue" /> 
</svg>
```

*   **Result:** When opened in a modern web browser that supports SVG, this XML file will render as an image showing three overlapping rectangles (green, red, blue). The browser understands the SVG vocabulary defined by the namespace `http://www.w3.org/2000/svg`.

---


