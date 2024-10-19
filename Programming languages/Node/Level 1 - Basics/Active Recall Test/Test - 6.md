Here’s an extended quiz with 15 questions based on the tutorial:

### Quiz: Command Line Arguments and Environment Variables in Node.js

**Question 1: What method is used to access command line arguments in Node.js?**
- [ ] A) `console.argv`
- [ ] B) `process.argv`
- [ ] C) `system.argv`
- [ ] D) `node.argv`


**Question 2: What is included in the `process.argv` array by default?**
- [ ] A) Node.js version and system environment
- [ ] B) The path to the node binary and the script file
- [ ] C) Only user-provided arguments
- [ ] D) Environment variables


**Question 3: What does the `process.argv.slice(2)` method do?**
- [ ] A) Removes the first three elements from the array
- [ ] B) Removes default arguments and retains user inputs
- [ ] C) Displays all environment variables
- [ ] D) Filters out environment variables


**Question 4: What will be the output of this code when run as `node script.js foo bar`?**
   ```javascript
   console.log(process.argv.slice(2));
   ```
- [ ] A) `[ '/usr/bin/node', '/home/user/script.js' ]`
- [ ] B) `[ 'foo', 'bar' ]`
- [ ] C) `[ 'foo' ]`
- [ ] D) `[ 'bar' ]`


**Question 5: Which method is used to access environment variables in Node.js?**
- [ ] A) `process.env`
- [ ] B) `env.process`
- [ ] C) `env.system`
- [ ] D) `process.system`


**Question 6: What happens if you try to access a non-existent environment variable?**
- [ ] A) It throws an error
- [ ] B) It returns an empty string
- [ ] C) It returns `undefined`
- [ ] D) It returns `null`


**Question 7: How would you print the value of the `HOME` environment variable in Node.js?**
- [ ] A) `console.log(process.env["HOME"]);`
- [ ] B) `console.log(env["HOME"]);`
- [ ] C) `console.log(process.env.HOME);`
- [ ] D) Both A and C


**Question 8: If you want to retrieve multiple environment variables at once, which approach is correct?**
- [ ] A) `process.env.getVariables(['HOME', 'USER'])`
- [ ] B) `args.forEach(arg => console.log(process.env[arg]));`
- [ ] C) `process.getVariables()`
- [ ] D) `console.log(process.argv);`


**Question 9: What will be the output of this code when run as `node echo.js HOME PWD`?**
   ```javascript
   const args = process.argv.slice(2);
   args.forEach(arg => {
       console.log(process.env[arg]);
   });
   ```
- [ ] A) `/home/user /home/user/first-program`
- [ ] B) The full list of environment variables
- [ ] C) `[ 'HOME', 'PWD' ]`
- [ ] D) `/home/user`


**Question 10: How can you check if an environment variable is undefined in a Node.js script?**
- [ ] A) Using a try-catch block
- [ ] B) Using an `if` statement: `if (envVar === undefined)`
- [ ] C) Using `if (envVar == null)`
- [ ] D) Using `if (envVar.empty)`


**Question 11: What will be the output when running `node echo.js HOME NOT_DEFINED` and using the following code?**
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
- [ ] A) `/home/user /home/user/first-program`
- [ ] B) `/home/user Could not find "NOT_DEFINED" in environment`
- [ ] C) `[ 'HOME', 'NOT_DEFINED' ]`
- [ ] D) Throws an error for undefined environment variable


**Question 12: Which of the following best describes the output of `console.log(process.env);`?**
- [ ] A) It prints only user-defined environment variables
- [ ] B) It prints all system and user environment variables
- [ ] C) It prints command line arguments
- [ ] D) It prints Node.js binary path and script path


**Question 13: In what format does `process.env` return environment variables?**
- [ ] A) As an array
- [ ] B) As an object
- [ ] C) As a string
- [ ] D) As a set


**Question 14: If you need to access command line arguments excluding the default ones, how would you structure your code?**
- [ ] A) `process.argv.slice(2)`
- [ ] B) `process.env`
- [ ] C) `process.slice(2)`
- [ ] D) `console.argv.slice(2)`


**Question 15: What is the correct way to handle errors for undefined command line arguments or environment variables?**
- [ ] A) `try-catch` block
- [ ] B) Check if the variable is `null`
- [ ] C) Check if the variable is `undefined`
- [ ] D) Handle undefined input with a default value


---

**Answers**
1. B  
2. B  
3. B  
4. B  
5. A  
6. C  
7. D  
8. B  
9. A  
10. B  
11. B  
12. B  
13. B  
14. A  
15. C  