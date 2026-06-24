---
sources:
  - "[[React Notes]]"
---
> [!question] What is the primary purpose of React?
> a) To build back-end APIs
> b) To manage databases
> c) To build user interfaces
> d) To optimize server performance
>> [!success]- Answer
>> c) To build user interfaces

> [!question] Which feature of React allows HTML-like code within JavaScript files?
> a) JSX
> b) Virtual DOM
> c) Babel
> d) TypeScript
>> [!success]- Answer
>> a) JSX

> [!question] What is the Virtual DOM used for in React?
> a) Storing data permanently
> b) Efficiently updating and rendering changes
> c) Creating animations
> d) Managing server requests
>> [!success]- Answer
>> b) Efficiently updating and rendering changes

> [!question] What is the purpose of running `npm install` after initializing a React project with Vite?
> a) To start the development server
> b) To compile the project into production code
> c) To install all necessary dependencies
> d) To update Node.js to the latest version
>> [!success]- Answer
>> c) To install all necessary dependencies

> [!question] Which command is used to start the Vite development server?
> a) `npm start`
> b) `npm run dev`
> c) `npm create vite@latest`
> d) `npm build`
>> [!success]- Answer
>> b) `npm run dev`

> [!question] In a React project, where should you place public assets like fonts and images?
> a) `src/assets`
> b) `node_modules`
> c) `public`
> d) `components`
>> [!success]- Answer
>> c) `public`

> [!question] Which file is the entry point of a React application where the root component is imported?
> a) `App.jsx`
> b) `main.jsx`
> c) `index.html`
> d) `package.json`
>> [!success]- Answer
>> b) `main.jsx`

> [!question] How do you export a React component so it can be used in other files?
> a) `import default ComponentName;`
> b) `export default ComponentName;`
> c) `export ComponentName;`
> d) `import ComponentName;`
>> [!success]- Answer
>> b) `export default ComponentName;`

> [!question] Which of the following is the correct way to create a functional component in React?
> a) ```jsx
function Header() {return <h1>My Header</h1>; }
```
> b) ```jsx function Header() {return <h1>My Header</h1>; }```
> c) ```jsx function Header() {return <h1>My Header</h1>; }```
> d) ```jsx function Header() {return <h1>My Header</h1>; }```
>> [!success]- Answer
>> b) ```jsx function Header() {return <h1>My Header</h1>; }```

> [!question] Which React hook is used to manage component state?
> a) `useState`
> b) `useEffect`
> c) `useContext`
> d) `useReducer`
>> [!success]- Answer
>> a) `useState`

> [!question] What is the purpose of the `componentDidMount` lifecycle method in class components?
> a) To handle events
> b) To update the component
> c) To clean up resources
> d) To run code after the component has been rendered to the DOM
>> [!success]- Answer
>> d) To run code after the component has been rendered to the DOM

> [!question] How do you pass data to a child component in React?
> a) Through `props`
> b) Through `state`
> c) Through `context`
> d) Through `refs`
>> [!success]- Answer
>> a) Through `props`

> [!question] Which of the following correctly applies inline styles in a React component?
> a)
> ```jsx
> <div style="color: blue; background-color: lightgray;">Styled Div</div>
> ```
> b)
> ```jsx
> const divStyle = {
>   color: 'blue',
>   backgroundColor: 'lightgray',
> };
> 
> <div style={divStyle}>Styled Div</div>
> ```
> c)
> ```jsx
> <div style={{color: blue, backgroundColor: lightgray}}>Styled Div</div>
> ```
> d)
> ```jsx
> <div className="divStyle">Styled Div</div>
> ```
>> [!success]- Answer
>> b)
>> ```jsx
>> const divStyle = {
>>   color: 'blue',
>>   backgroundColor: 'lightgray',
>> };
>> 
>> <div style={divStyle}>Styled Div</div>
>> ```

> [!question] What is the advantage of using CSS Modules in React?
> a) They allow global styling across all components.
> b) They enable scoped and modular CSS to avoid naming conflicts.
> c) They automatically optimize CSS for production.
> d) They allow inline styling without writing CSS.
>> [!success]- Answer
>> b) They enable scoped and modular CSS to avoid naming conflicts.

> [!question] Which package is used in React for defining styled components?
> a) `react-bootstrap`
> b) `styled-components`
> c) `material-ui`
> d) `classnames`
>> [!success]- Answer
>> b) `styled-components`
