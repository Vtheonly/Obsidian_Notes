
Entities in a DTD allow you to replace a string of characters with a symbol, facilitating data reuse and management.

1. **General Entities:**
   - General entities allow you to define elements that can be substituted in the body of the XML document.
   - They can be declared internally or externally.

   Examples:
   - Internal declaration:
     ```xml
     <!ENTITY website "http://www.mysite.com">
     ```
   - External declaration:
     ```xml
     <!ENTITY website SYSTEM "http://www.mysite.com">
     ```
   - To reference them:
     ```xml
     &website;
     ```

   Example of use in an XML document:
   ```xml
   <url>The website for the DSS course is: &website;</url>
   ```
   This will be evaluated as:
```xml
   <url>The website for the DSS course is: http://www.mysite.com</url>

```
---

**Parameter Entities:**

Parameter entities allow the use of entities within the DTD itself.

- **Declaration Syntax:**
  ```xml
  <!ENTITY % entity_name definition>
  ```
- **Reference Syntax:**
  ```xml
  %entity_name;
  ```

**Declaration:**
- External Parameter Entity:
  ```xml
  <!ENTITY % entity_name SYSTEM "File_Name">
  ```
- Internal Parameter Entity:
  ```xml
  <!ENTITY % entity_name "definition">
  ```

**Example:**

```xml
<!ENTITY % common "level, color">

<!ELEMENT rectangle (%common;, vertex+) >
<!ELEMENT triangle (%common;, vertex+)>
<!ELEMENT circle (%common;, center, radius) >
```

This is equivalent to the following fragment of DTD:

```xml
<!ELEMENT rectangle (level, color, vertex+)>
<!ELEMENT triangle (level, color, vertex+)>
<!ELEMENT circle (level, color, center, radius)>
```

Parameter entities are useful for defining common sets of elements or attributes that can be reused across multiple element declarations within the DTD.
   
   
---
**Character Entities:**

Character entities allow the representation of reserved characters in XML documents.

Representation:
- `&` as `&amp;`
- `<` as `&lt;`
- `>` as `&gt;`
- `'` as `&apos;`
- `"` as `&quot;`

Note:
Any character can be inserted into a document using an entity constructed according to the syntax `&#decimal_code;` or `&#xhexadecimal_code;`.

**Example:**
The code `&#960;` or `&#x03C0;`:
allows the insertion of the Greek letter π (pi).

Character entities are reserved characters in XML represented as general entities to allow the insertion of these reserved characters into the XML document.

List of primary character entities:
- `&amp;` for `&`
- `&lt;` for `<`
- `&gt;` for `>`
- `&apos;` for `'`
- `&quot;` for `"`

---
**Notations:**

- Notations allow for identifying the format of unparsed entities by name in XML parsers. They define the data format and the applications capable of processing it.

- For example, it's possible to associate GIF images with the program `view.exe` using the following syntax:

```xml
<!DOCTYPE xs:notation [
  <!NOTATION gif PUBLIC "image/gif" "view.exe">
]>
```

In this example:
- `gif` is the name of the notation.
- `PUBLIC` indicates a public identifier.
- `"image/gif"` specifies the MIME type of the data.
- `"view.exe"` specifies the program associated with handling this data format.