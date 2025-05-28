

### 🔍 **Debugging & Inspection**

#### 1. **React Developer Tools** (Browser Extension)

- **What:** Chrome/Firefox DevTools extension to inspect React component trees.
    
- **Why:** View props, state, hooks, and component hierarchy.
    
- **Install:** Search _React Developer Tools_ on Chrome Web Store or Firefox Add-ons.
    
- **Bonus:** Profiler tab helps detect performance bottlenecks.
    

#### 2. **Redux DevTools** (for Redux-based apps)

- **What:** Monitor actions, state changes, and time-travel debugging.
    
- **Install:** Chrome/Firefox extension + optional `redux-devtools-extension` npm package.
    
- **Why:** Great when using Redux or Zustand with middleware.
    

#### 3. **React Error Overlay** (built into Create React App)

- **What:** Automatically shows full-screen error overlays when your app crashes.
    
- **Why:** Instant feedback for runtime errors in dev mode.
    
- **Tip:** Works out of the box with CRA and Vite.
    

---

### 🛠️ **Linting & Type Checking**

#### 4. **ESLint + eslint-plugin-react + eslint-plugin-react-hooks**

- **What:** Powerful linter for catching anti-patterns and enforcing standards.
    
- **Why:** Prevents most common React bugs (like incorrect hooks usage).
    
- **Install:**
    

```bash
npm install eslint eslint-plugin-react eslint-plugin-react-hooks --save-dev
```

#### 5. **TypeScript**

- **What:** Strong typing system for JavaScript.
    
- **Why:** Prevents a huge class of runtime errors and helps with IDE autocompletion.
    
- **Setup:** Convert `.js` files to `.tsx` and install TypeScript:
    

```bash
npm install --save-dev typescript @types/react @types/react-dom
```

#### 6. **Prettier**

- **What:** Code formatter that auto-formats your code consistently.
    
- **Why:** Keeps your React code clean and readable.
    
- **Setup with ESLint:**
    

```bash
npm install --save-dev prettier eslint-config-prettier eslint-plugin-prettier
```

---

### 🔧 **Component/Hook-Level Debugging**

#### 7. **why-did-you-render**

- **What:** Detects unnecessary re-renders.
    
- **Why:** Optimizes performance and exposes wasted renders.
    
- **Install:**
    

```bash
npm install @welldone-software/why-did-you-render --save-dev
```

#### 8. **React Profiler API**

- **What:** Use programmatically to profile individual components.
    
- **When:** Combine with `React.memo`, `useCallback`, `useMemo` optimizations.
    

---

### 🧪 **Testing & Error Reporting**

#### 9. **React Testing Library**

- **What:** Test UI behavior from the user’s perspective.
    
- **Why:** Ensures components work properly without being tightly coupled to implementation.
    
- **Install:**
    

```bash
npm install --save-dev @testing-library/react
```

#### 10. **Sentry / LogRocket**

- **What:** Monitors and logs runtime errors with stack traces.
    
- **Why:** Real-time bug reporting, session recording, and error logging.
    
- **Use for production:** Especially useful for catching bugs you didn’t see in dev.
    

---

### 🧩 **IDE Extensions (VS Code)**

#### 11. **ES7+ React/Redux Snippets**

- **Why:** Auto-generate component/function imports, boilerplate fast.
    
- **Extension ID:** `dsznajder.es7-react-js-snippets`
    

#### 12. **React Native Tools** _(even for React Web debugging)_

- **Features:** Debug JS directly, logs console statements nicely, supports breakpoints.
    

#### 13. **Import Cost**

- **Shows:** File size of each import — helpful for keeping bundle size small.
    

#### 14. **Error Lens**

- **What:** Highlights ESLint or TypeScript errors inline (not just in Problems tab).
    

---

### 🧭 **Code Quality & Architecture Helpers**

#### 15. **Bit.dev**

- **What:** Share and reuse React components across projects.
    
- **Why:** Modularizes UI and promotes better architecture.
    

#### 16. **Storybook**

- **What:** Isolated development environment for components.
    
- **Why:** Test components outside of your app before integrating.
    

#### 17. **React Styleguidist / Docz**

- **Why:** Document reusable components with live preview.
    

---

### ⚙️ Bonus: Boilerplate Generators

#### 18. **Create React App + ESLint + Prettier + TypeScript Template**

- Clone this kind of template for maximum tool integration:
    

```bash
npx create-react-app my-app --template typescript
```

Then add ESLint and Prettier.

---

## 🧠 Tips for Using These Tools Effectively

- Keep **type checking and linting always running** in your editor.
    
- Use the **React DevTools Profiler** once a week to audit re-renders.
    
- Set up **eslint-plugin-jsx-a11y** for accessible React apps.
    
- Use **Sentry** or **LogRocket** in staging environments to catch bugs before release.
    

---

Would you like a preconfigured **starter repo with all these tools** baked in? I can generate a structure and `.eslintrc`, `tsconfig.json`, etc., ready to go.