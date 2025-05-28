---
sources:
  - "[[React State Update and Re-rendering]]"
---
> [!question] What is the purpose of the `useState` hook in React?
> a) To manage component's lifecycle
> b) To handle state in functional components
> c) To fetch data from APIs
> d) To manipulate the DOM directly
>> [!success]- Answer
>> b) To handle state in functional components

> [!question] In the provided code snippet, what is the role of the function `(count) => count + 1`?
> a) It sets the state to a fixed value
> b) It resets the state to the initial value
> c) It increments the current state value by 1
> d) It initializes the state value
>> [!success]- Answer
>> c) It increments the current state value by 1

> [!question] What happens when you click the button in the `Counter` component?
> a) The state value is set to 0
> b) The state value is decremented by 1
> c) The state value is incremented by 1
> d) The component is not updated
>> [!success]- Answer
>> c) The state value is incremented by 1

> [!question] How does React ensure that the button's text displays the updated `count` value?
> a) By directly manipulating the DOM
> b) By using a local variable to store the count
> c) By re-rendering the component with the new state
> d) By using a separate state management library
>> [!success]- Answer
>> c) By re-rendering the component with the new state

> [!question] What triggers the re-render of the `Counter` component?
> a) The button click
> b) A change in props
> c) A state update using `setCount`
> d) A direct update to the DOM
>> [!success]- Answer
>> c) A state update using `setCount`

> [!question] What will the displayed text in the button be after the first click if the initial state is 0?
> a) `count is 0`
> b) `count is 1`
> c) `count is -1`
> d) `count is NaN`
>> [!success]- Answer
>> b) `count is 1`

> [!question] Which of the following is true about the updater function used with `setCount`?
> a) It directly modifies the `count` variable
> b) It calculates and returns a new state based on the current state
> c) It does not cause a re-render
> d) It initializes the state variable
>> [!success]- Answer
>> b) It calculates and returns a new state based on the current state

> [!question] How does React handle state changes in terms of component updates?
> a) React manually updates the DOM
> b) React re-renders the component with the new state
> c) React stores state changes in local storage
> d) React ignores state changes if they are too frequent
>> [!success]- Answer
>> b) React re-renders the component with the new state

> [!question] In the `Counter` example, which part of the component updates when the state changes?
> a) Only the `count` variable
> b) Only the `button` element
> c) The entire component
> d) The browser console
>> [!success]- Answer
>> c) The entire component

> [!question] What is the default value of the `count` state when using `useState`?
> a) `null`
> b) `0`
> c) `undefined`
> d) `false`
>> [!success]- Answer
>> b) `0`