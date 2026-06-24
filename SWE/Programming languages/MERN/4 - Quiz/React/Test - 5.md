---
sources:
  - "[[useState Hook in React]]"
---
> [!question] What is the purpose of the `useState` hook in React?
> a) To manage the lifecycle of a component
> b) To handle component's state in functional components
> c) To fetch data from an API
> d) To manipulate DOM directly
>> [!success]- Answer
>> b) To handle component's state in functional components

> [!question] How do you initialize state with `useState`?
> a) By passing an object to `useState`
> b) By passing a function to `useState`
> c) By passing a value to `useState`
> d) By using `useEffect` to set the initial state
>> [!success]- Answer
>> c) By passing a value to `useState`

> [!question] In the Counter component example, what does the `increment` function do?
> a) Resets the count to 0
> b) Decreases the count by 1
> c) Increases the count by 1
> d) Does not affect the count
>> [!success]- Answer
>> c) Increases the count by 1

> [!question] How is state updated in the UserForm component?
> a) By directly modifying the `name` and `email` variables
> b) By using `setName` and `setEmail` functions
> c) By calling `handleSubmit`
> d) By submitting the form only
>> [!success]- Answer
>> b) By using `setName` and `setEmail` functions

> [!question] What does the `toggleVisibility` function in the Toggle component do?
> a) Hides the details
> b) Shows the details
> c) Toggles between showing and hiding the details
> d) Updates the state to a fixed value
>> [!success]- Answer
>> c) Toggles between showing and hiding the details

> [!question] In the ItemList component, what does the `addItem` function do?
> a) Removes the last item from the list
> b) Clears the list
> c) Adds a new item to the list
> d) Updates the state with an empty array
>> [!success]- Answer
>> c) Adds a new item to the list

> [!question] What type of state is managed in the `UserProfile` component?
> a) An array of strings
> b) A single string
> c) An object with `name` and `age` properties
> d) A boolean value
>> [!success]- Answer
>> c) An object with `name` and `age` properties

> [!question] How can you update the state based on the previous state in `useState`?
> a) By passing the current state directly to the setter function
> b) By using the `useEffect` hook
> c) By passing a function to the setter function
> d) By using `useReducer`
>> [!success]- Answer
>> c) By passing a function to the setter function

> [!question] What will the `UserForm` component display after the form is submitted?
> a) An alert with the values of `name` and `email`
> b) The form will reset
> c) The form values will be cleared
> d) A new form will be rendered
>> [!success]- Answer
>> a) An alert with the values of `name` and `email`

> [!question] What is the initial state value in the Counter component?
> a) 1
> b) 0
> c) -1
> d) null
>> [!success]- Answer
>> b) 0

> [!question] How does `useState` handle complex state, such as objects or arrays?
> a) By using multiple `useState` calls for different parts of the object or array
> b) By creating new state variables
> c) By passing the entire object or array to the setter function
> d) By combining `useState` with `useEffect`
>> [!success]- Answer
>> a) By using multiple `useState` calls for different parts of the object or array

> [!question] In the `ItemList` example, what does the `map` function do?
> a) Adds new items to the list
> b) Updates the list in place
> c) Renders each item in the list as a `<li>` element
> d) Clears the list
>> [!success]- Answer
>> c) Renders each item in the list as a `<li>` element

> [!question] What will be the result of clicking the button in the `Toggle` component if `isVisible` is `true`?
> a) The details will be hidden
> b) The details will be shown
> c) The `isVisible` state will be reset to `false`
> d) An alert will be shown
>> [!success]- Answer
>> a) The details will be hidden

> [!question] Why is it important to use the setter function returned by `useState`?
> a) To directly modify the state variable
> b) To ensure the component re-renders with the updated state
> c) To handle state changes with side effects
> d) To avoid using `useEffect`
>> [!success]- Answer
>> b) To ensure the component re-renders with the updated state

> [!question] What will the `UserProfile` component display after clicking the "Update Profile" button?
> a) A form to update the profile
> b) The updated `name` and `age` values
> c) An alert with the new profile information
> d) An error message
>> [!success]- Answer
>> b) The updated `name` and `age` values