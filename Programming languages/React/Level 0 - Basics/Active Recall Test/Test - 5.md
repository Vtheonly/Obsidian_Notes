### `useState` Hook in React Quiz

1. **What is the purpose of the `useState` hook in React?**
   - [ ] A) To manage the lifecycle of a component
   - [ ] B) To handle component's state in functional components
   - [ ] C) To fetch data from an API
   - [ ] D) To manipulate DOM directly

2. **How do you initialize state with `useState`?**
   - [ ] A) By passing an object to `useState`
   - [ ] B) By passing a function to `useState`
   - [ ] C) By passing a value to `useState`
   - [ ] D) By using `useEffect` to set the initial state

3. **In the Counter component example, what does the `increment` function do?**
   - [ ] A) Resets the count to 0
   - [ ] B) Decreases the count by 1
   - [ ] C) Increases the count by 1
   - [ ] D) Does not affect the count

4. **How is state updated in the UserForm component?**
   - [ ] A) By directly modifying the `name` and `email` variables
   - [ ] B) By using `setName` and `setEmail` functions
   - [ ] C) By calling `handleSubmit`
   - [ ] D) By submitting the form only

5. **What does the `toggleVisibility` function in the Toggle component do?**
   - [ ] A) Hides the details
   - [ ] B) Shows the details
   - [ ] C) Toggles between showing and hiding the details
   - [ ] D) Updates the state to a fixed value

6. **In the ItemList component, what does the `addItem` function do?**
   - [ ] A) Removes the last item from the list
   - [ ] B) Clears the list
   - [ ] C) Adds a new item to the list
   - [ ] D) Updates the state with an empty array

7. **What type of state is managed in the `UserProfile` component?**
   - [ ] A) An array of strings
   - [ ] B) A single string
   - [ ] C) An object with `name` and `age` properties
   - [ ] D) A boolean value

8. **How can you update the state based on the previous state in `useState`?**
   - [ ] A) By passing the current state directly to the setter function
   - [ ] B) By using the `useEffect` hook
   - [ ] C) By passing a function to the setter function
   - [ ] D) By using `useReducer`

9. **What will the `UserForm` component display after the form is submitted?**
   - [ ] A) An alert with the values of `name` and `email`
   - [ ] B) The form will reset
   - [ ] C) The form values will be cleared
   - [ ] D) A new form will be rendered

10. **What is the initial state value in the Counter component?**
    - [ ] A) 1
    - [ ] B) 0
    - [ ] C) -1
    - [ ] D) null

11. **How does `useState` handle complex state, such as objects or arrays?**
    - [ ] A) By using multiple `useState` calls for different parts of the object or array
    - [ ] B) By creating new state variables
    - [ ] C) By passing the entire object or array to the setter function
    - [ ] D) By combining `useState` with `useEffect`

12. **In the `ItemList` example, what does the `map` function do?**
    - [ ] A) Adds new items to the list
    - [ ] B) Updates the list in place
    - [ ] C) Renders each item in the list as a `<li>` element
    - [ ] D) Clears the list

13. **What will be the result of clicking the button in the `Toggle` component if `isVisible` is `true`?**
    - [ ] A) The details will be hidden
    - [ ] B) The details will be shown
    - [ ] C) The `isVisible` state will be reset to `false`
    - [ ] D) An alert will be shown

14. **Why is it important to use the setter function returned by `useState`?**
    - [ ] A) To directly modify the state variable
    - [ ] B) To ensure the component re-renders with the updated state
    - [ ] C) To handle state changes with side effects
    - [ ] D) To avoid using `useEffect`

15. **What will the `UserProfile` component display after clicking the "Update Profile" button?**
    - [ ] A) A form to update the profile
    - [ ] B) The updated `name` and `age` values
    - [ ] C) An alert with the new profile information
    - [ ] D) An error message

### Answers

1. B) To handle component's state in functional components
2. C) By passing a value to `useState`
3. C) Increases the count by 1
4. B) By using `setName` and `setEmail` functions
5. C) Toggles between showing and hiding the details
6. C) Adds a new item to the list
7. C) An object with `name` and `age` properties
8. C) By passing a function to the setter function
9. A) An alert with the values of `name` and `email`
10. B) 0
11. A) By using multiple `useState` calls for different parts of the object or array
12. C) Renders each item in the list as a `<li>` element
13. A) The details will be hidden
14. B) To ensure the component re-renders with the updated state
15. B) The updated `name` and `age` values