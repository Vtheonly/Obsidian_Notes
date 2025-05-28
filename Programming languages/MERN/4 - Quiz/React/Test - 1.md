---
sources:
  - "[[React Project Structure]]"
---
> [!question] Which folder contains all the external libraries and packages your project relies on?
> a) `public`
> b) `src`
> c) `node_modules`
> d) `assets`
>> [!success]- Answer
>> c) `node_modules`

> [!question] Where should you place static assets like images and videos that need to be directly accessible by the public?
> a) `node_modules`
> b) `public`
> c) `src`
> d) `components`
>> [!success]- Answer
>> b) `public`

> [!question] What is the primary purpose of the `src` folder in a React project?
> a) To store external libraries
> b) To hold static files that are not processed by the build tool
> c) To contain the main source code of the application
> d) To store package metadata
>> [!success]- Answer
>> c) To contain the main source code of the application

> [!question] Which folder typically contains the main `index.html` file for your React application?
> a) `src`
> b) `public`
> c) `node_modules`
> d) `assets`
>> [!success]- Answer
>> b) `public`

> [!question] Which file in a React project is the entry point that renders the root component into the DOM?
> a) `App.jsx`
> b) `index.html`
> c) `main.jsx`
> d) `package.json`
>> [!success]- Answer
>> c) `main.jsx`

> [!question] Which folder inside `src` is typically used to organize reusable React components?
> a) `public`
> b) `assets`
> c) `components`
> d) `node_modules`
>> [!success]- Answer
>> c) `components`

> [!question] What is the role of the `App.jsx` file in a React project?
> a) To manage external libraries
> b) To define and structure the root component of the application
> c) To serve static assets to the public
> d) To configure project metadata
>> [!success]- Answer
>> b) To define and structure the root component of the application

> [!question] Where do you store images that need to be bundled into the final build of your React application?
> a) `public`
> b) `node_modules`
> c) `components`
> d) `assets`
>> [!success]- Answer
>> d) `assets`

> [!question] Which file contains scripts for running tasks like starting the development server or building the app?
> a) `main.jsx`
> b) `App.jsx`
> c) `package.json`
> d) `index.html`
>> [!success]- Answer
>> c) `package.json`

> [!question] How do you reference an image located in the `public` folder in your React code?
> a) `import exampleImage from './public/example.jpg';`
> b) `<img src={`${process.env.PUBLIC_URL}/example.jpg`} alt="example" />`
> c) `<img src="./src/assets/example.jpg" alt="example" />`
> d) `<img src="./components/example.jpg" alt="example" />`
>> [!success]- Answer
>> b) `<img src={`${process.env.PUBLIC_URL}/example.jpg`} alt="example" />`

> [!question] What happens to files placed in the `assets` folder during the build process?
> a) They are directly served without modification
> b) They are bundled and processed by the build tool
> c) They are deleted before deployment
> d) They are moved to the `node_modules` folder
>> [!success]- Answer
>> b) They are bundled and processed by the build tool

> [!question] Which file typically contains a `<div>` with an `id` of `root`?
> a) `main.jsx`
> b) `App.jsx`
> c) `index.html`
> d) `package.json`
>> [!success]- Answer
>> c) `index.html`

> [!question] What kind of assets should be placed in the `public` folder?
> a) Assets that need to be bundled and processed by Webpack
> b) Global assets that should be served as-is, like a favicon
> c) JavaScript components
> d) Node modules
>> [!success]- Answer
>> b) Global assets that should be served as-is, like a favicon

> [!question] Which file contains metadata about the project and its dependencies?
> a) `App.jsx`
> b) `package.json`
> c) `main.jsx`
> d) `index.html`
>> [!success]- Answer
>> b) `package.json`

> [!question] How do you typically import an image from the `assets` folder in a React component?
> a) `import image from '../public/image.jpg';`
> b) `import image from './assets/image.jpg';`
> c) `import image from '../../node_modules/image.jpg';`
> d) `import image from '../components/image.jpg';`
>> [!success]- Answer
>> b) `import image from './assets/image.jpg';`

> [!question] What type of files would you place in the `components` folder?
> a) JavaScript files that define reusable UI components
> b) Static files that need to be accessed directly
> c) Node.js server files
> d) Configuration files for the build process
>> [!success]- Answer
>> a) JavaScript files that define reusable UI components

> [!question] How are paths resolved for assets placed in the `assets` folder?
> a) They are hardcoded and never change
> b) They are resolved by the build tool during the bundling process
> c) They are ignored and not bundled
> d) They are moved to the `public` folder automatically
>> [!success]- Answer
>> b) They are resolved by the build tool during the bundling process

> [!question] Which file is responsible for bootstrapping the entire React application?
> a) `App.jsx`
> b) `index.html`
> c) `main.jsx`
> d) `package.json`
>> [!success]- Answer
>> c) `main.jsx`

> [!question] What does the `react-scripts start` command do in a React project?
> a) Starts the production build process
> b) Ejects the project from the default configuration
> c) Starts the development server
> d) Installs project dependencies
>> [!success]- Answer
>> c) Starts the development server

> [!question] What is the purpose of the `ReactDOM.render` method in `main.jsx`?
> a) To define the structure of the root component
> b) To bundle and minify assets for production
> c) To render the React component tree into the DOM
> d) To import and organize external libraries
>> [!success]- Answer
>> c) To render the React component tree into the DOM