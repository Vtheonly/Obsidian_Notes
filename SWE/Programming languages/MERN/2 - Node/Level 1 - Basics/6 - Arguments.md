### Receiving User Input via Command Line Arguments

This tutorial covers how to create a Node.js application that dynamically handles user input through command line arguments and environment variables.

#### Step 1: Setting Up Command Line Arguments

1. **Create `arguments.js` File**
    ```bash
    nano arguments.js
    ```

2. **Add Code to Handle Command Line Arguments**
    ```javascript
    console.log(process.argv);
    ```

3. **Run the Program with Arguments**
    ```bash
    node arguments.js hello world
    ```

   **Output:**
   ```plaintext
   [ '/usr/bin/node',
     '/home/sammy/first-program/arguments.js',
     'hello',
     'world' ]
   ```

   The output shows:
   - The Node.js binary path.
   - The script path.
   - The user-provided arguments.

4. **Filter Out Default Arguments**
    ```javascript
    console.log(process.argv.slice(2));
    ```

5. **Run the Program Again**
    ```bash
    node arguments.js hello world
    ```

   **Output:**
   ```plaintext
   [ 'hello', 'world' ]
   ```

   Now, only user-provided arguments are displayed.

#### Step 2: Accessing Environment Variables

1. **Create `environment.js` File**
    ```bash
    nano environment.js
    ```

2. **Add Code to Display Environment Variables**
    ```javascript
    console.log(process.env);
    ```

3. **Run the Program**
    ```bash
    node environment.js
    ```

   **Output:** (Example)
   ```plaintext
   {
     SHELL: '/bin/bash',
     SESSION_MANAGER: 'local/digitalocean:@/tmp/.ICE-unix/1003,unix/digitalocean:/tmp/.ICE-unix/1003',
     ...
     HOME: '/home/sammy',
     USERNAME: 'sammy',
     ...
   }
   ```

4. **Access Specific Environment Variable**
    ```javascript
    console.log(process.env["HOME"]);
    ```

5. **Run the Program Again**
    ```bash
    node environment.js
    ```

   **Output:**
   ```plaintext
   /home/sammy
   ```

   Now, only the `HOME` environment variable is displayed.

#### Step 3: Retrieving Environment Variables from Command Line Input

1. **Create `echo.js` File**
    ```bash
    nano echo.js
    ```

2. **Add Code to Handle User Input for Environment Variables**
    ```javascript
    const args = process.argv.slice(2);
    console.log(process.env[args[0]]);
    ```

3. **Run the Program with an Argument**
    ```bash
    node echo.js HOME
    ```

   **Output:**
   ```plaintext
   /home/sammy
   ```

   The program prints the value of the specified environment variable.

#### Step 4: Viewing Multiple Environment Variables

1. **Update `echo.js` to Handle Multiple Arguments**
    ```javascript
    const args = process.argv.slice(2);
    args.forEach(arg => {
        console.log(process.env[arg]);
    });
    ```

2. **Run the Program with Multiple Arguments**
    ```bash
    node echo.js HOME PWD
    ```

   **Output:**
   ```plaintext
   /home/sammy
   /home/sammy/first-program
   ```

   Each argument is printed in sequence.

#### Step 5: Handling Undefined Input

1. **Update `echo.js` to Handle Undefined Variables**
    ```javascript
    const args = process.argv.slice(2);
    args.forEach(arg => {
        let envVar = process.env[arg];
        if (envVar === undefined) {
            console.error(`Could not find "${arg}" in environment`);
        } else {
            console.log(envVar);
        }
    });
    ```

2. **Run the Program with an Undefined Variable**
    ```bash
    node echo.js HOME PWD NOT_DEFINED
    ```

   **Output:**
   ```plaintext
   /home/sammy
   /home/sammy/first-program
   Could not find "NOT_DEFINED" in environment
   ```

   This output provides a clear error message for undefined variables.

### Conclusion

You have learned how to:
- Accept command line arguments and environment variables in a Node.js application.
- Display specific or multiple environment variables based on user input.
- Handle cases where the requested environment variables are not defined.

Feel free to enhance this utility further by adding more features or validations.