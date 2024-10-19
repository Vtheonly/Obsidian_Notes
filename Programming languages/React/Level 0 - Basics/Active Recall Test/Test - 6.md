### React State Update and Re-rendering Quiz

1. **What is the purpose of the `useState` hook in React?**
   - [ ] A) To manage component's lifecycle
   - [x] B) To handle state in functional components
   - [ ] C) To fetch data from APIs
   - [ ] D) To manipulate the DOM directly

2. **In the provided code snippet, what is the role of the function `(count) => count + 1`?**
   - [ ] A) It sets the state to a fixed value
   - [ ] B) It resets the state to the initial value
   - [x] C) It increments the current state value by 1
   - [ ] D) It initializes the state value

3. **What happens when you click the button in the `Counter` component?**
   - [ ] A) The state value is set to 0
   - [ ] B) The state value is decremented by 1
   - [ ] C) The state value is incremented by 1
   - [ ] D) The component is not updated

4. **How does React ensure that the button's text displays the updated `count` value?**
   - [ ] A) By directly manipulating the DOM
   - [ ] B) By using a local variable to store the count
   - [ ] C) By re-rendering the component with the new state
   - [ ] D) By using a separate state management library

5. **What triggers the re-render of the `Counter` component?**
   - [ ] A) The button click
   - [ ] B) A change in props
   - [ ] C) A state update using `setCount`
   - [ ] D) A direct update to the DOM

6. **What will the displayed text in the button be after the first click if the initial state is 0?**
   - [ ] A) `count is 0`
   - [ ] B) `count is 1`
   - [ ] C) `count is -1`
   - [ ] D) `count is NaN`

7. **Which of the following is true about the updater function used with `setCount`?**
   - [ ] A) It directly modifies the `count` variable
   - [ ] B) It calculates and returns a new state based on the current state
   - [ ] C) It does not cause a re-render
   - [ ] D) It initializes the state variable

8. **How does React handle state changes in terms of component updates?**
   - [ ] A) React manually updates the DOM
   - [ ] B) React re-renders the component with the new state
   - [ ] C) React stores state changes in local storage
   - [ ] D) React ignores state changes if they are too frequent

9. **In the `Counter` example, which part of the component updates when the state changes?**
   - [ ] A) Only the `count` variable
   - [ ] B) Only the `button` element
   - [ ] C) The entire component
   - [ ] D) The browser console

10. **What is the default value of the `count` state when using `useState`?**
    - [ ] A) `null`
    - [ ] B) `0`
    - [ ] C) `undefined`
    - [ ] D) `false`

### Answers

1. B) To handle state in functional components
2. C) It increments the current state value by 1
3. C) The state value is incremented by 1
4. C) By re-rendering the component with the new state
5. C) A state update using `setCount`
6. B) `count is 1`
7. B) It calculates and returns a new state based on the current state
8. B) React re-renders the component with the new state
9. C) The entire component
10. B) `0`