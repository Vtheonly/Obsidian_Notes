# Understanding Props in React

### Overview

Props, short for properties, are used to pass data from a parent component to a child component in React. This allows you to make components reusable with different data.

### 1. Basic Usage of Props

1. **Create the Student Component**
   ```jsx
   // src/Student.jsx
   import React from 'react';

   const Student = (props) => {
     return (
       <div className="student">
         <p>Name: {props.name}</p>
         <p>Age: {props.age}</p>
         <p>Student: {props.isStudent ? 'Yes' : 'No'}</p>
       </div>
     );
   };

   export default Student;
   ```

2. **Use the Student Component in App**
   ```jsx
   // src/App.jsx
   import React from 'react';
   import Student from './Student';

   const App = () => {
     return (
       <div>
         <Student name="SpongeBob" age={30} isStudent={true} />
         <Student name="Patrick" age={42} isStudent={false} />
         <Student name="Squidward" age={50} isStudent={false} />
         <Student name="Sandy" age={27} isStudent={true} />
       </div>
     );
   };

   export default App;
   ```

### 2. Styling the Student Component

1. **Add CSS for Student Component**
   ```css
   /* src/index.css */
   .student {
     font-family: Arial, sans-serif;
     font-size: 2em;
     padding: 10px;
     border: 1px solid hsl(200, 50%, 50%);
     margin-bottom: 10px;
   }

   .student p {
     margin: 0;
   }
   ```

### 3. Prop Types

Prop Types help validate the type of props passed to a component.

1. **Install Prop Types**
   ```bash
   npm install prop-types
   ```

2. **Define Prop Types in Student Component**
   ```jsx
   // src/Student.jsx
   import React from 'react';
   import PropTypes from 'prop-types';

   const Student = (props) => {
     return (
       <div className="student">
         <p>Name: {props.name}</p>
         <p>Age: {props.age}</p>
         <p>Student: {props.isStudent ? 'Yes' : 'No'}</p>
       </div>
     );
   };

   Student.propTypes = {
     name: PropTypes.string.isRequired,
     age: PropTypes.number.isRequired,
     isStudent: PropTypes.bool.isRequired,
   };

   export default Student;
   ```

### 4. Default Props

Default props provide default values for props if none are provided.

1. **Define Default Props**
   ```jsx
   // src/Student.jsx
   import React from 'react';
   import PropTypes from 'prop-types';

   const Student = (props) => {
     return (
       <div className="student">
         <p>Name: {props.name}</p>
         <p>Age: {props.age}</p>
         <p>Student: {props.isStudent ? 'Yes' : 'No'}</p>
       </div>
     );
   };

   Student.propTypes = {
     name: PropTypes.string.isRequired,
     age: PropTypes.number.isRequired,
     isStudent: PropTypes.bool.isRequired,
   };

   Student.defaultProps = {
     name: 'Guest',
     age: 0,
     isStudent: false,
   };

   export default Student;
   ```

2. **Test Default Props**
   ```jsx
   // src/App.jsx
   import React from 'react';
   import Student from './Student';

   const App = () => {
     return (
       <div>
         <Student />
         <Student name="Larry" />
       </div>
     );
   };

   export default App;
   ```

### Summary

- **Props**: Used to pass data between components. They allow components to be reusable with different data.
- **Prop Types**: Validate the type of data passed to components.
- **Default Props**: Provide default values for props if none are provided.

These features enhance the flexibility and maintainability of your React components.