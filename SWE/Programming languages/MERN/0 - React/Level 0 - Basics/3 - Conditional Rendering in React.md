
**Conditional rendering** allows you to control what gets rendered in your application based on certain conditions. It enables you to show, hide, or change components dynamically.

### Example: User Greeting Component

1. **Create a Component:**
   - **File:** `UserGreeting.jsx`
   - **Component Type:** Function-based
   - **Export:** Default export for the component

   ```jsx
   function UserGreeting(props) {
     if (props.isLoggedIn) {
       return <h2>Welcome, {props.username}!</h2>;
     } else {
       return <h2>Please log in to continue.</h2>;
     }
   }

   export default UserGreeting;
   ```

2. **Using the Component:**
   - **File:** `App.jsx`
   - Import and use the `UserGreeting` component with `props`.

   ```jsx
   import UserGreeting from './UserGreeting';

   function App() {
     const isLoggedIn = true; // or false
     const username = "Bro Code";

     return (
       <div>
         <UserGreeting isLoggedIn={isLoggedIn} username={username} />
       </div>
     );
   }

   export default App;
   ```

### Conditional Logic Options

1. **Using `if` Statements:**
   ```jsx
   function UserGreeting(props) {
     if (props.isLoggedIn) {
       return <h2>Welcome, {props.username}!</h2>;
     } else {
       return <h2>Please log in to continue.</h2>;
     }
   }
   ```

2. **Using Ternary Operator:**
   ```jsx
   function UserGreeting(props) {
     return props.isLoggedIn
       ? <h2>Welcome, {props.username}!</h2>
       : <h2>Please log in to continue.</h2>;
   }
   ```

3. **Using Constants for Readability:**
   ```jsx
   function UserGreeting(props) {
     const welcomeMessage = <h2>Welcome, {props.username}!</h2>;
     const loginPrompt = <h2>Please log in to continue.</h2>;

     return props.isLoggedIn ? welcomeMessage : loginPrompt;
   }
   ```

### CSS Styling

1. **Apply Styles in `App.jsx`:**
   - Add class names based on conditions.

   ```jsx
   function App() {
     const isLoggedIn = true; // or false
     const username = "Bro Code";

     return (
       <div>
         <UserGreeting 
           isLoggedIn={isLoggedIn} 
           username={username} 
           className={isLoggedIn ? "welcome-message" : "login-prompt"} 
         />
       </div>
     );
   }
   ```

2. **CSS Example:**
   - **File:** `index.css`

   ```css
   .welcome-message {
     font-size: 2.5em;
     background-color: hsl(120, 100%, 50%);
     color: white;
     padding: 10px;
     border-radius: 5px;
   }

   .login-prompt {
     font-size: 2.5em;
     background-color: hsl(0, 100%, 50%);
     color: white;
     padding: 10px;
     border-radius: 5px;
   }
   ```

### Prop Types and Default Props

1. **Set Up Prop Types:**
   - **File:** `UserGreeting.jsx`

   ```jsx
   import PropTypes from 'prop-types';

   UserGreeting.propTypes = {
     isLoggedIn: PropTypes.bool.isRequired,
     username: PropTypes.string.isRequired
   };
   ```

2. **Set Up Default Props:**
   - **File:** `UserGreeting.jsx`

   ```jsx
   UserGreeting.defaultProps = {
     isLoggedIn: false,
     username: 'Guest'
   };
   ```

3. **Testing Default Props:**
   - If `isLoggedIn` is true and `username` is not provided, it will default to "Guest".

### Summary

Conditional rendering is used to display different content based on conditions. It can be achieved using `if` statements, ternary operators, or constants. CSS can be applied dynamically based on conditions, and prop types along with default props help ensure correct usage and provide fallback values.
