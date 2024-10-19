# React Notes

## Introduction

### Overview
- **React**: A JavaScript library for building user interfaces.
- **Components**: Self-contained sections of code that function as reusable building blocks.

### Key Features
- **JSX (JavaScript XML)**: Allows HTML-like code within JavaScript files.
- **Virtual DOM**: A lightweight version of the real DOM to efficiently update and render changes.

### Prerequisites
- **JavaScript**: Arrays, classes, objects, ES6 features like arrow functions.
- **HTML**: Essential for rendering elements.
- **CSS**: Required for styling components.

## Setup

### Installation
1. **Download Node.js** from [nodejs.org](https://nodejs.org/).
2. **Install a text editor** like VS Code from [code.visualstudio.com](https://code.visualstudio.com/).

### Project Initialization
1. **Open a terminal** in VS Code: `Terminal > New Terminal`.
2. **Navigate to project folder**: `cd path/to/your/project`.
3. **Create a React app**:
   ```sh
   npm create vite@latest my-react-app
   cd my-react-app
   npm install
   npm run dev
   ```

---

### What is Vite?

Vite is a modern build tool that provides an alternative to traditional build tools like Webpack, Parcel, and others. Developed by Evan You, the creator of Vue.js, Vite is designed to provide a faster and more efficient development experience for modern web projects. Here's a brief overview of Vite's features and benefits:

- **Fast Cold Starts**: Vite uses native ES modules to serve files during development, which eliminates the need for bundling. This results in significantly faster cold starts compared to traditional bundlers.
- **Hot Module Replacement (HMR)**: Vite's HMR is designed to be fast and efficient, allowing developers to see changes instantly without a full reload.
- **Optimized Build**: For production, Vite bundles the application using Rollup, ensuring that the final build is optimized and efficient.
- **Out-of-the-Box Support**: Vite has built-in support for popular frameworks like React, Vue, and others, making it easy to get started with minimal configuration.

### Why Should I Run `npm install`?

When you create a new project using Vite (or any other tool that generates a project scaffold), the project usually includes a `package.json` file. This file contains a list of dependencies that your project needs to run. Here's why running `npm install` is essential:

- **Install Dependencies**: The `npm install` command reads the `package.json` file and installs all the listed dependencies into a `node_modules` directory. These dependencies include libraries and tools your project relies on to function correctly.
- **Resolve Versions**: It ensures that the exact versions of dependencies specified in the `package.json` are installed, maintaining consistency across different environments.
- **Prepare for Development**: By installing all necessary packages, it sets up the development environment so you can start coding, building, and running your project.

### Step-by-Step Explanation of Your Commands

1. **Create a New Project**:
    ```bash
    npm create vite@latest my-react-app
    ```
    - This command initializes a new Vite project named `my-react-app`. It prompts you to select a framework (React) and a variant (JavaScript).

2. **Navigate to the Project Directory**:
    ```bash
    cd .\my-react-app\
    ```
    - This command changes the current working directory to the newly created project folder.

3. **Install Dependencies**:
    ```bash
    npm install
    ```
    - This command installs all the necessary dependencies listed in the `package.json` file. It ensures your project has everything it needs to run.

4. **Start the Development Server**:
    ```bash
    npm run dev
    ```
    - This command starts the Vite development server. The server will watch your files for changes and provide fast feedback with Hot Module Replacement (HMR).

### Summary

- **Vite** is a modern build tool that offers fast development and optimized production builds.
- Running `npm install` is crucial for setting up your project's dependencies and preparing your development environment.
- After installing dependencies, you can start the development server to begin working on your project.

---
## Project Structure

### Folders
- **node_modules**: Contains external libraries and packages.
- **public**: Stores public assets (fonts, images, videos).
- **src**: Main folder for source code.
  - **assets**: Contains images and videos bundled during the final output.
  - **components**: Folder for React components.

### Important Files
- **main.jsx**: Entry point, imports the root component.
- **App.jsx**: Root component of the application.
- **index.html**: Main HTML file with a root `div` where React components are rendered.
- **package.json**: Contains project metadata and dependencies.

## Creating Components

### Functional Components
1. **Creating a component**:
   ```jsx
   // Header.jsx
   import React from 'react';

   function Header() {
     return (
       <header>
         <h1>My Website</h1>
         <nav>
           <ul>
             <li><a href="#">Home</a></li>
             <li><a href="#">About</a></li>
             <li><a href="#">Services</a></li>
             <li><a href="#">Contact</a></li>
           </ul>
         </nav>
       </header>
     );
   }

   export default Header;
   ```

2. **Importing and using a component**:
   ```jsx
   // App.jsx
   import React from 'react';
   import Header from './Header';

   function App() {
     return (
       <>
         <Header />
       </>
     );
   }

   export default App;
   ```

### Exporting and Importing
- **Export a component**:
  ```jsx
  export default ComponentName;
  ```
- **Import a component**:
  ```jsx
  import ComponentName from './ComponentName';
  ```

## JSX Syntax
- **Embedding expressions**:
  ```jsx
  const name = 'React';
  const element = <h1>Hello, {name}!</h1>;
  ```

- **Conditional rendering**:
  ```jsx
  const isLoggedIn = true;
  return (
    <div>
      {isLoggedIn ? <h1>Welcome back!</h1> : <h1>Please sign up.</h1>}
    </div>
  );
  ```

- **Lists and keys**:
  ```jsx
  const numbers = [1, 2, 3, 4, 5];
  const listItems = numbers.map((number) =>
    <li key={number.toString()}>{number}</li>
  );

  return (
    <ul>{listItems}</ul>
  );
  ```

## Advanced Topics

### State and Props
- **State**: Manages component data.
  ```jsx
  import React, { useState } from 'react';

  function Counter() {
    const [count, setCount] = useState(0);

    return (
      <div>
        <p>You clicked {count} times</p>
        <button onClick={() => setCount(count + 1)}>Click me</button>
      </div>
    );
  }

  export default Counter;
  ```

- **Props**: Passes data to components.
  ```jsx
  function Welcome(props) {
    return <h1>Hello, {props.name}</h1>;
  }

  function App() {
    return (
      <div>
        <Welcome name="Sara" />
        <Welcome name="Cahal" />
        <Welcome name="Edite" />
      </div>
    );
  }
  ```

### Lifecycle Methods (Class Components)
- **Mounting, Updating, and Unmounting**:
  ```jsx
  import React, { Component } from 'react';

  class Example extends Component {
    componentDidMount() {
      // Runs after the component output has been rendered to the DOM
    }

    componentDidUpdate(prevProps, prevState) {
      // Runs after the component updates
    }

    componentWillUnmount() {
      // Runs before the component is removed from the DOM
    }

    render() {
      return <div>Example Component</div>;
    }
  }

  export default Example;
  ```

### Event Handling
- **Handling events**:
  ```jsx
  function handleClick() {
    console.log('Button clicked!');
  }

  return (
    <button onClick={handleClick}>Click me</button>
  );
  ```

## Styling Components
- **Inline styles**:
  ```jsx
  const divStyle = {
    color: 'blue',
    backgroundColor: 'lightgray',
  };

  function StyledComponent() {
    return <div style={divStyle}>Styled Div</div>;
  }
  ```

- **CSS Modules**:
  ```jsx
  import styles from './App.module.css';

  function App() {
    return <div className={styles.container}>Styled with CSS Modules</div>;
  }

  export default App;
  ```

- **Styled Components**:
  ```jsx
  import styled from 'styled-components';

  const Button = styled.button`
    background: blue;
    color: white;
    font-size: 1em;
    padding: 0.25em 1em;
    border-radius: 3px;
  `;

  function App() {
    return <Button>Styled Button</Button>;
  }

  export default App;
  ```

---

This structured approach provides a comprehensive understanding of React, from setup to creating and using components, and advanced topics like state management and styling.