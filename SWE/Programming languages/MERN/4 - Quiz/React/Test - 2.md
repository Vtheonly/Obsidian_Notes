---
sources:
  - "[[Understanding Props in React]]"
---
> [!question] What is the primary purpose of props in React?
> a) To style components
> b) To manage state within a component
> c) To pass data from one component to another
> d) To render components conditionally
>> [!success]- Answer
>> c) To pass data from one component to another

> [!question] In the `Student` component, how is the `isStudent` prop used?
> a) To conditionally apply CSS styles
> b) To determine the text displayed ('Yes' or 'No')
> c) To define a method
> d) To manipulate the component's state
>> [!success]- Answer
>> b) To determine the text displayed ('Yes' or 'No')

> [!question] What will happen if a required prop is not passed to a component that has `propTypes` defined?
> a) The component will not render
> b) A warning will be shown in the console
> c) The app will crash
> d) The component will use default values
>> [!success]- Answer
>> b) A warning will be shown in the console

> [!question] Which library is used to define prop types in React?
> a) `prop-checker`
> b) `prop-types`
> c) `type-check`
> d) `react-validator`
>> [!success]- Answer
>> b) `prop-types`

> [!question] What will be the value of the `name` prop in the `Student` component when rendered without any props in the example?
> a) `undefined`
> b) `'Guest'`
> c) `'Anonymous'`
> d) `null`
>> [!success]- Answer
>> b) `'Guest'`

> [!question] Where do you typically define the `defaultProps` for a component?
> a) In the `App` component
> b) At the top of the component file
> c) Directly after the component definition
> d) Inside the `render` method
>> [!success]- Answer
>> c) Directly after the component definition

> [!question] What is the output of the `age` prop when it is not provided in the `Student` component?
> a) `undefined`
> b) `0`
> c) `null`
> d) `20`
>> [!success]- Answer
>> b) `0`

> [!question] How do you pass a prop from a parent to a child component in React?
> a) By defining it inside the child component
> b) By using `this.props` in the parent component
> c) By using the component's state
> d) By including it as an attribute in the JSX of the parent component
>> [!success]- Answer
>> d) By including it as an attribute in the JSX of the parent component

> [!question] Which prop type validation is used to ensure a prop is a required number?
> a) `PropTypes.number`
> b) `PropTypes.number.required`
> c) `PropTypes.number.isRequired`
> d) `PropTypes.required.number`
>> [!success]- Answer
>> c) `PropTypes.number.isRequired`

> [!question] What is the benefit of using `defaultProps` in a component?
> a) It prevents runtime errors
> b) It sets a fallback value when a prop is not provided
> c) It validates the type of props
> d) It improves the performance of the component
>> [!success]- Answer
>> b) It sets a fallback value when a prop is not provided

> [!question] How can you access props inside a functional component?
> a) By using `this.props`
> b) By passing them as a parameter to the function
> c) By using `getProps()`
> d) By using `useProps()`
>> [!success]- Answer
>> b) By passing them as a parameter to the function

> [!question] Which of the following is NOT a valid prop type in `PropTypes`?
> a) `PropTypes.string`
> b) `PropTypes.arrayOf`
> c) `PropTypes.func`
> d) `PropTypes.date`
>> [!success]- Answer
>> d) `PropTypes.date`

> [!question] If you pass an additional prop to a component that is not defined in `propTypes`, what happens?
> a) The component will ignore it
> b) A warning will be shown in the console
> c) The app will crash
> d) The component will receive the prop without any issues
>> [!success]- Answer
>> d) The component will receive the prop without any issues

> [!question] How can you ensure a prop passed to a component is a string?
> a) `PropTypes.ensureString`
> b) `PropTypes.stringOnly`
> c) `PropTypes.string.isRequired`
> d) `PropTypes.string`
>> [!success]- Answer
>> d) `PropTypes.string`

> [!question] What is the purpose of using `isRequired` with a prop type?
> a) To make the prop optional
> b) To ensure the prop is not undefined or null
> c) To give the prop a default value
> d) To make sure the prop is an array
>> [!success]- Answer
>> b) To ensure the prop is not undefined or null