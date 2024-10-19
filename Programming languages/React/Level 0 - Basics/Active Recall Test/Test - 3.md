### Conditional Rendering in React Quiz

1. **What is the purpose of conditional rendering in React?**
   - [ ] A) To define the style of a component
   - [ ] B) To render components only when specific conditions are met
   - [ ] C) To manage state across different components
   - [ ] D) To pass data from one component to another

2. **Which of the following statements correctly describes how the `UserGreeting` component works?**
   - [ ] A) It always displays "Welcome, Guest!" regardless of props
   - [ ] B) It conditionally displays a welcome message or a login prompt based on the `isLoggedIn` prop
   - [ ] C) It renders different components based on the `username` prop
   - [ ] D) It renders nothing if `username` is not provided

3. **What will be displayed when `isLoggedIn` is `true` and `username` is `"Bro Code"`?**
   - [ ] A) `Please log in to continue.`
   - [ ] B) `Welcome, Bro Code!`
   - [ ] C) `Welcome, Guest!`
   - [ ] D) `undefined`

4. **How would you modify the `UserGreeting` component to use a ternary operator for conditional rendering?**
   - [ ] A) Replace `if` statements with `switch` statements
   - [ ] B) Use the ternary operator inside the `return` statement
   - [ ] C) Remove the `props` from the component
   - [ ] D) Use an array instead of JSX

5. **What is the advantage of using constants for messages in conditional rendering?**
   - [ ] A) It makes the code longer and more complex
   - [ ] B) It enhances the readability and maintainability of the code
   - [ ] C) It prevents the component from rendering
   - [ ] D) It removes the need for CSS classes

6. **What does `defaultProps` do in the `UserGreeting` component?**
   - [ ] A) It validates the type of props passed
   - [ ] B) It sets fallback values for props when they are not provided
   - [ ] C) It prevents the component from rendering if props are missing
   - [ ] D) It automatically logs errors in the console

7. **If `isLoggedIn` is `false` and `username` is not provided, what will the component display?**
   - [ ] A) `Welcome, Bro Code!`
   - [ ] B) `Please log in to continue.`
   - [ ] C) `Welcome, Guest!`
   - [ ] D) `Error`

8. **How do you apply CSS styles based on a condition in the `App` component?**
   - [ ] A) By using inline styles only
   - [ ] B) By changing the CSS file name dynamically
   - [ ] C) By setting class names conditionally in JSX
   - [ ] D) By creating multiple CSS files

9. **Which of the following is a valid `propTypes` definition for the `UserGreeting` component?**
   - [ ] A) `PropTypes.string.isRequired`
   - [ ] B) `PropTypes.array.isRequired`
   - [ ] C) `PropTypes.string.optional`
   - [ ] D) `PropTypes.number.isRequired`

10. **How can you ensure that `username` is always passed as a string to the `UserGreeting` component?**
    - [ ] A) By using `PropTypes.string.isRequired`
    - [ ] B) By using `PropTypes.username`
    - [ ] C) By passing it as an integer
    - [ ] D) By defining it as a constant

11. **What will happen if the `isLoggedIn` prop is missing when rendering the `UserGreeting` component?**
    - [ ] A) A console error will be shown
    - [ ] B) The component will not render
    - [ ] C) The component will use the default value set in `defaultProps`
    - [ ] D) The application will crash

12. **Which method is NOT recommended for conditional rendering?**
    - [ ] A) Using `if` statements
    - [ ] B) Using ternary operators
    - [ ] C) Using constants
    - [ ] D) Rendering all components and hiding them with CSS

13. **How would you modify the `UserGreeting` component to render a custom message when no username is provided?**
    - [ ] A) Set a default value for `username` in `defaultProps`
    - [ ] B) Use an `if` statement inside the `App` component
    - [ ] C) Pass a custom message as a new prop
    - [ ] D) Replace `props.username` with `props.customMessage`

14. **What is the primary role of `propTypes` in a component?**
    - [ ] A) To handle state within the component
    - [ ] B) To define the structure and type of data passed as props
    - [ ] C) To automatically apply CSS classes
    - [ ] D) To set default values for props

15. **Which CSS class will be applied if `isLoggedIn` is `false` in the `App` component?**
    - [ ] A) `.welcome-message`
    - [ ] B) `.login-prompt`
    - [ ] C) `.guest-message`
    - [ ] D) `.error-message`

### Answers

1. B) To render components only when specific conditions are met
2. B) It conditionally displays a welcome message or a login prompt based on the `isLoggedIn` prop
3. B) `Welcome, Bro Code!`
4. B) Use the ternary operator inside the `return` statement
5. B) It enhances the readability and maintainability of the code
6. B) It sets fallback values for props when they are not provided
7. B) `Please log in to continue.`
8. C) By setting class names conditionally in JSX
9. A) `PropTypes.string.isRequired`
10. A) By using `PropTypes.string.isRequired`
11. C) The component will use the default value set in `defaultProps`
12. D) Rendering all components and hiding them with CSS
13. A) Set a default value for `username` in `defaultProps`
14. B) To define the structure and type of data passed as props
15. B) `.login-prompt`