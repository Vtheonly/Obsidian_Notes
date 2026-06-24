
*   Components are typically function-based.
*   File extension: `.jsx`.
*   Convention: Component names are PascalCase (e.g., `Header`, `MyComponent`).

**Steps to Create a Component (e.g., `Header.jsx`):**

1.  **Create File**: In `src/`, create `Header.jsx`.
2.  **Define Function**:
    ```javascript
    function Header() {
        // JavaScript logic can go here
        return (
            // JSX (HTML-like structure)
            <header>
                <h1>My Website</h1>
                <nav>
                    <ul>
                        <li><a href="#">Home</a></li>
                        {/* More list items */}
                    </ul>
                </nav>
                <hr />
            </header>
        );
    }
    ```
3.  **Export Component**:
    ```javascript
    export default Header;
    ```

**Key JSX Rules in `return()`:**

*   **Single Root Element**: A component must return a single top-level JSX element.
    *   If you need multiple sibling elements, wrap them in a **Fragment**: `<> ... </>` or `<React.Fragment> ... </React.Fragment>`.
*   **Embedding JavaScript**: Use curly braces `{}` to embed JavaScript expressions.
    *   Example: `<h1>{new Date().getFullYear()}</h1>`
    *   Example: `<li>{foodOne}</li>`
    *   Example: `<li>{foodTwo.toUpperCase()}</li>`
*   JavaScript variables/constants defined *outside* the `return` statement (but inside the component function) can be used directly within `{}` in the JSX.

**Importing and Using Components (e.g., in `App.jsx`):**

1.  **Import**:
    ```javascript
    import Header from './Header.jsx'; // Assuming Header.jsx is in the same folder
    import Footer from './Footer.jsx';
    import Food from './Food.jsx';
    ```
2.  **Use in JSX**:
    ```javascript
    function App() {
        // Clean up default content from App.jsx
        // Remove unused imports (useState, logo)
        // Delete content from App.css if desired

        return (
            <> {/* Fragment to return multiple components */}
                <Header />
                <Food />
                <Food /> {/* Components are reusable */}
                <Footer />
            </>
        );
    }

    export default App;
    ```
    *   Self-closing tag: `<Header />` if no children components/content.
    *   Paired tags: `<Header>Some child content</Header>` (less common for simple components like this).

## Example Components Created

*   **`Header.jsx`**: Contains a title, navigation links, and a horizontal rule.
*   **`Footer.jsx`**: Contains a copyright notice with the current year dynamically generated using `new Date().getFullYear()`.
*   **`Food.jsx`**:
    *   Defines JavaScript constants (`foodOne`, `foodTwo`).
    *   Returns an unordered list displaying these food items, demonstrating JS variable usage and method calls (`.toUpperCase()`) within JSX.

## Core Idea: Reusability

Components are designed to be reusable. You can render the same component multiple times (`<Food />`, `<Food />`) or rearrange their order easily within a parent component to change the application's layout and feel.

## Styling

*   Global styles can be placed in `index.css`.
*   Component-specific styles can be created (e.g., `App.css` for `App.jsx`), but the tutorial deletes `App.css` content for a fresh start.
*   Future videos will cover CSS application methods in more detail.

# React: Importing & Exporting Components (Focus on `default`)

In React, applications are built by composing smaller, reusable pieces of code called components. To make this work, React (and JavaScript modules in general) use an `import` and `export` system. The tutorials provided primarily use **`default` exports** for components.

## Exporting a Component (using `export default`)

When you create a component in its own file (e.g., `Header.jsx`, `Card.jsx`), you need to make it available for other parts of your application to use. This is done with the `export` keyword.

*   **`export default ComponentName;`**
    *   This statement is typically placed at the end of the component's `.jsx` file.
    *   It signifies that `ComponentName` is the **primary or default thing** being exported from that file (module).
    *   A JavaScript module can have **only one `default` export**.

**Examples from the text:**

```javascript
// In src/Header.jsx
function Header() {
  // ... component logic ...
  return (/* ... JSX ... */);
}
export default Header; // Header is the default export of this file

// In src/Footer.jsx
function Footer() {
  // ... component logic ...
  return (/* ... JSX ... */);
}
export default Footer; // Footer is the default export

// In src/Card.jsx
function Card() {
  // ... component logic ...
  return (/* ... JSX ... */);
}
export default Card; // Card is the default export
```

Even the main `App` component is often set up this way:

```javascript
// In src/App.jsx
function App() {
  // ... component logic ...
  return (/* ... JSX ... */);
}
export default App;
```

## Importing a `default` Export

Once a component is exported as a `default`, you can import it into another file (e.g., into `App.jsx` to use the `Header` or `Card` component, or into `main.jsx` to use the `App` component).

*   **`import ChosenName from './path/to/File.jsx';`**
    *   **`ChosenName`**: When importing a `default` export, you can give it **any name you like** in the importing file. By convention, this name often matches the original component name (e.g., importing `Header` as `Header`), but it's not a strict requirement.
    *   **`'./path/to/File.jsx'`**: This is the relative path from the current file to the `.jsx` file containing the `export default`.
        *   `./` means "in the current directory."
        *   `../` would mean "in the parent directory."
        *   `./assets/image.jpg` would mean "in the assets sub-directory."

**Examples from the text:**

```javascript
// In src/App.jsx, importing Header, Footer, and Food components
import Header from './Header.jsx';    // Importing the default export from Header.jsx
import Footer from './Footer.jsx';    // Importing the default export from Footer.jsx
import Food from './Food.jsx';      // Importing the default export from Food.jsx

// To use them:
// <Header />
// <Footer />
// <Food />

// In src/App.jsx, importing the Card component
import Card from './Card.jsx'; // Importing the default export from Card.jsx

// To use it:
// <Card />
```

**Importing Assets (like Images):**

The same `import` syntax is used for assets when your build tool (like Vite) is configured to handle them. The asset is effectively the `default` export of that file from the perspective of the JavaScript module system.

```javascript
// In src/Card.jsx
import profilePic from './assets/profile.jpeg';
// 'profilePic' now holds a reference (e.g., a URL) to the image.
// <img src={profilePic} alt="profile picture" />
```

## Why `default` Exports for Components?

*   **Simplicity**: When a file's primary purpose is to define a single component, `export default` makes it straightforward to export and import.
*   **Flexibility in Naming (on import)**: As shown, you can rename the component during import if needed, though it's common practice to keep the name consistent for clarity.

In summary, `export default` is used to declare the main component (or value) a file provides, and `import AnyName from 'path'` is used to bring that component into another file, allowing you to choose `AnyName` for its local reference. This system is fundamental for building modular and organized React applications.
```