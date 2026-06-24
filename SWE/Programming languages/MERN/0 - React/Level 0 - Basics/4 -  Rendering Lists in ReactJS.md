### Rendering Lists in ReactJS

In this tutorial, we will explore how to render lists in ReactJS, starting from a basic example and moving towards more advanced concepts. We will cover creating a component to display a list, handling arrays of objects, sorting and filtering data, and making the component reusable.

#### 1. **Creating the List Component**

1. **Create a New File**
   - Navigate to the `src` folder.
   - Create a new file named `List.jsx`.

2. **Define the Component**
   - Create a function-based component named `List`.
   - Export the component by default.
   ```jsx
   // src/List.jsx
   import React from 'react';

   function List() {
     return (
       <div>
         {/* Content will go here */}
       </div>
     );
   }

   export default List;
   ```

3. **Render an Array of Strings**
   - Create an array of fruits in the `List` component.
   - Return this array within the `List` component.
   ```jsx
   function List() {
     const fruits = ['Apple', 'Orange', 'Banana', 'Coconut', 'Pineapple'];
     return (
       <ul>
         {fruits.map(fruit => (
           <li key={fruit}>{fruit}</li>
         ))}
       </ul>
     );
   }
   ```

4. **Using the Component**
   - Import the `List` component into the `App` component.
   - Render the `List` component in the `App` component.
   ```jsx
   // src/App.jsx
   import React from 'react';
   import List from './List';

   function App() {
     return (
       <div>
         <List />
       </div>
     );
   }

   export default App;
   ```

#### 2. **Rendering Arrays of Objects**

1. **Modify the Array**
   - Change the array to hold objects with `name` and `calories` properties.
   ```jsx
   function List() {
     const fruits = [
       { name: 'Apple', calories: 95 },
       { name: 'Orange', calories: 45 },
       { name: 'Banana', calories: 105 },
       { name: 'Coconut', calories: 159 },
       { name: 'Pineapple', calories: 37 }
     ];
     return (
       <ul>
         {fruits.map(fruit => (
           <li key={fruit.name}>
             {fruit.name}: <strong>{fruit.calories}</strong> calories
           </li>
         ))}
       </ul>
     );
   }
   ```

2. **Handling Unique Keys**
   - Use a unique `key` for each list item to avoid warnings.
   - If using names as keys, ensure they are unique or use an ID if available.

3. **Sorting and Filtering Data**
   - Sort the fruits array by name or calories.
   - Filter fruits based on calorie count.
   ```jsx
   function List() {
     const fruits = [
       { name: 'Apple', calories: 95 },
       { name: 'Orange', calories: 45 },
       { name: 'Banana', calories: 105 },
       { name: 'Coconut', calories: 159 },
       { name: 'Pineapple', calories: 37 }
     ];

     // Sort by name
     fruits.sort((a, b) => a.name.localeCompare(b.name));

     // Filter low calorie fruits
     const lowCalFruits = fruits.filter(fruit => fruit.calories < 100);

     return (
       <ul>
         {lowCalFruits.map(fruit => (
           <li key={fruit.name}>
             {fruit.name}: <strong>{fruit.calories}</strong> calories
           </li>
         ))}
       </ul>
     );
   }
   ```

#### 3. **Making the Component Reusable**

1. **Passing Props**
   - Modify the `List` component to accept `items` and `category` as props.
   ```jsx
   function List(props) {
     const { items, category } = props;

     return (
       <>
         {category && <h3>{category}</h3>}
         <ul>
           {items.map(item => (
             <li key={item.id}>
               {item.name}: <strong>{item.calories}</strong> calories
             </li>
           ))}
         </ul>
       </>
     );
   }
   ```

2. **Using the Component with Props**
   - Pass `items` and `category` from the `App` component.
   ```jsx
   // src/App.jsx
   import React from 'react';
   import List from './List';

   function App() {
     const fruits = [
       { id: 1, name: 'Apple', calories: 95 },
       { id: 2, name: 'Orange', calories: 45 },
       { id: 3, name: 'Banana', calories: 105 },
       { id: 4, name: 'Coconut', calories: 159 },
       { id: 5, name: 'Pineapple', calories: 37 }
     ];

     const vegetables = [
       { id: 6, name: 'Potatoes', calories: 110 },
       { id: 7, name: 'Celery', calories: 15 },
       { id: 8, name: 'Carrots', calories: 25 },
       { id: 9, name: 'Corn', calories: 63 },
       { id: 10, name: 'Broccoli', calories: 50 }
     ];

     return (
       <div>
         <List items={fruits} category="Fruits" />
         <List items={vegetables} category="Vegetables" />
       </div>
     );
   }

   export default App;
   ```

#### 4. **Adding CSS Styling**

1. **Define CSS Classes**
   - Add styles for the category and list items in `index.css`.
   ```css
   /* index.css */
   .list-category {
     font-size: 2.5em;
     font-weight: bold;
     color: hsl(185, 100%, 50%);
     margin-bottom: 10px;
     text-align: center;
     border: 3px solid hsl(185, 100%, 50%);
     border-radius: 5px;
     background-color: hsl(185, 100%, 90%);
   }

   .list-items {
     font-size: 2em;
     list-style: none;
     color: hsl(200, 50%, 25%);
     text-align: center;
     margin: 0;
   }

   .list-items li:hover {
     background-color: hsl(200, 50%, 45%);
     cursor: pointer;
   }
   ```

#### 5. **Handling Empty Lists and Default Props**

1. **Conditional Rendering**
   - Render the list only if it has items.
   ```jsx
   function List(props) {
     const { items, category } = props;

     if (!items.length) return null;

     return (
       <>
         {category && <h3>{category}</h3>}
         <ul>
           {items.map(item => (
             <li key={item.id}>
               {item.name}: <strong>{item.calories}</strong> calories
             </li>
           ))}
         </ul>
       </>
     );
   }
   ```

2. **Default Props**
   - Set default props for `category` and `items`.
   ```jsx
   List.defaultProps = {
     category: 'Category',
     items: []
   };
   ```

3. **Prop Types**
   - Validate prop types using `prop-types`.
   ```jsx
   import PropTypes from 'prop-types';

   List.propTypes = {
     category: PropTypes.string,
     items: PropTypes.arrayOf(
       PropTypes.shape({
         id: PropTypes.number.isRequired,
         name: PropTypes.string.isRequired,
         calories: PropTypes.number.isRequired
       })
     ).isRequired
   };
   ```

By following these steps, you will have a reusable and styled list component in ReactJS, capable of handling different types of data and ensuring proper rendering even when data is missing or incorrect.