## 1. Généralités (General Concepts)

### Présentation du XSLT (Introduction to XSLT)

#tags: #XSL #XSLT #XSL_FO #transformation #styling #formatting #W3C

*   **XSL (eXtensible Stylesheet Language):** A family of W3C recommendations covering the transformation and styling of XML documents. It comprises two main languages:
    *   **XSLT (eXtensible Stylesheet Language Transformations):** Transforms an input XML document into another format. This output can be another XML document (possibly with a different structure), HTML, plain text, or other formats.
    *   **XSL-FO (eXtensible Stylesheet Language - Formatting Objects):** An XML vocabulary used to specify pagination, layout, and styling information for the final presentation of XML data, often targeting formats like PDF, PostScript (PS), or Rich Text Format (RTF). It describes the desired *visual* result.

*   **Processing Flow (Diagram - Slide 4):**
    1.  An **XSLT Processor** takes two inputs:
        *   The source **XML Document**.
        *   The **XSLT Stylesheet** (an XML document defining transformation rules, often ending in `.xsl` or `.xslt`).
    2.  The processor applies the rules from the stylesheet to the source XML.
    3.  The output (**Result Tree**) can be:
        *   Another **XML Document**.
        *   A **Text Document**.
        *   An **XHTML/HTML Document** (which can then be rendered by a browser, potentially styled with CSS).
        *   An **XSL-FO Document**.
    4.  If the output is an XSL-FO document, a separate **XSL-FO Processor** takes this document as input and generates a final formatted output like **PDF**, **PS**, **RTF**, etc.

### Premier Exemple (First Example - XSLT Stylesheet)

#tags: #XSLT #example #stylesheet #template_rule #match_attribute #HTML_output

This is a minimal XSLT stylesheet that transforms *any* XML document into a simple fixed HTML page.

```xml
<?xml version="1.0" encoding="iso-8859-1"?> 
<!-- XSLT Stylesheet Root Element -->
<xsl:stylesheet version="1.0" 
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                xmlns="http://www.w3.org/1999/xhtml"> 
                <!-- Default namespace for literal result elements (HTML) -->

  <!-- Template Rule: Matches the root node of the source XML -->
  <xsl:template match="/"> 
    <!-- Literal Result Elements (HTML output) -->
    <html>
      <head>
        <title>Bonjour Les L3!</title>
      </head>
      <body>
        <h1>Hello world!</h1>
      </body>
    </html>
  </xsl:template> 

</xsl:stylesheet>
```

*   **`<xsl:stylesheet>`:** The root element, declaring the XSLT namespace (`xmlns:xsl`).
*   **`version="1.0"`:** Specifies XSLT version 1.0.
*   **`xmlns="..."`:** Declares the default namespace for elements *created* by the stylesheet (literal result elements). Here it's set to XHTML.
*   **`<xsl:template match="/">`:** Defines a template rule. The `match="/"` attribute uses an XPath pattern to match the root node of the source XML document.
*   **Content of `<xsl:template>`:** Contains the structure to be output when this template rule is activated. Here, it's literal HTML markup.

### Premier Exemple : Résultat (First Example: Result)

#tags: #XSLT #example #result_document #HTML_output #transformation

Applying the previous XSLT stylesheet to *any* well-formed XML document using an XSLT processor will produce the following output document (an HTML file):

```html
<?xml version="1.0" encoding="utf-8"?> <!-- Output encoding may vary -->
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> <!-- Often added by processor -->
    <title>Bonjour les L3!</title>
  </head>
  <body>
    <h1>Hello world!</h1>
  </body>
</html>
```

*   The result is the literal HTML structure defined inside the `<xsl:template match="/">` rule in the stylesheet.
*   The XSLT processor copied the literal elements (`<html>`, `<head>`, etc.) to the output.

### XSLT est donc... (What XSLT Is...)

#tags: #XSLT #definition #transformation #XML #HTML #text #W3C #XPath #processor

*   **Technology:** XSLT is a technology for **transforming** information from a source **XML document** into another document type (XML, HTML, text).
*   **Association:** An XSLT stylesheet document (`.xsl`) is associated with a source XML document to create a new result document.
*   **Standard:** XSLT is an XML application itself (written in XML) and is a **W3C standard**.
    *   Version 1.0: 1999
    *   Version 2.0: 2007
    *   Version 3.0: 2017
*   **Dependency:** XSLT relies heavily on **XPath** for selecting information (nodes) from the source XML document to be transformed.
*   **Instructions:** XSLT elements (like `<xsl:value-of>`, `<xsl:apply-templates>`) are instructions executed by the **XSLT processor**.
*   **Processing Diagram (Slide 8):** Input XML + Input XSLT -> XSLT Processor -> Output Document (XML, HTML, PDF via XSL-FO, etc.).

---

## 2. Structure d'une feuille de style (Stylesheet Structure)

#tags: #XSLT #stylesheet #structure #root_element #xsl_stylesheet #xsl_transform #xsl_output #xsl_template

An XSLT stylesheet is an XML document with a specific structure:

*   **Root Element:** Must be `<xsl:stylesheet>` or its synonym `<xsl:transform>`.
    *   **`version` attribute:** Specifies the XSLT version (e.g., "1.0", "2.0", "3.0"). `1.0` is common.
    *   **`xmlns:xsl` attribute:** Declares the XSLT namespace (`http://www.w3.org/1999/XSL/Transform`), associating it with the `xsl` prefix. This is mandatory.
*   **Top-Level Elements:** Children of the root element define the transformation details:
    *   **`<xsl:output>`:** (Optional) Specifies formatting details for the result document (e.g., output method, encoding, indentation).
    *   **`<xsl:template>`:** Defines template rules, which specify how different parts of the source XML should be transformed. This is the core of the stylesheet.
    *   *(Other top-level elements exist: `<xsl:import>`, `<xsl:include>`, `<xsl:param>`, `<xsl:variable>`, `<xsl:key>`, `<xsl:attribute-set>`, etc.)*

**Example Skeleton (Slide 10):**

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- entete --> 
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <!-- DECLARATIONS -->
  <xsl:output method="..." .../> <!-- Output formatting -->
  
  <!-- LISTE DES REGLES (Templates) -->
  
  <!-- modèle de transformation 1 -->
  <xsl:template match="..."> 
    ... 
  </xsl:template>

  <!-- modèle de transformation 2 -->
  <xsl:template match="...">
    ...
  </xsl:template>
  
  ...

  <!-- modèle de transformation n -->
  <xsl:template match="...">
    ...
  </xsl:template>

</xsl:stylesheet>
```

### Déclaration d'output (`<xsl:output>`)

#tags: #XSLT #xsl_output #result_format #method #encoding #indent #doctype

*   **Purpose:** The top-level `<xsl:output/>` element provides instructions to the XSLT processor on how to format and serialize the final result tree (the output document).
*   **Key Attributes:**
    *   **`method`:** Specifies the desired output format. Common values:
        *   `"xml"` (Default if output looks like XML): Standard XML output, includes XML declaration. Empty tags like `<br/>`.
        *   `"html"`: HTML output. Understands HTML tag semantics (e.g., empty tags like `<br>`, non-XML entities like `&nbsp;`). Usually omits XML declaration.
        *   `"xhtml"` (XSLT 2.0+): Outputs well-formed XHTML, follows XML rules for empty tags, includes relevant DOCTYPE.
        *   `"text"`: Plain text output. All markup is stripped or converted to text content.
    *   **`encoding`:** Specifies the character encoding for the output file (e.g., `"UTF-8"`, `"ISO-8859-1"`). Defaults often depend on the processor or system.
    *   **`indent`:** Controls whether the processor should add whitespace to "pretty-print" the output.
        *   `"yes"`: Enables indentation (useful for readability).
        *   `"no"` (Default): No extra indentation is added.
    *   **`doctype-public` / `doctype-system`:** Specifies the PUBLIC and SYSTEM identifiers to be included in a `<!DOCTYPE>` declaration in the output (relevant for `xml` and `html` methods).

**Example (Slide 12):**

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- l'élément racine -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  
  <!-- l'élément output -->
  <xsl:output 
      method="html" 
      encoding="UTF-8"
      doctype-public="-//W3C//DTD HTML 4.01//EN"
      doctype-system="http://www.w3.org/TR/html4/strict.dtd"
      indent="yes"/>

  <!-- contenu du template -->
  <xsl:template match="/">
     <!-- ... HTML generation ... -->
  </xsl:template>

</xsl:stylesheet>
```

---

## 3. Modèle de traitement (Processing Model)

#tags: #XSLT #processing_model #template_rule #node_processing #context_node #result_tree #xsl_apply_templates

XSLT processing is driven by template rules and node traversal:

1.  **Source Document:** The input XML document is parsed into a tree structure.
2.  **Applying Rules:** The XSLT processor starts by finding a template rule (`<xsl:template>`) that matches the **root node** (`/`) of the source document.
3.  **Rule Instantiation:** The content of the matching template rule is processed (instantiated). This content can include:
    *   **Literal Result Elements:** Markup (like HTML tags) directly included in the template is copied to the result tree.
    *   **XSLT Instructions:** Elements from the `xsl:` namespace are executed.
4.  **Fragment Creation:** Each instantiated template rule produces a fragment of the result document.
5.  **Assembly:** These fragments are assembled (concatenated based on processing order) to form the final result document.
6.  **Recursion (`<xsl:apply-templates>`):** The key instruction `<xsl:apply-templates>` directs the processor to find and apply the best matching template rules for the *children* (or other selected nodes) of the current node (the context node). This recursive process drives the traversal of the source tree and the construction of the result tree.

*   **`<xsl:template>`:** Defines *how* to transform a specific type of node (matched by `match` attribute).
*   **`<xsl:apply-templates>`:** Defines *which* nodes to process next, triggering the search for matching templates for those nodes.

---

## 4. Structure d'une règle (Rule Structure - Templates)

#tags: #XSLT #xsl_template #template_rule #match_attribute #name_attribute #XPath #pattern #xsl_apply_templates #xsl_call_template

*   **Definition:** A rule is defined by the `<xsl:template>` element. It specifies what output to generate when a particular node (or set of nodes) in the source document is matched.
*   **Identification:** Templates are primarily identified and selected using the `match` attribute, but can also be named using the `name` attribute for explicit calls.
*   **Key Attributes:**
    *   **`match`:** Contains an **XPath pattern** (a subset of XPath expressions). This pattern is used by the processor (during `<xsl:apply-templates>`) to select which template rule to apply to a given source node. It specifies the *condition* under which the template should be invoked.
        *   Definition Syntax: `<xsl:template match="XPathPattern"> ... </xsl:template>`
        *   Invocation: Implicitly via `<xsl:apply-templates select="XPathExpression"/>` (processor finds the best match for selected nodes).
    *   **`name`:** Assigns a unique name to the template. This allows the template to be called explicitly like a function, using `<xsl:call-template>`. Named templates do *not* need a `match` attribute (though they can have one).
        *   Definition Syntax: `<xsl:template name="TemplateName"> ... </xsl:template>`
        *   Invocation: Explicitly via `<xsl:call-template name="TemplateName"/>`.

### Modèle d'exécution pour l'attribut `match` (Execution Model for `match` Attribute)

#tags: #XSLT #processing_model #context_node #template_matching #recursion #depth_first

The execution flow when using `match` and `apply-templates` is typically recursive and depth-first:

1.  **Context Node:** Processing always happens relative to a **current node** (contexte node) in the source XML tree. Initially, this is the root node (`/`).
2.  **Find Matching Template:** The processor searches for the template rule whose `match` pattern best fits the current context node. (Conflict resolution rules apply if multiple templates match - see Priority section).
3.  **Instantiate Template:** The content of the selected template is instantiated.
4.  **Process Children (Recursive Step):** If the template contains `<xsl:apply-templates>`, the processor selects the children (or nodes specified by the `select` attribute) of the *current source context node*. For each selected node, it repeats the process from Step 2 (find best matching template for *that* node).
5.  **Continue:** This continues recursively down the source tree. The output fragments generated by each template instantiation are assembled in order.

**Example Flow (Slide 15 & 18):**

*   Start at `/`. Template `match="/"` is found.
*   `<html>`, `<head>`, `<title>` are output.
*   `<xsl:value-of select="CD/@nom"/>` gets the `nom` attribute of the `CD` element and outputs it inside `<title>`.
*   `<body>` is output.
*   `<xsl:apply-templates select="CD/artiste"/>` is encountered.
    *   Processor selects all `<artiste>` children of the `<CD>` element from the source XML.
    *   For *each* selected `<artiste>` node:
        *   The context node becomes the `<artiste>` element.
        *   The processor looks for the best template matching `artiste`. It finds `<xsl:template match="artiste">`.
        *   The content `<h1><xsl:value-of select="nom"/></h1>` is instantiated.
            *   `<xsl:value-of select="nom"/>` selects the text content of the `nom` child of the *current* `<artiste>` node and outputs it inside `<h1>`.
        *   The processor finishes processing the `<artiste>` template.
    *   After processing all selected `<artiste>` nodes, control returns to the `match="/"` template.
*   `</body>`, `</html>` are output.

**Source XML (Slide 17):**
```xml
<?xml-stylesheet type="text/xsl" href="artisteDevoir.xsl"?>
<CD nom="MON CD"> 
  <!-- Les artistes -->
  <artiste no="a01" ville="Constantine">
    <nom>FIRGANI mohamed Taher</nom>
    <site url="http://www.Mohamedfergani.dz"/>
    <biographie>Ne a constantine, grand cahnteur de malouf</biographie>
  </artiste>
  <artiste no="a03" ville="Alger">
    <nom>ALHACHEMI GUARRWABI</nom>
    <site url="http://www.AlhachemiGUATWABI.dz"/>
    <biographie>Ne a alger, grand chanteur de asimi</biographie>
  </artiste>
  <artiste no="a02" ville="Annaba">
    <nom>BENANI Hamdi</nom>
    <site url="http://www.Bennani Hamedi.dz"/>
    <biographie>Ne a Annaba, grand chanteur de malouf moderne</biographie>
  </artiste>
  <artiste no="a04" ville="TIZI OUZOU">
    <nom>IDIR</nom>
    <site url="http://www.IDIR.dz"/>
    <!-- Biographie might be missing or empty -->
  </artiste>
</CD>
```

**XSLT Stylesheet (Slide 18):**
```xml
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:template match="/"> 
    <html>
      <head>
        <title><xsl:value-of select="CD/@nom"/></title> 
      </head>
      <body bgcolor="#ffffff"> 
        mon Album est : <xsl:apply-templates select="CD/artiste"/> 
      </body>
    </html>
  </xsl:template>

  <xsl:template match="artiste"> 
    <h1 align="center"><xsl:value-of select="nom"/></h1> 
  </xsl:template>

</xsl:stylesheet>
```

**Result HTML (Slide 19):**
```html
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>MON CD</title>
  </head>
  <body bgcolor="#ffffff"> 
    mon Album est : 
    <h1 align="center">FIRGANI mohamed Taher</h1>
    <h1 align="center">ALHACHEMI GUARRWABI</h1>
    <h1 align="center">BENANI Hamdi</h1>
    <h1 align="center">IDIR</h1>
  </body>
</html>
```

---

## 5. Construction du document résultat (Constructing the Result Document)

#tags: #XSLT #result_tree #output_generation #xsl_value_of #xsl_copy_of #xsl_variable #xsl_for_each #xsl_if #xsl_choose #xsl_text #literal_result_element

Templates construct the result tree by combining literal result elements and the output of XSLT instructions. Key operations include:

*   **insérer la valeur d'un noeud du document d'entrée (Insert node value):** Use `<xsl:value-of>`.
*   **copier un fragment du document d'entrée (Copy input fragment):** Use `<xsl:copy>` or `<xsl:copy-of>`.
*   **insérer un nouvel élément de valeur 'statique' (Insert new static element):** Include literal result elements directly in the template.
*   **insérer un nouvel élément de valeur 'dynamique' (Insert new dynamic element):** Use instructions like `<xsl:element>`, `<xsl:attribute>`, often with values determined by XPath expressions.

### L'instruction `value-of`

#tags: #XSLT #xsl_value_of #select_attribute #text_content #XPath #output_value

*   **Purpose:** The `<xsl:value-of>` instruction calculates the **string value** of an XPath expression and inserts it as a **text node** into the result tree.
*   **Syntax:** `<xsl:value-of select="XPathExpression"/>`
*   **`select` attribute:** Contains the XPath expression.
*   **Behavior:**
    *   If the expression selects a node-set, it typically takes the string value of the *first* node in the set (in document order).
    *   If the expression selects an attribute, it inserts the attribute's value.
    *   If the expression calculates an atomic value (string, number, boolean), it converts it to a string and inserts it.

**Examples (Slide 21):**

```xml
<!-- Get string value of the first 'artiste' child -->
<xsl:value-of select="artiste"/> 

<!-- Get value of the 'date' attribute of the context node -->
<xsl:value-of select="@date"/> 

<!-- Get string value of the first 'chanson' child of the first 'chansons' child of the first 'album' child -->
<xsl:value-of select="/album/chansons/chanson"/> 

<!-- Get string value of the context node -->
<xsl:value-of select="."/> 

<!-- Get the count of 'chanson' elements anywhere in the document -->
<xsl:value-of select="count(//chanson)"/> 

<!-- Get the position of the context node among its siblings -->
<xsl:value-of select="position()"/> 
```

**Example with Function (Slide 22):**

```xml
<!-- Inside a template -->
<body>
  <!-- Aucune regle -->
  nombre d'artistes est : <xsl:value-of select="count(CD/artiste)"/> 
</body>

<!-- Result -->
<body>
  nombre d'artistes est : 4
</body>
```

### L'instruction `copy-of`

#tags: #XSLT #xsl_copy_of #deep_copy #node_copy #select_attribute #XPath

*   **Purpose:** The `<xsl:copy-of>` instruction performs a **deep copy** of the selected nodes. It copies the entire node(s) selected by the XPath expression, including child nodes, attributes, text content, etc., into the result tree.
*   **Syntax:** `<xsl:copy-of select="XPathExpression"/>`
*   **`select` attribute:** Contains the XPath expression selecting the node(s) to copy.
*   **Behavior:** Unlike `<xsl:value-of>` which extracts the string value, `<xsl:copy-of>` replicates the selected XML structure.

**Example (Slide 24):**

```xml
<!-- Inside a template -->
<!-- Get only the text value of the first matching 'nom' -->
<h2>nombre d'artistes est : <xsl:value-of select="CD/artiste/nom"/></h2> 
<!-- Copy the *entire* 'nom' element(s) found -->
<h3>noms d'artistes sont : <xsl:copy-of select="CD/artiste/nom"/></h3> 

<!-- Result -->
<body>
  <h2>nombre d'artistes est : FIRGANI mohamed Taher</h2> <!-- Only the first nom's text -->
  <h3>noms d'artistes sont : 
    <nom>FIRGANI mohamed Taher</nom> <!-- Copies all matching nom elements -->
    <nom>ALHACHEMI GUARRWABI</nom>
    <nom>BENANI Hamdi</nom>
    <nom>IDIR</nom>
  </h3>
</body>
```

### Les variables (`<xsl:variable>`)

#tags: #XSLT #xsl_variable #variable #select_attribute #name_attribute #XPath #reusability

*   **Purpose:** Allows storing a value (a node-set, string, number, boolean, or result tree fragment) in a named variable for reuse within the stylesheet. Useful for complex expressions or values needed multiple times.
*   **Definition:** Defined using the `<xsl:variable>` element.
*   **Syntax:**
    ```xml
    <!-- Assign value using select attribute -->
    <xsl:variable name="VariableName" select="XPathExpression"/>
    
    <!-- Assign value using content (Result Tree Fragment) -->
    <xsl:variable name="VariableName">
      <!-- Content (literal elements, XSLT instructions) goes here -->
    </xsl:variable>
    ```
*   **`name` attribute:** Specifies the name of the variable.
*   **`select` attribute:** An XPath expression whose result is assigned to the variable.
*   **Content:** If `select` is not used, the content within the `<xsl:variable>` tags is instantiated, and the resulting fragment is assigned to the variable.
*   **Usage:** Reference the variable's value in XPath expressions using `$VariableName`.
*   **Scope:** Variables are typically scoped to the template or block (like `xsl:for-each`) where they are defined. Top-level variables are global.
*   **Immutability (XSLT 1.0):** In XSLT 1.0, variables are single-assignment – once set, their value cannot be changed. XSLT 2.0+ introduces `<xsl:sequence>` and other ways to handle sequences more flexibly.

**Example (Slide 25):**

```xml
<!-- definition de variable -->
<!-- Stores the value of the @no attribute of the first 'artiste' node -->
<xsl:variable name="refART" select="artiste/@no"/> 

<!-- utilisation de variable -->
<!-- Uses the variable in a predicate -->
<xsl:value-of select="/album[@ref-artiste=$refART]/chansons/chanson"/> 
```

### La fonction `for-each`

#tags: #XSLT #xsl_for_each #iteration #looping #select_attribute #context_change

*   **Purpose:** Iterates over a node-set selected by an XPath expression. The content of the `<xsl:for-each>` element is instantiated once for *each node* in the selected set.
*   **Syntax:** `<xsl:for-each select="XPathExpression"> ... </xsl:for-each>`
*   **`select` attribute:** The XPath expression selecting the node-set to iterate over.
*   **Context Change:** Inside the loop, the **context node** changes to the current node being processed from the selected node-set. XPath expressions within the loop are evaluated relative to this changing context node.

**Example (Slide 26-27):** Displaying the name of each artist.

```xml
<!-- Template displaying the name for each artist -->
<body>
  <h2>noms d'artistes :</h2>
  <xsl:for-each select="CD/artiste"> <!-- Select all 'artiste' children of 'CD' -->
     <!-- Inside the loop, context node is the current 'artiste' -->
     <h3><xsl:value-of select="nom"/></h3> <!-- Select 'nom' child of current 'artiste' -->
  </xsl:for-each>
</body>

<!-- Result -->
<body>
  <h2>noms d'artistes :</h2>
  <h3>FIRGANI mohamed Taher</h3>
  <h3>ALHACHEMI GUARRWABI</h3>
  <h3>BENANI Hamdi</h3>
  <h3>IDIR</h3>
</body>
```

### La fonction `if`

#tags: #XSLT #xsl_if #conditional #boolean #test_attribute #XPath

*   **Purpose:** Provides simple conditional processing. The content of `<xsl:if>` is instantiated **only if** a boolean test evaluates to true.
*   **Syntax:** `<xsl:if test="BooleanXPathExpression"> ... </xsl:if>`
*   **`test` attribute:** An XPath expression that evaluates to a boolean (`true` or `false`).
*   **No `else`:** `<xsl:if>` does **not** have an `else` or `otherwise` branch. For multiple alternatives, use `<xsl:choose>`.

**Example (Slide 28):** Output " encore " except for the last item.

```xml
<!-- Assume iterating with for-each or apply-templates -->
<xsl:template match="item">
  <xsl:value-of select="."/>
  <!-- If the current item is NOT the last one in its context set -->
  <xsl:if test="not(position()=last())"> 
     <xsl:text> encore </xsl:text> <!-- Output the text " encore " -->
  </xsl:if>
</xsl:template>
```

### L'élément `xsl:choose`

#tags: #XSLT #xsl_choose #xsl_when #xsl_otherwise #conditional #multiple_choice #if_else

*   **Purpose:** Provides multi-way conditional branching (like `if-elseif-else` or `switch`).
*   **Structure:**
    *   Contains one or more `<xsl:when>` elements, each with a boolean `test` attribute.
    *   Optionally contains **one** `<xsl:otherwise>` element at the end.
*   **Behavior:** The processor evaluates the `test` expressions on the `<xsl:when>` elements sequentially. The content of the **first** `<xsl:when>` whose test evaluates to true is instantiated. If no `<xsl:when>` tests are true, the content of the `<xsl:otherwise>` element (if present) is instantiated.
*   **Syntax:**
    ```xml
    <xsl:choose>
      <xsl:when test="BooleanXPathExpression1">
        <!-- Content for first condition -->
      </xsl:when>
      <xsl:when test="BooleanXPathExpression2">
        <!-- Content for second condition -->
      </xsl:when>
      ...
      <xsl:otherwise>
        <!-- Content if no 'when' condition is true -->
      </xsl:otherwise>
    </xsl:choose>
    ```

**Example (Slide 30):** Output 'bonjour' if name starts with 'F', otherwise 'au revoir'.

```xml
<!-- Inside a template matching 'artiste' -->
<xsl:choose>
  <xsl:when test="starts-with(nom, 'F')"> 
     <!-- Assuming bonjour is literal text to output -->
     <xsl:text>bonjour </xsl:text> 
     <xsl:value-of select="nom"/> 
  </xsl:when>
  <xsl:otherwise>
     <xsl:text>au revoir</xsl:text> 
  </xsl:otherwise>
</xsl:choose>

<!-- Example Result for FIRGANI -->
bonjour FIRGANI mohamed Taher 
```
*(Note: The example seems to mix outputting "bonjour" text with the value. Assuming it means prepend "bonjour". Corrected example)*

```xml
<!-- If processing the artist "FIRGANI mohamed Taher" -->
<xsl:choose>
  <xsl:when test="starts-with(nom, 'F')">
    bonjour <xsl:value-of select="nom"/>
  </xsl:when>
  <xsl:otherwise>
    au revoir
  </xsl:otherwise>
</xsl:choose> 
<!-- Output: bonjour FIRGANI mohamed Taher -->
```

### Tris des noeuds sélectionnés (`<xsl:sort>`)

#tags: #XSLT #xsl_sort #sorting #ordering #xsl_apply_templates #xsl_for_each #select_attribute #order_attribute

*   **Purpose:** Specifies the order in which nodes selected by `<xsl:apply-templates>` or `<xsl:for-each>` should be processed.
*   **Placement:** `<xsl:sort>` must appear as the **first child element(s)** inside `<xsl:apply-templates>` or `<xsl:for-each>`.
*   **Syntax:** `<xsl:sort select="XPathExpression" order="ascending|descending" data-type="text|number" ... />`
*   **Key Attributes:**
    *   `select`: An XPath expression evaluated relative to each node in the set being sorted. The string value of this expression determines the sort key for that node (Default: `.`, sorts by node's string value).
    *   `order`: `"ascending"` (Default) or `"descending"`.
    *   `data-type`: `"text"` (Default) or `"number"`. Specifies whether to perform alphabetic or numeric comparison. Other values like `qname` exist.
*   **Multiple Keys:** Multiple `<xsl:sort>` elements can be used for multi-level sorting (primary key, secondary key, etc.).

**Example (Slide 32):** Apply templates to artists, sorted by name descending.

```xml
<!-- Inside a template -->
<body>
  <xsl:apply-templates select="CD/artiste">
    <!-- Sort artists by the value of their 'nom' child, descending order -->
    <xsl:sort select="nom" order="descending" data-type="text"/> 
  </xsl:apply-templates>
</body>

<!-- Result (assuming the template for 'artiste' outputs the name) -->
<body>
  IDIR <!-- Assuming text sort, 'I' comes after 'F' -->
  FIRGANI mohamed Taher
  BENANI Hamdi
  ALHACHEMI GUARRWABI 
</body> 
```
*(Note: The result in the slide shows IDIR first, suggesting descending text sort is correct).*

### Template avec nom et `call-template` (Named Templates)

#tags: #XSLT #xsl_template #name_attribute #xsl_call_template #named_template #function_call #reusability #xsl_param #xsl_with_param

*   **Named Templates:** Templates can be given a name using the `name` attribute, allowing them to be invoked explicitly, similar to calling a function.
    *   `<xsl:template name="MyTemplateName"> ... </xsl:template>`
*   **Calling Named Templates:** Use `<xsl:call-template name="MyTemplateName"/>`.
*   **Purpose:** Useful for:
    *   Reusing a specific block of transformation logic multiple times from different places.
    *   Breaking down complex templates into smaller, manageable units.
    *   Processing that isn't directly tied to matching a node in the source tree.
*   **Parameters:** Named templates can accept parameters.
    *   **Define Parameter:** Use `<xsl:param name="ParamName"/>` inside the `<xsl:template>`.
    *   **Pass Parameter:** Use `<xsl:with-param name="ParamName" select="ValueExpression"/>` inside `<xsl:call-template>`.
    ```xml
    <xsl:template name="example1">
      <xsl:param name="code"/> <!-- Define parameter 'code' -->
      <xsl:value-of select="//artiste[@no=$code]/nom"/> 
    </xsl:template>
    
    <xsl:template match="/"> <!-- Example call -->
       <xsl:call-template name="example1">
         <xsl:with-param name="code" select="'a01'"/> <!-- Pass value 'a01' -->
       </xsl:call-template>
    </xsl:template>
    ```

### Différence entre `apply-templates` et `call-template` : Exemple (Difference between `apply-templates` and `call-template`)

#tags: #XSLT #xsl_apply_templates #xsl_call_template #comparison #context_change #recursion #function_call

*   **`<xsl:apply-templates>`:**
    *   **Data-driven:** Processing depends on the nodes selected from the source XML.
    *   **Context Change:** The context node changes for each node being processed in the selected set.
    *   **Template Matching:** The processor finds the *best matching* template (`<xsl:template match="...">`) for each selected node.
    *   **Implicit Recursion:** Drives the recursive traversal of the source tree.
*   **`<xsl:call-template>`:**
    *   **Control-driven:** Invokes a *specific*, named template (`<xsl:template name="...">`).
    *   **No Context Change:** The context node does *not* change when calling the named template (unless explicitly changed within the called template).
    *   **Explicit Invocation:** Bypasses the template matching process.
    *   **No Implicit Recursion:** Does not automatically process children or other nodes.

**Example (Slide 35-36):**

```xml
<xsl:template match="/">
  <!-- Approach 1: Using apply-templates (data-driven) -->
  mon Album par match Template est : <xsl:apply-templates select="CD/artiste"/>
  <hr/>
  <!-- Approach 2: Calling a named template (control-driven) -->
  mon Album par nom tempalte est : <xsl:call-template name="MyTem"/> 
</xsl:template>

<!-- Template matched by apply-templates -->
<xsl:template match="artiste">
  <h1 color="#FF0000"><xsl:value-of select="nom"/></h1>
</xsl:template>

<!-- Named template called by call-template -->
<xsl:template name="MyTem">
  <!-- Il faut faire un for each pour afficher tout les nom --> 
  <xsl:for-each select="CD/artiste"> 
    <h1 color="#FF0000"><xsl:value-of select="nom"/></h1>
  </xsl:for-each>
</xsl:template>

<!-- Result (Slide 36) shows both approaches produce the same list of names -->
```
This example highlights that while both can achieve similar results, `apply-templates` relies on matching rules and context changes, whereas `call-template` requires explicit iteration (like `for-each`) if multiple nodes need processing within the called template.

### Les modes (`mode` attribute)

#tags: #XSLT #mode #xsl_template #xsl_apply_templates #conditional_processing #multiple_transforms

*   **Purpose:** Modes allow an element from the source XML to be processed multiple times in different ways, using different sets of template rules.
*   **Mechanism:**
    *   A template rule can be assigned to a specific mode using the `mode` attribute: `<xsl:template match="element" mode="ModeName"> ... </xsl:template>`
    *   When invoking processing, `<xsl:apply-templates>` can specify which mode to use via its `mode` attribute: `<xsl:apply-templates select="element" mode="ModeName"/>`
*   **Behavior:** When `<xsl:apply-templates>` specifies a mode, the processor *only* considers template rules (`<xsl:template>`) that either:
    1.  Have a matching `mode` attribute value.
    2.  Have *no* `mode` attribute (these apply to the default, unnamed mode).
*   **Use Case:** Useful when you need to generate different representations of the same source element (e.g., an entry in a table of contents vs. the full content in the main body).

**Example (Slide 38-39):** Process artists in two modes - "model1" (output name in `<li>`) and "mode2" (output site URL in `<h2>`).

```xml
<xsl:template match="/">
  <body>
    <h1>Mes artistes</h1>
    <ul>
      <!-- Apply templates to artists using mode "model1" -->
      <xsl:apply-templates select="CD/artiste" mode="model1"/> 
    </ul>
    <!-- Apply templates to artists using mode "mode2" -->
    <xsl:apply-templates select="CD/artiste" mode="mode2"/> 
  </body>
</xsl:template>

<!-- Template for 'artiste' in mode "model1" -->
<xsl:template match="artiste" mode="model1"> 
  <li><xsl:value-of select="nom"/></li> 
</xsl:template>

<!-- Template for 'artiste' in mode "mode2" -->
<xsl:template match="artiste" mode="mode2"> 
  <h2><xsl:value-of select="site/@url"/></h2> 
</xsl:template>

<!-- Result (Slide 39) -->
<body>
  <h1>Mes artistes</h1>
  <ul>
    <li>FIRGANI mohamed Taher</li>
    <li>ALHACHEMI GUARRWABI</li>
    <li>BENANI Hamdi</li>
    <li>IDIR</li>
  </ul>
  <h2>http://www.Mohamedfergani.dz</h2>
  <h2>http://www.AlhachemiGUATWABI.dz</h2>
  <h2>http://www.Bennani Hamedi.dz</h2>
  <h2>http://www.IDIR.dz</h2>
</body>
```

---

## 6. Priorité de règles (Rule Priority)

#tags: #XSLT #template_priority #conflict_resolution #default_rules #priority_attribute #specificity

*   **Problem:** Sometimes, more than one template rule (`<xsl:template match="...">`) might match the same node during processing initiated by `<xsl:apply-templates>`. How does the XSLT processor decide which one to use?
*   **Solution:** Conflict resolution is based on **priority**.

**Default Built-in Template Rules:**
XSLT processors have built-in, low-priority template rules that apply if no explicit rule matches:
1.  **Elements and Root (`match="*|/"`)**: Recursively applies templates to children.
    ```xml
    <xsl:template match="*|/">
      <xsl:apply-templates/>
    </xsl:template>
    ```
    *Effect:* Traverses the tree, ignoring element tags themselves but processing children.
2.  **Text and Attributes (`match="text()|@*"`)**: Copies the text value to the output.
    ```xml
    <xsl:template match="text()|@*">
      <xsl:value-of select="."/>
    </xsl:template>
    ```
    *Effect:* Outputs text content and attribute values when encountered.
3.  **Comments and PIs (`match="processing-instruction()|comment()"`)**: Does nothing (ignores them).
    ```xml
    <xsl:template match="processing-instruction()|comment()"/>
    ```

**Conflict Resolution Rules:**
When multiple *explicit* templates match a node:
1.  **Import Precedence:** Rules imported later override rules imported earlier (using `<xsl:import>`).
2.  **Explicit Priority (`priority` attribute):** A template can be assigned a numeric priority: `<xsl:template match="..." priority="N">`. Higher numbers have higher priority. This manually overrides default priorities.
3.  **Default Priority (Specificity):** If no explicit `priority` is given, the processor calculates a default priority based on the specificity of the `match` pattern. More specific patterns generally have higher priority. Examples (higher priority first):
    *   `element[@attr='value']` (more specific than below)
    *   `element`
    *   `prefix:*`
    *   `*` (least specific element match)
    *   Patterns involving specific node types (`text()`, `comment()`) or axes other than `child`/`attribute` also have specific default priorities (often lower than named element matches).

**Example (Slide 43 & 45):**

```xml
<!-- Default rule match="*" would apply templates, eventually outputting text via match="text()" -->

<!-- Explicit rule for root - higher priority than default *|/ -->
<xsl:template match="/">
   <html>... <xsl:apply-templates/> ... </html>
</xsl:template>

<!-- Explicit rule for 'nom' - higher priority than default * -->
<!-- This template has higher default priority than the one below -->
<xsl:template match="nom"> 
  <h1>bonjour Mr. <xsl:value-of select="."/></h1>
</xsl:template>

<!-- If we add priorities: -->
<xsl:template match="nom" priority="1"> 
  <h1>bonjour Mr. <xsl:value-of select="."/></h1>
</xsl:template>

<xsl:template match="nom" priority="2"> 
  <h1>bonsoir Mr. <xsl:value-of select="."/></h1>
</xsl:template>
<!-- The template with priority="2" will always be chosen for 'nom' nodes --> 
```

*   **Why is text displayed in Slide 46?** Even with explicit templates for `/` and potentially `artiste`, the default rule `match="*|/"` eventually calls `apply-templates` on nodes not explicitly matched (like `biographie`, `site`). The default rule `match="text()|@*"` then copies the text content of these nodes to the output.

---

## 7. Référencer un document XSLT (Referencing an XSLT Document)

#tags: #XSLT #linking #xml_stylesheet #processing_instruction #PI #XML #browser #processor

To associate an XSLT stylesheet with an XML document so that a processor (like a browser or standalone tool) knows which transformation to apply, use the **`<?xml-stylesheet ... ?>` processing instruction** within the XML document's prolog (after the XML declaration).

*   **Syntax:**
    ```xml
    <?xml-stylesheet type="text/xsl" href="URI_to_Stylesheet.xsl"?>
    ```
*   **`type="text/xsl"`:** Specifies the MIME type of the stylesheet, indicating it's XSLT.
*   **`href="URI_to_Stylesheet.xsl"`:** Provides the path or URL to the XSLT file.

**Example (Slide 48):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="artiste.xsl"?> <!-- Link to the XSLT -->
<CD nom="MON CD">
  <!-- Corp du document --> 
  ...
</CD>
```

When a browser loads this XML file, it sees the processing instruction and attempts to fetch `artiste.xsl` and apply the transformation before rendering the result (which is often HTML). Standalone XSLT processors also use this information, or allow specifying input XML and XSL files via command line arguments.