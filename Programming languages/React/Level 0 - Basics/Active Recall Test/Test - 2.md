### Understanding Props in React Quiz

1. **What is the primary purpose of props in React?**
   - [ ] A) To style components
   - [ ] B) To manage state within a component
   - [ ] C) To pass data from one component to another
   - [ ] D) To render components conditionally

2. **In the `Student` component, how is the `isStudent` prop used?**
   - [ ] A) To conditionally apply CSS styles
   - [ ] B) To determine the text displayed ('Yes' or 'No')
   - [ ] C) To define a method
   - [ ] D) To manipulate the component's state

3. **What will happen if a required prop is not passed to a component that has `propTypes` defined?**
   - [ ] A) The component will not render
   - [ ] B) A warning will be shown in the console
   - [ ] C) The app will crash
   - [ ] D) The component will use default values

4. **Which library is used to define prop types in React?**
   - [ ] A) `prop-checker`
   - [ ] B) `prop-types`
   - [ ] C) `type-check`
   - [ ] D) `react-validator`

5. **What will be the value of the `name` prop in the `Student` component when rendered without any props in the example?**
   - [ ] A) `undefined`
   - [ ] B) `'Guest'`
   - [ ] C) `'Anonymous'`
   - [ ] D) `null`

6. **Where do you typically define the `defaultProps` for a component?**
   - [ ] A) In the `App` component
   - [ ] B) At the top of the component file
   - [ ] C) Directly after the component definition
   - [ ] D) Inside the `render` method

7. **What is the output of the `age` prop when it is not provided in the `Student` component?**
   - [ ] A) `undefined`
   - [ ] B) `0`
   - [ ] C) `null`
   - [ ] D) `20`

8. **How do you pass a prop from a parent to a child component in React?**
   - [ ] A) By defining it inside the child component
   - [ ] B) By using `this.props` in the parent component
   - [ ] C) By using the component's state
   - [ ] D) By including it as an attribute in the JSX of the parent component

9. **Which prop type validation is used to ensure a prop is a required number?**
   - [ ] A) `PropTypes.number`
   - [ ] B) `PropTypes.number.required`
   - [ ] C) `PropTypes.number.isRequired`
   - [ ] D) `PropTypes.required.number`

10. **What is the benefit of using `defaultProps` in a component?**
    - [ ] A) It prevents runtime errors
    - [ ] B) It sets a fallback value when a prop is not provided
    - [ ] C) It validates the type of props
    - [ ] D) It improves the performance of the component

11. **How can you access props inside a functional component?**
    - [ ] A) By using `this.props`
    - [ ] B) By passing them as a parameter to the function
    - [ ] C) By using `getProps()`
    - [ ] D) By using `useProps()`

12. **Which of the following is NOT a valid prop type in `PropTypes`?**
    - [ ] A) `PropTypes.string`
    - [ ] B) `PropTypes.arrayOf`
    - [ ] C) `PropTypes.func`
    - [ ] D) `PropTypes.date`

13. **If you pass an additional prop to a component that is not defined in `propTypes`, what happens?**
    - [ ] A) The component will ignore it
    - [ ] B) A warning will be shown in the console
    - [ ] C) The app will crash
    - [ ] D) The component will receive the prop without any issues

14. **How can you ensure a prop passed to a component is a string?**
    - [ ] A) `PropTypes.ensureString`
    - [ ] B) `PropTypes.stringOnly`
    - [ ] C) `PropTypes.string.isRequired`
    - [ ] D) `PropTypes.string`

15. **What is the purpose of using `isRequired` with a prop type?**
    - [ ] A) To make the prop optional
    - [ ] B) To ensure the prop is not undefined or null
    - [ ] C) To give the prop a default value
    - [ ] D) To make sure the prop is an array

### Answers

1. C) To pass data from one component to another
2. B) To determine the text displayed ('Yes' or 'No')
3. B) A warning will be shown in the console
4. B) `prop-types`
5. B) `'Guest'`
6. C) Directly after the component definition
7. B) `0`
8. D) By including it as an attribute in the JSX of the parent component
9. C) `PropTypes.number.isRequired`
10. B) It sets a fallback value when a prop is not provided
11. B) By passing them as a parameter to the function
12. D) `PropTypes.date`
13. D) The component will receive the prop without any issues
14. D) `PropTypes.string`
15. B) To ensure the prop is not undefined or null