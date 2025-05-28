
### **1. Prerequisites**

- **Install Node.js**: If you don’t already have Node.js installed, download it from [Node.js Official Site](https://nodejs.org/) and install it.
    - You can check if Node.js is installed by running:
        
        ```bash
        node -v
        npm -v
        ```
        
        These commands will display the installed version of Node.js and npm (Node Package Manager).

---

### **2. Create a New Node.js Project**

1. Create a new folder for your project:
    
    ```bash
    mkdir my-express-app
    cd my-express-app
    ```
    
2. Initialize a new Node.js project with the following command:
    
    ```bash
    npm init -y
    ```
    
    - This will create a `package.json` file with default configurations.
    - The `package.json` file keeps track of project dependencies like Express.js.

---

### **3. Install Express.js**

Run the following command to install Express.js:

```bash
npm install express
```

- This command downloads and installs the Express package and adds it to the `dependencies` section of your `package.json` file.

---

### **4. Verify Installation**

After installation:

1. Check your `package.json` file. You should see Express listed under the `dependencies`:
    
    ```json
    {
      "dependencies": {
        "express": "^4.18.2"
      }
    }
    ```
    
2. A new folder named `node_modules` will appear in your project directory. It contains the Express library and its dependencies.
    

---

### **5. Create a Simple Express Server**

1. Create a file named `index.js`:
    
    ```bash
    touch index.js
    ```
    
2. Add the following code to `index.js`:
    
    ```javascript
    const express = require('express'); // Import Express
    const app = express(); // Create an Express app
    const port = 3000; // Define the port
    
    // Define a route for the root URL
    app.get('/', (req, res) => {
      res.send('Hello from Express!');
    });
    
    // Start the server
    app.listen(port, () => {
      console.log(`App running at http://localhost:${port}`);
    });
    ```
    
3. Run the Express server:
    
    ```bash
    node index.js
    ```
    
4. Open a browser and visit:
    
    ```
    http://localhost:3000
    ```
    
    You should see the message **"Hello from Express!"**.
    

---

### **6. Common Issues**

- **`command not found: npm`**:
    - Ensure Node.js and npm are properly installed and added to your system's PATH.
- **Permission errors** on Linux/Mac:
    - Use `sudo npm install express` if you encounter permission issues, but it’s better to configure npm to avoid needing `sudo`.

---

That's it! You’ve successfully installed Express.js and created your first Express server. Let me know if you'd like to explore middleware, routing, or API creation next!