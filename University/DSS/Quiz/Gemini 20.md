---
sources: []
---
> [!question] In a DTD, `(#PCDATA)` means an element can only contain Parsed Character Data (text) and cannot contain child elements.
>> [!success]- Answer
>> True

> [!question] Which DTD attribute type is used to ensure an attribute's value is unique across the entire XML document and can be referenced by other attributes?
> a) CDATA
> b) NMTOKEN
> c) ID
> d) IDREF
>> [!success]- Answer
>> c) ID

> [!question] According to the employee DTD example (`employés.dtd`), which of the following elements are *optional* children of the `employé` element? (Select all that apply)
> a) prénom
> b) nom
> c) email
> d) NumTel
> e) salaire
> f) id
>> [!success]- Answer
>> c) email

> [!question] Match the DTD attribute declaration keyword (Group A) with its meaning (Group B).
>> [!example] Group A
>> a) #REQUIRED
>> b) #IMPLIED
>> c) #FIXED "value"
>> d) Default "value"
>
>> [!example] Group B
>> n) The attribute is optional.
>> o) The attribute must be present.
>> p) The attribute is optional, but if omitted, it defaults to the specified value.
>> q) The attribute must have the specified value if present.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> q)
>> d) -> p)

> [!question] An XML Schema definition is itself an XML document, unlike a DTD.
>> [!success]- Answer
>> True

> [!question] In XML Schema, which element is used to define a restriction or constraint on a data type (e.g., setting a required pattern)?
> a) `<xs:complexType>`
> b) `<xs:simpleType>`
> c) `<xs:restriction>`
> d) `<xs:element>`
>> [!success]- Answer
>> c) `<xs:restriction>`

> [!question] Based on the graph XML (`graphe1.xml`), which of the following XPath expressions correctly selects the `sbut` attribute value for arcs originating from the `sommet` with `setiq="a01"`? (Select all that apply)
> a) `/graphe/sommet[@setiq='a01']/arc/@sbut`
> b) //sommet[@setiq='a01']/arc/@sbut
> c) //arc[../@setiq='a01']/@sbut
> d) //sommet[setiq='a01']/arc/sbut
> e) /graphe/sommet[1]/arc/@sbut
> f) //sommet[@setiq='a01']/@sbut
>> [!success]- Answer
>> a) `/graphe/sommet[@setiq='a01']/arc/@sbut`
>> b) //sommet[@setiq='a01']/arc/@sbut
>> c) //arc[../@setiq='a01']/@sbut

> [!question] Match the XML Schema component (Group A) with its typical use (Group B).
>> [!example] Group A
>> a) `<xs:sequence>`
>> b) `<xs:choice>`
>> c) `<xs:attribute>`
>> d) `<xs:pattern>`
>
>> [!example] Group B
>> n) Defines an attribute for an element.
>> o) Specifies a regular expression constraint for a simple type.
>> p) Enforces a specific order for child elements.
>> q) Allows only one of a set of child elements to appear.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] The XPath expression `count(//chanson)` applied to the `CD.xml` example would return the total number of `<chanson>` elements in the entire document.
>> [!success]- Answer
>> True

> [!question] Which XPath function would you use to select employees (`employé`) whose `nom` *contains* the letter 's', based on `employés.xml`?
> a) `substring()`
> b) `starts-with()`
> c) `text()`
> d) `contains()`
>> [!success]- Answer
>> d) `contains()`

> [!question] In the `Enseignement.XML` example, which XPath expressions select the `intitule` attribute of the `chapitre` element named "SQL"? (Select all that apply)
> a) //chapitre[@intitule='SQL']/@intitule
> b) //chapitre[intitule='SQL']/@intitule
> c) /lenseignement/module/chapitres/chapitre[@intitule='SQL']/@intitule
> d) //chapitre[.='SQL']/@intitule
> e) //attribute::intitule[../@intitule='SQL']
> f) //chapitre[contains(@intitule, 'SQL')]/@intitule
>> [!success]- Answer
>> a) //chapitre[@intitule='SQL']/@intitule
>> c) /lenseignement/module/chapitres/chapitre[@intitule='SQL']/@intitule
>> f) //chapitre[contains(@intitule, 'SQL')]/@intitule

> [!question] Match the XSLT element (Group A) with its primary function (Group B).
>> [!example] Group A
>> a) `<xsl:template match="...">`
>> b) `<xsl:apply-templates select="...">`
>> c) `<xsl:value-of select="...">`
>> d) `<xsl:for-each select="...">`
>
>> [!example] Group B
>> n) Iterates over a node-set selected by an XPath expression.
>> o) Defines a rule to be applied when a node matching the pattern is encountered.
>> p) Extracts and outputs the string value of a selected node.
>> q) Processes the children or selected nodes of the current node according to matching templates.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> p)
>> d) -> n)

> [!question] Namespaces in XML are primarily used to provide metadata about the document's author.
>> [!success]- Answer
>> False

> [!question] How is a namespace typically declared within an XML document?
> a) Using a processing instruction `<?xml-namespace ...?>`
> b) Using the `xmlns` or `xmlns:prefix` attribute
> c) Using a `<namespace>` element in the document root
> d) By defining it in the DTD using `<!NAMESPACE ...>`
>> [!success]- Answer
>> b) Using the `xmlns` or `xmlns:prefix` attribute

> [!question] From the `CD.xml` structure, which XPath expressions would select the `ville` element of the artiste whose `num` attribute is 'a02'? (Select all that apply)
> a) //artiste[@num='a02']/ville
> b) /CD/artiste[@num='a02']/ville
> c) //ville[../@num='a02']
> d) //artiste[num='a02']/ville
> e) //artiste[attribute::num='a02']/child::ville
> f) //artiste[@num=a02]/ville
>> [!success]- Answer
>> a) //artiste[@num='a02']/ville
>> b) /CD/artiste[@num='a02']/ville
>> c) //ville[../@num='a02']
>> e) //artiste[attribute::num='a02']/child::ville

> [!question] Match the concept (Group A) related to XML structure with its definition (Group B).
>> [!example] Group A
>> a) Well-formed
>> b) Valid
>> c) Root Element
>> d) Attribute
>
>> [!example] Group B
>> n) A name-value pair providing additional information about an element.
>> o) Conforms to the basic syntax rules of XML (e.g., proper nesting, closing tags).
>> p) The single, top-level element that contains all other elements in an XML document.
>> q) Conforms to the rules defined in a DTD or XML Schema in addition to being well-formed.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> p)
>> d) -> n)

> [!question] In XSLT, `<xsl:call-template>` processes nodes based on matching template rules, while `<xsl:apply-templates>` explicitly calls a named template.
>> [!success]- Answer
>> False

> [!question] Which XPath expression finds the `nom` of the employee (`employé`) with the highest `salaire` in `employés.xml`?
> a) //employé[salaire=max(//salaire)]/nom
> b) max(//employé/salaire)/../nom
> c) //employé[salaire > avg(//salaire)]/nom
> d) //nom[../salaire = max(//employé/salaire)]
>> [!success]- Answer
>> a) //employé[salaire=max(//salaire)]/nom
>> d) //nom[../salaire = max(//employé/salaire)]

> [!question] Based on the `Company.xml` rattrapage example, which of the following attributes are defined for the `Person` element? (Select all that apply)
> a) Manager
> b) Degree
> c) First
> d) Last
> e) PhoneExt
> f) EMail
>> [!success]- Answer
>> a) Manager
>> b) Degree

> [!question] Match the file type/concept (Group A) with its typical role in XML processing (Group B).
>> [!example] Group A
>> a) XML file (.xml)
>> b) DTD file (.dtd)
>> c) XSLT file (.xsl or .xslt)
>> d) XML Schema file (.xsd)
>
>> [!example] Group B
>> n) Contains the data structured with tags.
>> o) Defines the rules for transforming XML into another format.
>> p) Defines the structure and vocabulary of an XML document (older syntax).
>> q) Defines the structure, constraints, and data types of an XML document (XML-based syntax).
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)
>> d) -> q)