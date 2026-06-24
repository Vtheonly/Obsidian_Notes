---
sources:
  - "[[Conditional Rendering in React]]"
---
> [!question] What is the purpose of conditional rendering in React?
> a) To define the style of a component
> b) To render components only when specific conditions are met
> c) To manage state across different components
> d) To pass data from one component to another
>> [!success]- Answer
>> b) To render components only when specific conditions are met

> [!question] Which of the following statements correctly describes how the `UserGreeting` component works?
> a) It always displays "Welcome, Guest!" regardless of props
> b) It conditionally displays a welcome message or a login prompt based on the `isLoggedIn` prop
> c) It renders different components based on the `username` prop
> d) It renders nothing if `username` is not provided
>> [!success]- Answer
>> b) It conditionally displays a welcome message or a login prompt based on the `isLoggedIn` prop

> [!question] What will be displayed when `isLoggedIn` is `true` and `username` is `"Bro Code"`?
> a) `Please log in to continue.`
> b) `Welcome, Bro Code!`
> c) `Welcome, Guest!`
> d) `undefined`
>> [!success]- Answer
>> b) `Welcome, Bro Code!`

> [!question] How would you modify the `UserGreeting` component to use a ternary operator for conditional rendering?
> a) Replace `if` statements with `switch` statements
> b) Use the ternary operator inside the `return` statement
> c) Remove the `props` from the component
> d) Use an array instead of JSX
>> [!success]- Answer
>> b) Use the ternary operator inside the `return` statement

> [!question] What is the advantage of using constants for messages in conditional rendering?
> a) It makes the code longer and more complex
> b) It enhances the readability and maintainability of the code
> c) It prevents the component from rendering
> d) It removes the need for CSS classes
>> [!success]- Answer
>> b) It enhances the readability and maintainability of the code

> [!question] What does `defaultProps` do in the `UserGreeting` component?
> a) It validates the type of props passed
> b) It sets fallback values for props when they are not provided
> c) It prevents the component from rendering if props are missing
> d) It automatically logs errors in the console
>> [!success]- Answer
>> b) It sets fallback values for props when they are not provided

> [!question] If `isLoggedIn` is `false` and `username` is not provided, what will the component display?
> a) `Welcome, Bro Code!`
> b) `Please log in to continue.`
> c) `Welcome, Guest!`
> d) `Error`
>> [!success]- Answer
>> b) `Please log in to continue.`

> [!question] How do you apply CSS styles based on a condition in the `App` component?
> a) By using inline styles only
> b) By changing the CSS file name dynamically
> c) By setting class names conditionally in JSX
> d) By creating multiple CSS files
>> [!success]- Answer
>> c) By setting class names conditionally in JSX

> [!question] Which of the following is a valid `propTypes` definition for the `UserGreeting` component?
> a) `PropTypes.string.isRequired`
> b) `PropTypes.array.isRequired`
> c) `PropTypes.string.optional`
> d) `PropTypes.number.isRequired`
>> [!success]- Answer
>> a) `PropTypes.string.isRequired`

> [!question] How can you ensure that `username` is always passed as a string to the `UserGreeting` component?
> a) By using `PropTypes.string.isRequired`
> b) By using `PropTypes.username`
> c) By passing it as an integer
> d) By defining it as a constant
>> [!success]- Answer
>> a) By using `PropTypes.string.isRequired`

> [!question] What will happen if the `isLoggedIn` prop is missing when rendering the `UserGreeting` component?
> a) A console error will be shown
> b) The component will not render
> c) The component will use the default value set in `defaultProps`
> d) The application will crash
>> [!success]- Answer
>> c) The component will use the default value set in `defaultProps`

> [!question] Which method is NOT recommended for conditional rendering?
> a) Using `if` statements
> b) Using ternary operators
> c) Using constants
> d) Rendering all components and hiding them with CSS
>> [!success]- Answer
>> d) Rendering all components and hiding them with CSS

> [!question] How would you modify the `UserGreeting` component to render a custom message when no username is provided?
> a) Set a default value for `username` in `defaultProps`
> b) Use an `if` statement inside the `App` component
> c) Pass a custom message as a new prop
> d) Replace `props.username` with `props.customMessage`
>> [!success]- Answer
>> a) Set a default value for `username` in `defaultProps`

> [!question] What is the primary role of `propTypes` in a component?
> a) To handle state within the component
> b) To define the structure and type of data passed as props
> c) To automatically apply CSS classes
> d) To set default values for props
>> [!success]- Answer
>> b) To define the structure and type of data passed as props

> [!question] Which CSS class will be applied if `isLoggedIn` is `false` in the `App` component?
> a) `.welcome-message`
> b) `.login-prompt`
> c) `.guest-message`
> d) `.error-message`
>> [!success]- Answer
>> b) `.login-prompt`