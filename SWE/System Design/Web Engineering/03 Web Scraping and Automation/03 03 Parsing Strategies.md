## 3.3. Parsing Strategies and Document Querying

Once the raw content has been retrieved, we must query and extract targeted nodes efficiently.

---

### 1. CSS Selectors vs. XPath Expressions

To navigate the DOM tree, programmers rely on two query standards:

| Feature | CSS Selectors | XPath (XML Path Language) |
| :--- | :--- | :--- |
| **Syntactic Complexity**| Simple, clean, standardized. | Complex, powerful, extensive. |
| **Navigation Direction**| Downwards (descendant parsing only).| Bidirectional (can query ancestors/siblings). |
| **Attribute Filtering** | Basic (existence, exact match, prefix).| Advanced (complex logic, substring matches). |
| **Text Content Queries**|  No (cannot query elements based on inner text).|  Yes (can filter nodes matching inner text). |

---

### 2. Understanding XPath Power

XPath treats the DOM document as a structural tree of nodes. It allows you to write path expressions to navigate around the document.

#### Common XPath Axis Examples
* `//a[@href]`: Finds all `<a>` tags with a `href` attribute.
* `//div[@class="container"]/p`: Finds all `<p>` tags that are direct children of a `<div>` tag with a class of `"container"`.
* `//h3[contains(text(), "Results")]`: Finds any `<h3>` tag whose inner text contains the substring `"Results"`.
* `//input[@id="username"]/parent::form`: Navigates to the parent `<form>` tag containing the targeted username input.

---

###  Common Student Pitfalls & Pro-Tips
* **The Fragile Auto-Generated Selector:** Avoid right-clicking an element in your browser's Developer Tools and selecting "Copy Selector" or "Copy XPath". This generates long, absolute paths like `/html/body/div[2]/div[1]/form/div[3]/input`. If the website developers modify even a single layout tag or wrap an element in an extra container, these absolute queries will break immediately. Instead, write robust, semantic selectors targeting unique IDs, specific class names, or data attributes (e.g., `//input[@data-testid="login-input"]`).

---
