

#tags: #semistructured_data #XML #XML_Schema #XSD #course_notes

---


### Problèmes de DTD => schéma XML (Problems with DTD leading to XML Schema)

#tags: #DTD #XML_Schema #limitation #data_types #namespaces #XML_syntax #validation

DTDs have several limitations that XML Schema was designed to overcome:

1.  **Syntax:** DTDs **do not use XML syntax**. They have their own unique declaration syntax (`<!ELEMENT ...>`, `<!ATTLIST ...>`), requiring different parsers/tools than those used for XML documents themselves. XML Schemas *are* written in XML.
2.  **Data Typing:** DTDs offer very **limited data typing**. Primarily, they distinguish between basic text (`CDATA`), IDs (`ID`, `IDREF`), name tokens (`NMTOKEN`), and enumerations. They cannot specify types like integer, decimal, date, boolean, or apply detailed constraints (facets) to text like patterns or length limits. XML Schema provides a rich set of built-in data types and allows creating complex user-defined types.
3.  **Namespace Support:** DTDs **do not inherently support XML Namespaces**. While workarounds exist (declaring prefixed names literally, using `#FIXED` attributes for `xmlns`), it's awkward and doesn't fully integrate namespace validation. XML Schema is fully namespace-aware.

**Solution:** **Schémas XML (XML Schemas / XSD)** were developed by the W3C to address these issues, providing a more powerful, flexible, and XML-based way to define the structure and content rules for XML documents.

### Définition: Schéma XML (XML Schema)

#tags: #XML_Schema #XSD #W3C #validation #document_model #schema_language

*   **XML Schema (XSD - XML Schema Definition):** XML Schemas are XML documents themselves that define the structure, content, data types, and constraints for a class of other XML documents (called instance documents).
*   **Purpose:** Like DTDs, they allow defining document models and validating instance documents against those models.
*   **Advantages over DTD:** XML syntax, rich data typing, namespace awareness, more powerful content models and constraints, extensibility.

### Exemple Introductif (Introductory Example)

This example illustrates the same simple bibliography data represented in:
1.  XML (Instance Document)
2.  DTD (Document Type Definition)
3.  XSD (XML Schema Definition)

#tags: #XSD_example #DTD_example #XML_example #schema_comparison #validation

**Figure - Document XML (`biblio.xml`)**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<bibio>
  <livre reference="02"> 
    <titre>Données semi Structurées</titre>
    <auteur>Ba</auteur> 
  </livre>
</bibio>
```

**Figure - DTD (`biblio.dtd`)**
```dtd
<!ELEMENT bibio (livre)>
<!ELEMENT livre (titre, auteur)>
<!ATTLIST livre 
    reference CDATA #REQUIRED>
<!ELEMENT titre (#PCDATA)>
<!ELEMENT auteur (#PCDATA)>
```

**Figure - XMLSchema (`biblio.xsd`)**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" 
           elementFormDefault="qualified"> 
  
  <!-- Global element declaration for 'bibio' -->
  <xs:element name="bibio">
    <xs:complexType>
      <xs:sequence>
        <!-- Reference to the global 'livre' element -->
        <xs:element ref="livre"/> 
      </xs:sequence>
    </xs:complexType>
  </xs:element>

  <!-- Global element declaration for 'livre' -->
  <xs:element name="livre">
    <xs:complexType>
      <xs:sequence>
         <!-- Reference to the global 'titre' element -->
        <xs:element ref="titre"/>
         <!-- Reference to the global 'auteur' element -->
        <xs:element ref="auteur"/> 
      </xs:sequence>
      <!-- Attribute declaration for 'reference' -->
      <xs:attribute name="reference" use="required" type="xs:integer"/> 
    </xs:complexType>
  </xs:element>

  <!-- Global element declaration for 'titre' with simple type xs:string -->
  <xs:element name="titre" type="xs:string"/> 
  <!-- Global element declaration for 'auteur' with simple type xs:NCName -->
  <xs:element name="auteur" type="xs:NCName"/> 

</xs:schema>
```
*   **(Visual Labels):** Prologue, Racine (Root), Élément complexe (Complex Element), Attribut (Attribute), Élément simple (Simple Element).
*   **Key Observations:**
    *   The XSD is written in XML, using elements like `<xs:schema>`, `<xs:element>`, `<xs:attribute>`, `<xs:complexType>`, `<xs:sequence>`.
    *   It uses the `xs:` prefix bound to the official XML Schema namespace.
    *   It explicitly defines data types (e.g., `xs:string`, `xs:integer`, `xs:NCName`).
    *   It declares elements and attributes globally and references them (`ref="..."`).

---

## Élément Racine (Root Element)

### Schéma XML : les bases (XML Schema: The Basics)

#tags: #XSD #root_element #xs_schema #XML_Schema_namespace #prologue

*   **Structure:** An XML Schema document is an XML document itself.
*   **Prologue:** Usually starts with the standard XML declaration `<?xml version="1.0" encoding="UTF-8"?>`.
*   **Root Element:** The root element of *every* XML Schema document **must** be `<schema>`, belonging to the XML Schema namespace.
*   **Namespace:** The conventional prefix for the XML Schema namespace (`http://www.w3.org/2001/XMLSchema`) is `xs` (or sometimes `xsd`). This prefix must be declared (e.g., `xmlns:xs="http://www.w3.org/2001/XMLSchema"`).
*   **Content:** Inside the `<xs:schema>` element, you declare global elements, attributes, types (simple and complex), groups, etc., that define the vocabulary for the instance documents.

```xml
<?xml version="1.0"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"> 

  <!-- Schema declarations for elements, attributes, and types go here -->
  
</xs:schema>
```

*   **Alternative Root:** You might sometimes see `<schema>` without a prefix if the XML Schema namespace is declared as the *default* namespace (`xmlns="http://www.w3.org/2001/XMLSchema"`). Both `<xs:schema>` and `<schema>` (with default ns declaration) are valid root elements.

### Example Schema Structure

#tags: #XSD_example #xs_schema #targetNamespace #elementFormDefault #complexType #sequence

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- Schema simple de message -->
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           targetNamespace="https://www.monnamespace.com" <!-- 1. Declares the namespace this schema DEFINES -->
           xmlns="https://www.monnamespace.com"         <!-- 2. Sets default ns for THIS schema (optional, can use prefix) -->
           elementFormDefault="qualified">            <!-- 3. Elements defined here MUST be namespace-qualified in instance docs -->

    <!-- Defines a global element 'message' -->
    <xs:element name="message">
      <xs:complexType> <!-- Defines the structure of 'message' -->
        <xs:sequence>  <!-- Specifies child elements must appear in sequence -->
          <!-- Defines local elements 'to' and 'from' of type string -->
          <xs:element name="to" type="xs:string"/>
          <xs:element name="from" type="xs:string"/>
        </xs:sequence>
      </xs:complexType>
    </xs:element>

</xs:schema>
```

### Espaces de noms (namespaces) et préfixes (Namespaces and Prefixes)

#tags: #XSD #namespaces #targetNamespace #elementFormDefault #qualified #unqualified #schema_namespace #instance_namespace

*   **Purpose:** Namespaces distinguish elements belonging to the schema definition itself (XSD elements like `<xs:element>`) from the elements and attributes being *defined* by the schema for the instance documents.
*   **Key Attributes on `<xs:schema>` for Namespaces:**
    *   `xmlns:xs="http://www.w3.org/2001/XMLSchema"`: Declares the prefix (`xs`) for the XML Schema language itself. (Essential).
    *   `targetNamespace="URI"`: Specifies the namespace that the elements and attributes defined *within this schema* will belong to. This is the namespace users will typically declare in their instance documents.
    *   `elementFormDefault="qualified|unqualified"`:
        *   `"qualified"` (Recommended): **Locally** declared elements within the schema **must** be explicitly qualified with the `targetNamespace` (either via prefix or default namespace) in the *instance document*. Global elements are always qualified.
        *   `"unqualified"` (Default): Locally declared elements in the schema belong to "no namespace" in the instance document, unless explicitly qualified there.
    *   `attributeFormDefault="qualified|unqualified"`: Same as `elementFormDefault`, but applies to locally declared attributes. (Default is `unqualified`).

**Defining a Namespace for the Schema:**

How do we associate the elements *defined* by the schema (like `<message>`, `<to>`, `<from>` in the previous example) with the `targetNamespace` in the instance document?

*   **Solution 1: Using `elementFormDefault="qualified"` in the Schema:**
    *   As shown in the example (`elementFormDefault="qualified"`).
    *   This forces *all* elements defined in the schema (both global and local) to belong to the `targetNamespace` in the instance document. The instance document must then use either a prefix or a default namespace declaration for the `targetNamespace`.
    *   **Example Schema:**
        ```xml
        <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
                   targetNamespace="https://www.monnamespace.com" 
                   elementFormDefault="qualified">
          <xs:element name="message">
            <xs:complexType>
              <xs:sequence>
                <xs:element name="to" type="xs:string"/>
                <xs:element name="from" type="xs:string"/>
              </xs:sequence>
            </xs:complexType>
          </xs:element>
        </xs:schema> 
        ```
    *   **Example Instance XML:**
        ```xml
        <msg:message xmlns:msg="https://www.monnamespace.com"> 
          <msg:to>Recipient</msg:to>
          <msg:from>Sender</msg:from>
        </msg:message>
        <!-- OR using default namespace -->
        <message xmlns="https://www.monnamespace.com">
          <to>Recipient</to>
          <from>Sender</from>
        </message>
        ```

*   **Solution 2: Defining a Prefix for User Elements in the Schema (Less Common):**
    *   Declare a prefix for the `targetNamespace` *within the schema itself* and use it for element/type references *within the schema*.
    *   This primarily affects how elements/types are referenced *inside the schema*, not qualification in the instance document (which is still controlled by `elementFormDefault`).
    *   The `targetNamespace` attribute *still* defines the namespace for the components.
    *   **Example Schema:**
        ```xml
        <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
                   targetNamespace="https://www.monnamespace.com" 
                   xmlns:monN="https://www.monnamespace.com"> <!-- Declare prefix for target -->
            
          <xs:element name="message"> <!-- Still defines <monN:message> -->
             <xs:complexType>
               <xs:sequence>
                 <xs:element name="to" type="xs:string"/> <!-- Defines <monN:to> -->
                 <xs:element name="from" type="xs:string"/> <!-- Defines <monN:from> -->
               </xs:sequence>
             </xs:complexType>
           </xs:element>
        </xs:schema>
        ```
     *   **Example Instance XML (assuming elementFormDefault="qualified"):**



```xml
        <monN:message xmlns:monN="https://www.monnamespace.com">
          <monN:to>Recipient</monN:to>
          <monN:from>Sender</monN:from>
        </monN:message>
```


### Validation (liaison du fichier XML avec le fichier XSD) (Validation: Linking XML to XSD)

#tags: #XSD #validation #XML_instance #xsi #schemaLocation #noNamespaceSchemaLocation #XML_Schema_Instance

To validate an XML document (instance document) against an XSD schema, the processor needs to know which schema(s) to use. This link is typically established *within the XML instance document* using attributes from the **XML Schema Instance** namespace (`http://www.w3.org/2001/XMLSchema-instance`), conventionally prefixed with `xsi`.

1.  **Declare the `xsi` namespace:** Add `xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"` to an element in the XML (usually the root).
2.  **Associate namespaces with schema locations:**
    *   **`xsi:schemaLocation`:** Used when the instance document uses elements from one or more **target namespaces** defined by schemas.
        *   **Syntax:** `xsi:schemaLocation="namespaceURI1 schemaURI1 namespaceURI2 schemaURI2 ..."`
        *   **Value:** A space-separated list of pairs. Each pair consists of a namespace URI followed by the URI (URL or file path) of the XSD file that defines that namespace.
    *   **`xsi:noNamespaceSchemaLocation`:** Used when the instance document's elements are **not** in any target namespace (i.e., the schema defines elements without a `targetNamespace`).
        *   **Syntax:** `xsi:noNamespaceSchemaLocation="schemaURI"`
        *   **Value:** The URI (URL or file path) of the XSD file.

**Example 1: Using `xsi:noNamespaceSchemaLocation`**

*   Assumes `charge.xsd` defines elements *without* a `targetNamespace`.
*   The instance document `charge.xml` does *not* use prefixes or default namespace declarations for its elements (except `xsi`).

**`charge.xml`:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<charge xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="charge.xsd"> <!-- Points to the schema -->
  <cours>
    <designation>Web sémantique</designation>
    <auteur id="ba">Boustil Amel</auteur>
    <Specialite>Systèmes d'information</Specialite>
  </cours>
  <cours>
    <designation>Theorie des langages</designation>
    <auteur id="ba">Boustil Amel</auteur> <!-- Note: ID 'ba' repeated, XSD could flag this if type="xs:ID" -->
    <Specialite>Licence Informatique</Specialite>
  </cours>
   <cours>
    <designation>Données sémie structurées</designation>
    <auteur id="ma">mohamed Ali</auteur>
    <Specialite>ISIL</Specialite>
  </cours>
</charge>
```

**`charge.xsd` (Partial, corresponding to no namespace):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"> <!-- NO targetNamespace -->
  
  <xs:element name="charge">
    <xs:complexType>
      <xs:sequence>
        <xs:element ref="cours" maxOccurs="unbounded"/> 
      </xs:sequence>
    </xs:complexType>
  </xs:element>

  <xs:element name="cours">
     <xs:complexType>
       <xs:sequence>
         <xs:element ref="designation"/>
         <xs:element ref="auteur"/>
         <xs:element ref="Specialite"/>
       </xs:sequence>
       <!-- Potential attribute declaration -->
       <!-- <xs:attribute name="id" type="xs:ID"/> --> 
     </xs:complexType>
   </xs:element>
   
  <xs:element name="designation" type="xs:string"/>
  <xs:element name="auteur" > <!-- Assuming complex type for attribute -->
      <xs:complexType>
          <xs:simpleContent>
              <xs:extension base="xs:string">
                  <xs:attribute name="id" type="xs:string"/> <!-- Example: changed type to string to allow reuse -->
              </xs:extension>
          </xs:simpleContent>
      </xs:complexType>
  </xs:element>
  <xs:element name="Specialite" type="xs:string"/>
  
</xs:schema>
```
*(Note: The schema structure shown on slide 18 implicitly assumes `elementFormDefault="qualified"` and `ref` attributes, which are more typical when using `targetNamespace`. A schema matching `noNamespaceSchemaLocation` might define elements locally or globally without refs if simple enough)*

**Example 2: Using `xsi:schemaLocation`**

*   Assumes `charge2.xsd` defines elements within the target namespace `http://mynamespace.org/`.
*   The instance document `charge2.xml` uses this namespace as the default.

**`charge2.xml`:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<charge xmlns="http://mynamespace.org/" <!-- Default namespace for elements -->
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://mynamespace.org/ charge2.xsd"> <!-- Pair: Namespace URI + Schema Location -->
  <cours>
    <designation>Web sémantique</designation>
    <auteur id="ba">Boustil Amel</auteur>
    <Specialite>Systèmes d'information</Specialite>
  </cours>
  <cours>
    <designation>Theorie des langages</designation>
    <auteur id="ba">Boustil Amel</auteur>
    <Specialite>Licence Informatique</Specialite>
  </cours>
  <cours>
    <designation>Données sémie structurées</designation>
    <auteur id="ma">mohamed Ali</auteur>
    <Specialite>ISIL</Specialite>
  </cours>
</charge>
```

**`charge2.xsd`:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           targetNamespace="http://mynamespace.org/" <!-- Defines this namespace -->
           xmlns="http://mynamespace.org/"         <!-- Sets default for this schema -->
           elementFormDefault="qualified">        <!-- Ensures local elements need qualification -->

  <xs:element name="charge">
    <xs:complexType>
      <xs:sequence>
        <xs:element ref="cours" maxOccurs="unbounded"/> 
      </xs:sequence>
    </xs:complexType>
  </xs:element>

  <xs:element name="cours">
     <xs:complexType>
       <xs:sequence>
         <xs:element ref="designation"/>
         <xs:element ref="auteur"/>
         <xs:element ref="Specialite"/>
       </xs:sequence>
       <!-- Add attribute declaration if needed -->
     </xs:complexType>
   </xs:element>
   
  <xs:element name="designation" type="xs:string"/>
  <xs:element name="auteur" type="xs:string"/> <!-- Simplified for example -->
  <xs:element name="Specialite" type="xs:string"/>
  
</xs:schema>
```

---

## Structure de base (Basic Structure)

### Type de données (Data Types)

#tags: #XSD #data_types #simple_type #complex_type #xs_simpleType #xs_complexType #type_hierarchy

XML Schema distinguishes two main categories of types:

1.  **Types simples (Simple Types):** Introduced by the `<xs:simpleType>` element.
    *   Cannot contain child elements.
    *   Cannot have attributes.
    *   Define constraints on the textual content of elements or attributes (e.g., string, integer, date, patterns, enumerations).
2.  **Types complexes (Complex Types):** Introduced by the `<xs:complexType>` element.
    *   Can contain child elements.
    *   Can have attributes.
    *   Can have simple text content *or* mixed content (text + elements).
    *   Can be empty (contain neither elements nor text, only attributes).

**Type Hierarchy Diagram (Slide 22):**
This diagram shows the relationship between built-in types in XSD.
*   **Top:** `xs:anyType` (The base type from which all simple and complex types derive).
*   **Branches:** Splits into `xs:anySimpleType` and the base for complex types.
*   **`xs:anySimpleType`:** Base for all simple types.
    *   **Atomic Types (`xs:anyAtomicType`):** Built-in primitive types like `xs:string`, `xs:decimal`, `xs:boolean`, `xs:date`, `xs:QName`, etc., and types derived from them (e.g., `xs:integer` derived from `xs:decimal`, `xs:token` derived from `xs:normalizedString`).
    *   **List Types (`xs:list`):** Space-separated sequences of atomic values (e.g., a list of integers).
    *   **Union Types (`xs:union`):** Allows a value to conform to one of several specified simple types.
*   **Complex Types:** Defined structure involving elements, attributes.
    *   **Content Models:** `xs:sequence` (ordered), `xs:choice` (select one), `xs:all` (unordered, maxOccurs=1).
    *   **Derivation:** `xs:extension` (add elements/attributes), `xs:restriction` (constrain content/attributes).

*(Note: The diagram also visually distinguishes primitive types, derived types, and derivation methods like restriction, list, and union for simple types.)*

### Déclaration d’éléments (Element Declaration)

#tags: #XSD #xs_element #element_declaration #data_types #simple_type #complex_type #default_value #fixed_value

*   **Syntax:** Elements are declared in a schema using the `<xs:element>` tag.
    ```xml
    <xs:element name="ElementName" type="DataTypeName" 
                default="DefaultValue" fixed="FixedValue"
                minOccurs="N" maxOccurs="M|unbounded"
                ref="GlobalElementName"
                ... /> 
    <!-- OR with inline type definition -->
    <xs:element name="ElementName">
      <xs:simpleType>...</xs:simpleType> 
      <!-- OR -->
      <xs:complexType>...</xs:complexType>
    </xs:element>
    ```
*   **Key Attributes:**
    *   `name`: The name of the element being defined.
    *   `type`: Specifies the data type of the element's content (e.g., `xs:string`, `xs:integer`, or a user-defined simple/complex type name). Either `type` or an inline type definition must be present.
    *   `default`: Provides a default value if the element is present but empty in the instance document.
    *   `fixed`: Specifies a fixed value. If the element is present, it *must* have this value. If present but empty, it takes this value.
    *   `minOccurs`, `maxOccurs`: Control how many times the element can appear (see Complex Types section). Default is `1`.
    *   `ref`: References a globally declared element (used for modularity, discussed later).

**Example:**
```xml
<xs:schema ...>
  <!-- Element 'Nom' must contain a string -->
  <xs:element name="Nom" type="xs:string"/> 
  
  <!-- Element 'adresse' uses a user-defined complex type 'typeAdresse' -->
  <xs:element name="adresse" type="typeAdresse"/> 

  <!-- Element 'color' is a string, defaults to "red" if empty -->
  <xs:element name="color" type="xs:string" default="red"/> 
  
  <!-- Element 'version' must be "1.0" if present -->
  <xs:element name="version" type="xs:string" fixed="1.0"/> 
</xs:schema>
```
**Remarque:** In the example `<xs:element name="Nom" type="xs:string"/>`, `xs:string` is a built-in simple type. In `<xs:element name="adresse" type="typeAdresse"/>`, `typeAdresse` is assumed to be a user-defined complex type defined elsewhere in the schema.

### Déclaration d’attributs (Attribute Declaration)

#tags: #XSD #xs_attribute #attribute_declaration #simple_type #default_value #fixed_value #required #optional

*   **Declaration:** Attributes are declared using the `<xs:attribute>` tag, typically within the `<xs:complexType>` definition of the element they belong to (or within an `<xs:attributeGroup>`).
*   **Type:** Attribute values **must** be described by **simple types** (built-in or user-derived). Attributes cannot contain elements.
*   **Syntax:**
    ```xml
    <xs:attribute name="AttributeName" type="SimpleTypeName"
                  default="DefaultValue" fixed="FixedValue"
                  use="optional|required" 
                  ref="GlobalAttributeName"
                  ... />
    <!-- OR with inline simple type definition -->
    <xs:attribute name="AttributeName">
      <xs:simpleType>...</xs:simpleType>
    </xs:attribute>
    ```
*   **Key Attributes:**
    *   `name`: The name of the attribute.
    *   `type`: Specifies the simple data type of the attribute's value (e.g., `xs:string`, `xs:integer`, `xs:boolean`).
    *   `default`: Provides a default value if the attribute is *not present* in the instance document.
    *   `fixed`: Specifies a fixed value. If the attribute is present, it *must* have this value. If omitted, it takes this value.
    *   `use`: Specifies whether the attribute is optional or required.
        *   `"optional"` (Default): The attribute may or may not be present.
        *   `"required"`: The attribute must be present.
        *   `"prohibited"`: (Used in restrictions) The attribute must NOT be present.
    *   `ref`: References a globally declared attribute.

**Remarques:**

*   Only complex elements (defined with `<xs:complexType>`) can have attributes.
*   Default values (`default`) apply if the attribute is *missing*. Fixed values (`fixed`) apply if missing *or* if present (constraining the value).
*   By default, attributes are optional (`use="optional"`). Use `use="required"` to make them mandatory.
*   Attribute types can be built-in simple types or user-derived simple types.

**Example:**
```xml
<xs:complexType name="ElementType">
  <xs:sequence>...</xs:sequence>
  <!-- Attribute 'lang' defaults to "EN" if omitted -->
  <xs:attribute name="lang" type="xs:string" default="EN"/> 
  
  <!-- Attribute 'version' must be "2.0" if present, or is assumed to be "2.0" if omitted -->
  <xs:attribute name="version" type="xs:decimal" fixed="2.0"/> 

  <!-- Attribute 'status' is optional (default use) -->
  <xs:attribute name="status" type="xs:string" use="optional"/> 

  <!-- Attribute 'id' must be present -->
  <xs:attribute name="id" type="xs:ID" use="required"/> 
</xs:complexType>
```

---

## Type Simple (Simple Types)

#tags: #XSD #simple_type #xs_simpleType #data_types #text_content #attribute_value #derivation #restriction #list #union

*   **Definition:** Simple types define constraints on data that appears as text content in elements (without child elements) or as attribute values.
*   **Constraints:** They cannot have attributes or contain child elements.
*   **Built-in Types:** XSD provides a large set of predefined simple types (e.g., `xs:string`, `xs:integer`, `xs:boolean`, `xs:date`, `xs:time`).
*   **User-Defined Simple Types:** New simple types can be "derived" from existing simple types (either built-in or other user-defined ones) using one of three methods:
    1.  **Restriction:** Constraining the value space of the base type (e.g., limiting a string length, restricting an integer range, defining a pattern). Uses `<xs:restriction>`.
    2.  **List:** Defining a type whose value is a space-separated sequence of values of a base atomic type (e.g., a list of integers). Uses `<xs:list>`.
    3.  **Union:** Defining a type whose value can conform to any one of several specified base simple types. Uses `<xs:union>`.

### Types simples prédéfinis (Built-in Simple Types)

#tags: #XSD #built_in_types #simple_type #data_types #string #integer #decimal #boolean #date #time #QName

*   **Purpose:** XSD provides a rich set of built-in simple types covering common data formats.
*   **Declaration Example:** Elements using built-in simple types.
    ```xml
    <xs:element name="Nom" type="xs:string"/> 
    <xs:element name="age" type="xs:integer"/>
    <xs:element name="dateNaissance" type="xs:date"/>
    ```

*   **Examples of Built-in Types:**
    *   **String-related:** `xs:string`, `xs:normalizedString`, `xs:token`, `xs:NMTOKEN`, `xs:NMTOKENS`, `xs:Name`, `xs:NCName`, `xs:QName`, `xs:language`, etc.
    *   **Numeric:** `xs:decimal`, `xs:integer`, `xs:positiveInteger`, `xs:negativeInteger`, `xs:nonNegativeInteger`, `xs:nonPositiveInteger`, `xs:long`, `xs:int`, `xs:short`, `xs:byte`, `xs:unsignedLong`, `xs:unsignedInt`, `xs:unsignedShort`, `xs:unsignedByte`, `xs:float`, `xs:double`, etc.
    *   **Date/Time:** `xs:date`, `xs:time`, `xs:dateTime`, `xs:duration`, `xs:gYear`, `xs:gYearMonth`, `xs:gMonth`, `xs:gMonthDay`, `xs:gDay`, etc.
    *   **Boolean:** `xs:boolean` (values `true`, `false`, `1`, `0`).
    *   **Binary:** `xs:hexBinary`, `xs:base64Binary`.
    *   **URI:** `xs:anyURI`.
    *   **Other:** `xs:ID`, `xs:IDREF`, `xs:IDREFS`, `xs:ENTITY`, `xs:ENTITIES`, `xs:NOTATION`.

*   **Hierarchy Diagram (Slide 30):** Shows the derivation hierarchy of these built-in types, starting from `xs:anySimpleType`. (See also: `http://dret.net/lectures/xml-fall11/img/xsd-type-hierarchy.gif`)

### Type simple dérivé : restrictions (Derived Simple Type: Restrictions)

#tags: #XSD #simple_type #derivation #restriction #facet #value_constraint #pattern #enumeration #range #length #whitespace

*   **Restrictions (Facets):** Restrictions are used to create new simple types by constraining the "value space" (the set of allowed values) of a base simple type. These constraints are called **facets**.
*   **Purpose:** To define more specific data types tailored to application needs (e.g., a string that must match a specific format, an integer within a certain range).
*   **Syntax:** Uses the `<xs:restriction>` element inside `<xs:simpleType>`, specifying the `base` type being restricted. Facets are defined using specific elements within `<xs:restriction>`.

**Common Restriction Facets:**

1.  **Range Facets (for numeric/date types):**
    *   `<xs:minInclusive value="N"/>`: Minimum value, inclusive (>= N).
    *   `<xs:maxInclusive value="M"/>`: Maximum value, inclusive (<= M).
    *   `<xs:minExclusive value="N"/>`: Minimum value, exclusive (> N).
    *   `<xs:maxExclusive value="M"/>`: Maximum value, exclusive (< M).
    *   **Example (Age between 16 and 120):**
        ```xml
        <xs:element name="age">
          <xs:simpleType>
            <xs:restriction base="xs:integer">
              <xs:minInclusive value="16"/>
              <xs:maxInclusive value="120"/>
            </xs:restriction>
          </xs:simpleType>
        </xs:element>
        ```

2.  **Enumeration Facet (for atomic types):**
    *   `<xs:enumeration value="allowedValue"/>`: Specifies one possible allowed value. Use multiple `xs:enumeration` elements to list all permitted values.
    *   **Example (Car must be Audi, Golf, or BMW):**
        ```xml
        <xs:element name="voiture">
          <xs:simpleType>
            <xs:restriction base="xs:string">
              <xs:enumeration value="Audi"/>
              <xs:enumeration value="Golf"/>
              <xs:enumeration value="BMW"/>
            </xs:restriction>
          </xs:simpleType>
        </xs:element>
        ```

3.  **Pattern Facet (primarily for strings):**
    *   `<xs:pattern value="regularExpression"/>`: Constrains the value to match a specified regular expression pattern.
    *   **Example (Message contains only lowercase letters):**
        ```xml
        <xs:element name="message">
          <xs:simpleType>
            <xs:restriction base="xs:string">
              <!-- Allows zero or more lowercase letters -->
              <xs:pattern value="[a-z]*"/> 
            </xs:restriction>
          </xs:simpleType>
        </xs:element>
        ```
    *   **Example (Choice 'male' or 'female'):**
        ```xml
         <xs:element name="sexe">
           <xs:simpleType>
             <xs:restriction base="xs:string">
               <!-- Matches exactly 'male' OR 'female' -->
               <xs:pattern value="male|female"/> 
             </xs:restriction>
           </xs:simpleType>
         </xs:element>
        ```
        *(Note: Enumeration is often clearer for simple choices like this).*

4.  **Whitespace Facet (for strings):**
    *   `<xs:whiteSpace value="preserve|replace|collapse"/>`: Controls how whitespace characters (spaces, tabs, newlines) are handled.
        *   `preserve`: Keep all whitespace.
        *   `replace`: Replace tabs, newlines, carriage returns with spaces.
        *   `collapse` (Default for `xs:token` and derived types): Replace whitespace characters with spaces, then collapse multiple spaces into one, and trim leading/trailing spaces.
    *   **Example (Preserve all spaces in address):**
        ```xml
        <xs:element name="address">
          <xs:simpleType>
            <xs:restriction base="xs:string">
              <xs:whiteSpace value="preserve"/>
            </xs:restriction>
          </xs:simpleType>
        </xs:element>
        ```

5.  **Length Facets (for strings, hexBinary, base64Binary, lists):**
    *   `<xs:length value="N"/>`: Value must have exactly N characters (or list items).
    *   `<xs:minLength value="N"/>`: Minimum length N.
    *   `<xs:maxLength value="M"/>`: Maximum length M.
    *   **Example (Password between 5 and 8 characters):**
        ```xml
        <xs:element name="password">
          <xs:simpleType>
            <xs:restriction base="xs:string">
              <xs:minLength value="5"/>
              <xs:maxLength value="8"/>
            </xs:restriction>
          </xs:simpleType>
        </xs:element>
        ```
*   **Other Facets:** `totalDigits`, `fractionDigits` (for decimals).

### Type simple encore !! (Simple Types Again!!)

#tags: #XSD #simple_type #derivation #W3C_documentation #data_types

*   **Reminder:** There are many derived simple types built into XSD (like `xs:integer`, `xs:token`, `xs:positiveInteger`).
*   **Further Info:** For the complete list of built-in types, facets, and detailed specifications, consult the official W3C XML Schema Part 2: Datatypes recommendation.
    *   **Link:** `https://www.w3.org/TR/xmlschema11-2/` (or the specific version mentioned, e.g., the older Recommendation).

---

## Type complexe (Complex Types)

### Types ou éléments complexes (Complex Types or Elements)

#tags: #XSD #complex_type #xs_complexType #element_content #attribute #simple_content #mixed_content #empty_element

*   **Rappel (Reminder):** Unlike simple types, complex types **can** contain child elements and/or have attributes. This makes them necessary for defining the structure of most XML elements.
*   **Motivation:** If an element needs to contain other elements or have attributes, it must be defined using a complex type.
*   **Four Main Kinds of Complex Types:** Based on their content:
    1.  **Elements with Element-Only Content:** Contain only child elements, no text nodes directly within the parent (though the children might contain text).
    2.  **Empty Elements:** Contain no child elements and no text content, but may have attributes.
    3.  **Elements with Simple Content:** Contain only text content (like a simple type) but *also* have attributes.
    4.  **Elements with Mixed Content:** Contain a mix of child elements and text content interspersed.

**Examples:**

1.  **Element-Only:**
    ```xml
    <employee>
      <nom>John</nom>
      <prenom>Smith</prenom>
    </employee>
    ```
2.  **Empty:**
    ```xml
    <product pid="1345"/> 
    ```
3.  **Simple Content (Text + Attributes):**
    ```xml
    <food type="dessert">Ice cream</food> 
    ```
4.  **Mixed Content:**
    ```xml
    <description>It happened on <date lang="norwegian">03.03.99</date></description>
    ```

### Comment définir un élément complexe ? (How to Define a Complex Element?)

#tags: #XSD #complex_type #global_definition #local_definition #inline_definition #named_type #anonymous_type #modularity #reusability

There are two main structural approaches to defining complex types and elements in XSD:

1.  **Structure en profondeur (Deep / Nested / Local Structure):**
    *   Type definitions (especially complex types) are defined *inline* within the element declaration that uses them.
    *   Element declarations are often nested inside the complex type definitions of their parents.
    *   These types are "anonymous" (no `name` attribute on the `<xs:complexType>` or `<xs:simpleType>`) and cannot be easily reused elsewhere in the schema.
    *   **Pro:** Can be intuitive for simple, non-repeating structures.
    *   **Con:** Less modular, harder to read for complex structures, prevents type reuse.

2.  **Structure plate (Flat / Global Structure - Recommended):**
    *   **Named Types:** Define complex types (and simple types) globally as direct children of `<xs:schema>`, giving them a `name`.
        ```xml
        <xs:schema ...>
          <xs:complexType name="PersonType">...</xs:complexType>
          <xs:element name="employee" type="PersonType"/>
          <xs:element name="manager" type="PersonType"/>
        </xs:schema>
        ```
    *   **Global Elements:** Define elements globally as direct children of `<xs:schema>`.
    *   **References:** Use the `ref` attribute within content models (`<xs:sequence>`, `<xs:choice>`, `<xs:all>`) to refer to these globally declared elements, and use the `type` attribute on element/attribute declarations to refer to globally defined types.
    *   **Pro:** Promotes modularity and reusability (define once, use many times), often easier to read and manage for larger schemas.
    *   **Con:** Requires careful naming and referencing.

**Example Comparison (Slides 42-43):**

*   **Deep Structure:**
    ```xml
    <xs:element name="employee">
      <xs:complexType> <!-- Anonymous type -->
        <xs:sequence>
          <xs:element name="Nom" type="xs:string"/> <!-- Local element -->
          <xs:element name="Prenom" type="xs:string"/> <!-- Local element -->
        </xs:sequence>
      </xs:complexType>
    </xs:element>
    ```
*   **Flat Structure (using `ref`):**
    ```xml
    <xs:schema ...>
      <!-- Global element declarations -->
      <xs:element name="Nom" type="xs:string"/>
      <xs:element name="Prenom" type="xs:string"/>

      <!-- Global element using references -->
      <xs:element name="employee">
        <xs:complexType> 
          <xs:sequence>
            <xs:element ref="Nom"/> <!-- Reference global 'Nom' -->
            <xs:element ref="Prenom"/> <!-- Reference global 'Prenom' -->
          </xs:sequence>
        </xs:complexType>
      </xs:element>
    </xs:schema>
    ```
*   **Flat Structure (using named `type` - Slide 44):**
    ```xml
    <xs:schema ...>
      <!-- Global named complex type -->
      <xs:complexType name="personne"> 
        <xs:sequence>
          <xs:element name="nom" type="xs:string"/> 
          <xs:element name="prenom" type="xs:string"/>
        </xs:sequence>
      </xs:complexType>

      <!-- Global elements using the named type -->
      <xs:element name="employe" type="personne"/>
      <xs:element name="etudiant" type="personne"/>
      <xs:element name="enseignant" type="personne"/>
    </xs:schema>
    ```

### Type complexe à éléments (Complex Type with Element-Only Content)

#tags: #XSD #complex_type #element_only_content #xs_sequence #xs_element #ref_attribute

*   **Definition:** This is a complex type whose content model allows only child elements (no text directly within the parent).
*   **Declaration:** Defined using `<xs:complexType>` containing a content model compositor (`<xs:sequence>`, `<xs:choice>`, or `<xs:all>`) which in turn contains `<xs:element>` declarations (or references).

**Example (Global element 'livre' with element-only content):**
```xml
<xs:schema ...>
  <!-- Define global elements for title and author -->
  <xs:element name="titre" type="xs:string"/>
  <xs:element name="auteur" type="xs:string"/>

  <!-- Define global element 'livre' -->
  <xs:element name="livre"> 
    <xs:complexType> <!-- Defines the structure -->
      <xs:sequence>  <!-- Children must be 'titre' then 'auteur' -->
        <xs:element ref="titre"/>  <!-- Reference global 'titre' element -->
        <xs:element ref="auteur"/> <!-- Reference global 'auteur' element -->
      </xs:sequence>
      <!-- Can also have attributes here -->
    </xs:complexType>
  </xs:element>
</xs:schema>
```

### Type complexe avec indicateurs (Complex Type with Indicators)

#tags: #XSD #complex_type #indicator #compositor #occurrence #group #xs_all #xs_choice #xs_sequence #minOccurs #maxOccurs #xs_group #xs_attributeGroup

XSD provides several indicators (compositors and attributes) to control the structure and occurrence of elements and attributes within complex types:

**1. Indicateurs d'ordre (Order Indicators / Compositors):** Define the order and choice of child elements within a content model. Exactly one compositor must be used directly within a `<xs:complexType>` (or within a group).
    *   `<xs:all>`: Allows child elements to appear **zero or one time**, in **any order**.
        *   *Limitation:* In XSD 1.0, elements within `<xs:all>` can only have `maxOccurs="1"`.
        *   **Example:**
            ```xml
            <xs:complexType>
              <xs:all> <!-- Nom and Prenom can appear 0 or 1 time, in any order -->
                <xs:element name="nom" type="xs:string" minOccurs="0"/> 
                <xs:element name="prenom" type="xs:string" minOccurs="0"/>
              </xs:all>
            </xs:complexType>
            ```
    *   `<xs:choice>`: Allows **exactly one** of the child elements (or groups) listed within it to appear.
        *   **Example:**
            ```xml
            <xs:complexType>
              <xs:choice> <!-- Either employee OR enseignant must appear -->
                <xs:element name="employee" type="employee"/>
                <xs:element name="enseignant" type="enseignant"/>
              </xs:choice>
            </xs:complexType>
            ```
    *   `<xs:sequence>`: Requires child elements (or groups) to appear **exactly in the specified order**.
        *   **Example:**
            ```xml
            <xs:complexType>
              <xs:sequence> <!-- Nom must appear first, then Prenom -->
                <xs:element name="nom" type="xs:string"/>
                <xs:element name="prenom" type="xs:string"/>
              </xs:sequence>
            </xs:complexType>
            ```

**2. Indicateurs d'occurrence (Occurrence Indicators):** Attributes placed on `<xs:element>`, `<xs:group>`, `<xs:choice>`, `<xs:sequence>`, `<xs:any>` to control repetition.
    *   `minOccurs="N"`: The minimum number of times the element/group must appear (Default: "1"). `N` must be non-negative integer.
    *   `maxOccurs="M|unbounded"`: The maximum number of times the element/group can appear (Default: "1"). `M` must be non-negative integer >= `minOccurs`. `"unbounded"` means no upper limit.
    *   **Example:**
        ```xml
        <xs:sequence>
          <xs:element name="nom" type="xs:string"/> <!-- min=1, max=1 (default) -->
          <xs:element name="prenom" type="xs:string" minOccurs="0"/> <!-- Optional -->
          <xs:element name="child" type="xs:string" maxOccurs="unbounded"/> <!-- 1 or more -->
          <xs:element name="comment" type="xs:string" minOccurs="0" maxOccurs="5"/> <!-- 0 to 5 -->
        </xs:sequence>
        ```
        *(Slide 50 Example: `<xs:element name="prenom" ... maxOccurs="10" minOccurs="1"/>` allows 1 to 10 'prenom' elements)*.

**3. Indicateurs de groupes (Group Indicators):** Allow grouping sequences, choices, or all compositors, or groups of attributes, for reuse.
    *   `<xs:group name="GroupName">`: Defines a reusable group of elements with a specific compositor (`<xs:sequence>`, `<xs:choice>`, or `<xs:all>`) inside.
    *   `<xs:group ref="GroupName"/>`: References a defined group within a content model.
    *   `<xs:attributeGroup name="AttributeGroupName">`: Defines a reusable set of attribute declarations (`<xs:attribute>`).
    *   `<xs:attributeGroup ref="AttributeGroupName"/>`: References a defined attribute group within a `<xs:complexType>` or another `<xs:attributeGroup>`.
    *   **Purpose:** Modularity and reusability of common element sequences or attribute sets.
    *   **Example (Element Group):**

```xml
        <xs:schema ...>
          <xs:group name="persongroup">
            <xs:sequence>
              <xs:element name="NOM" type="xs:string"/>
              <xs:element name="Prenom" type="xs:string"/>
              <xs:element name="DateNaissance" type="xs:date"/>
            </xs:sequence>
          </xs:group>
          
          <xs:element name="person">
            <xs:complexType>
               <xs:sequence>
                  <xs:group ref="persongroup"/> <!-- Include the defined group -->
                  <xs:element name="country" type="xs:string"/>
               </xs:sequence>
            </xs:complexType>
          </xs:element>
        </xs:schema>
```


*   **Example (Attribute Group):**
```xml
        <xs:schema ...>
           <xs:attributeGroup name="person_attr_group">
             <xs:attribute name="nom" type="xs:string"/>
             <xs:attribute name="prenom" type="xs:string"/>
             <xs:attribute name="dateNai" type="xs:date"/>
           </xs:attributeGroup>
           
           <xs:element name="person">
             <xs:complexType>
               <!-- elements here -->
               <xs:attributeGroup ref="person_attr_group"/> <!-- Include the attributes -->
             </xs:complexType>
           </xs:element>
        </xs:schema>
```

### Élément vide (Empty Element)

#tags: #XSD #complex_type #empty_element #attribute_only

*   **Definition:** An element defined with a complex type that explicitly allows **no content** (no text, no child elements), but which **can** have attributes.
*   **Declaration:** Define a `<xs:complexType>` without any element content model (no `<xs:sequence>`, `<xs:choice>`, `<xs:all>`) or simple content (`<xs:simpleContent>`). It can contain `<xs:attribute>` declarations.

**Example:**
```xml
<xs:schema ...>
  <xs:element name="produit">
    <xs:complexType> <!-- No content model specified -->
      <xs:attribute name="prodid" type="xs:positiveInteger" use="required"/>
    </xs:complexType>
  </xs:element>
</xs:schema>
```
*   **Valid Instance:** `<produit prodid="123"/>`
*   **Invalid Instances:** `<produit prodid="123">Text</produit>`, `<produit prodid="123"><child/></produit>`

### Type complexe à contenu texte (Complex Type with Simple Content)

#tags: #XSD #complex_type #simple_content #xs_simpleContent #xs_extension #xs_restriction #attribute #text_content

*   **Definition:** Defines an element that can contain **text content** (like a simple type) but can **also have attributes**.
*   **Declaration:** Use the `<xs:simpleContent>` element inside the `<xs:complexType>`.
*   **Derivation:** Inside `<xs:simpleContent>`, you must derive from a base simple type using either:
    *   `<xs:extension base="SimpleTypeName">`: Adds attributes to the base simple type. The text content must conform to the base type.
    *   `<xs:restriction base="SimpleTypeName">`: Restricts the text content using facets *and* can restrict or add attributes (though adding attributes via restriction is less common).
*   **Purpose:** Allows elements like `<price currency="USD">19.99</price>` where `19.99` conforms to a simple type (e.g., `xs:decimal`) and `currency` is an attribute.

**Example (using Extension):**
```xml
<xs:schema ...>
  <xs:element name="ville">
    <xs:complexType>
      <xs:simpleContent>
        <!-- Add 'pays' attribute to xs:integer content -->
        <xs:extension base="xs:integer"> 
          <xs:attribute name="pays" type="xs:string" use="required"/>
        </xs:extension>
      </xs:simpleContent>
    </xs:complexType>
  </xs:element>
</xs:schema>
```
*   **Valid Instance:** `<ville pays="Algeria">35</ville>` (Content `35` is `xs:integer`, `pays` attribute is present).

### Type complexe à contenu mixte (Complex Type with Mixed Content)

#tags: #XSD #complex_type #mixed_content #text_content #element_content #character_data

*   **Definition:** Defines an element that can contain a **mix of text content and child elements** interspersed.
*   **Declaration:** Set the `mixed` attribute of the `<xs:complexType>` element to `"true"`. The content model (`<xs:sequence>`, `<xs:choice>`, `<xs:all>`) then defines the allowed child elements within the text.
    ```xml
    <xs:complexType mixed="true">
        <xs:sequence> <!-- Or choice, all -->
            <xs:element name="child1" ... />
            <xs:element name="child2" ... />
        </xs:sequence>
        <xs:attribute name="..." ... />
    </xs:complexType>
    ```
*   **Purpose:** Useful for representing document-like structures (articles, paragraphs) where markup elements (like emphasis, links) appear within the flow of text.

**Example:**
```xml
<xs:schema ...>
  <xs:element name="lettre">
    <xs:complexType mixed="true"> <!-- Allow mixed content -->
      <xs:sequence>
         <!-- Define allowed child elements -->
        <xs:element name="nom" type="xs:string" minOccurs="0"/> 
        <xs:element name="numero" type="xs:positiveInteger" minOccurs="0"/>
        <xs:element name="datePublication" type="xs:date" minOccurs="0"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
```
*   **Valid Instance:**
    ```xml
    <lettre>
      Dear Mr. <nom>Ali BenAli</nom>.
      posséde le numero order <numero>1032</numero>
      publié le <datePublication>2001-07-13</datePublication>.
    </lettre>
    ```
    *(Text appears alongside the `<nom>`, `<numero>`, and `<datePublication>` elements).*


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