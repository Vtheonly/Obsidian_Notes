---

marp: true

---

<style>
/* A modern, dark theme to improve readability and prevent content overflow. */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=JetBrains+Mono:wght@400&display=swap');

:root {
  --primary-color: #4fc3f7; /* Light Blue */
  --bg-gradient-start: #2c3e50;
  --bg-gradient-end: #34495e;
  --text-color: #ecf0f1;
  --header-color: #ffffff;
  --code-bg: #282a36;
  --code-border: #44475a;
  --code-text-color: #f8f8f2;
}

section {
  font-family: 'Inter', sans-serif;
  color: var(--text-color);
  padding: 40px 60px;
  font-size: 22px;
  line-height: 1.5;
  position: relative;
  background-repeat: repeat, no-repeat;
  background-size: auto, cover;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  color: var(--header-color);
  text-align: left;
  margin-block-start: 0;
  margin-block-end: 0.6em;
  text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
  width: 100%;
}

h1 { font-size: 2.2em; padding-bottom: 0.3em; border-bottom: 3px solid var(--primary-color); }
h2 { font-size: 1.8em; }
h3 { font-size: 1.5em; } /* Added for slide titles */
h4 { font-size: 1.2em; font-weight: bold; color: var(--primary-color); } /* Added for subheadings */

p { margin-bottom: 1em; }
a { color: var(--primary-color); text-decoration: none; }
a:hover { text-decoration: underline; }

ul { list-style: none; padding-left: 0; }
ul li { padding-left: 1.5em; position: relative; margin-bottom: 0.6em; }
ul li::before { content: '»'; color: var(--primary-color); position: absolute; left: 0; font-weight: bold; }

/* Footer Watermark */
section::after {
  content: 'Horizon Algeria';
  position: absolute;
  bottom: 25px;
  left: 60px;
  font-size: 16px;
  font-weight: 400;
  color: #fff;
  opacity: 0.35;
  font-family: 'JetBrains Mono', monospace;
}

/* Background Patterns */
section:nth-of-type(4n+1) { --pattern-color: rgba(255, 255, 255, 0.04); background-image: repeating-linear-gradient(45deg, var(--pattern-color) 0, var(--pattern-color) 2px, transparent 0, transparent 50%), linear-gradient(135deg, var(--bg-gradient-start), var(--bg-gradient-end)); background-size: 40px 40px, cover; }
section:nth-of-type(4n+2) { --pattern-color: rgba(255, 255, 255, 0.05); background-image: repeating-conic-gradient(var(--pattern-color) 0% 25%, transparent 0% 50%), linear-gradient(135deg, var(--bg-gradient-start), var(--bg-gradient-end)); background-size: 50px 50px, cover; }
section:nth-of-type(4n+3) { --pattern-color: rgba(255, 255, 255, 0.03); background-image: repeating-linear-gradient(45deg, var(--pattern-color) 25%, transparent 25%, transparent 75%, var(--pattern-color) 75%, var(--pattern-color)), repeating-linear-gradient(-45deg, var(--pattern-color) 25%, transparent 25%, transparent 75%, var(--pattern-color) 75%, var(--pattern-color)), linear-gradient(135deg, var(--bg-gradient-start), var(--bg-gradient-end)); background-size: 35px 35px, 35px 35px, cover; }
section:nth-of-type(4n+4) { --pattern-color: rgba(255, 255, 255, 0.07); background-image: radial-gradient(circle at 1px 1px, var(--pattern-color) 1px, transparent 0), linear-gradient(135deg, var(--bg-gradient-start), var(--bg-gradient-end)); background-size: 25px 25px, cover; }

/* Special Title Slide Pattern */
section:first-of-type {
    background-image: repeating-conic-gradient(from 30deg, #4fc3f711 0% 10%, transparent 10% 40%, #ffffff11 40% 50%), linear-gradient(135deg, var(--bg-gradient-start), var(--bg-gradient-end));
    background-size: 90px 90px, cover;
}
section:first-of-type::after { opacity: 0.5; }

/* --- TWO-COLUMN LAYOUT STYLES --- */
.columns { display: flex; align-items: center; gap: 40px; width: 100%; height: 100%; margin-top: 20px; }
.columns .text { flex: 7; font-size: 1.05em; line-height: 1.6; }
.columns .image { flex: 3; display: flex; align-items: center; justify-content: center; }
.columns .image img { max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.25); }

/* --- STANDARD LAYOUT STYLES --- */
.standard-layout ul li { font-size: 0.95em; } /* Slightly smaller text for list-heavy slides */

</style>

---

# Extended Slide Deck for 1-Hour Intro to Web Development

### Introduction to Web Development & Coding Essentials

### Why the Web is the Best Place to Start Coding

---

### Why Learn Coding?

Web development is one of the most accessible and practical ways to begin learning programming.

Starting with the web gives you a strong foundation because:
- The skills you learn are transferable to many other areas of technology.

---

### Why Learn Coding? (Part 2)

Many successful desktop and mobile apps actually began as simple websites.

A website can be launched from anywhere, making it an easy and affordable entry point into software development.

---

### Why Learn Coding? (Part 3)

Unlike desktop or mobile apps—which often require specialized tools, platforms, or distribution—web development allows you to start small and see immediate results.

You can build something, test it instantly, and share it with others in just a few steps.

---

### Why Learn Coding? (Part 4)

- This immediate feedback creates motivation, helps you understand coding concepts faster, and gives you a sense of achievement early on.
- Over time, these skills can open doors to different career paths: starting your own projects, working for companies, or contributing to larger applications.
- By starting here, you set yourself up to expand confidently into more advanced fields—whether backend systems, mobile development, or even artificial intelligence.

---

### Why Start with Web Development?

- Accessible: needs only a browser.
- Instant feedback.
- Websites are universal.
- Foundation for future tech.

---

### Web Developer Jobs and Salaries in Algeria

- **Roles:** frontend, backend, full-stack, freelance.
- **Demand:** growing need in startups, agencies, and freelancing markets.
- **Salary ranges in Algeria (approximate 2025 data):**
  - Entry-level: 40,000 – 70,000 DZD/month.
  - Mid-level: 80,000 – 150,000 DZD/month.
  - Senior & freelance remote work: 150,000 – 300,000+ DZD/month.
- Global demand = opportunities to work remotely for foreign companies.

---

### What is programming, and programming languages?
#### Programming is giving instructions to a computer.
#### A programming language is the tool we use to write those instructions.

### Why are there so many languages?
#### Because none of them are perfect.
#### Each language is built for different needs and problems.

---

### Keep in mind: you will not learn all of them

#### There are 20+ coding languages in demand today (not counting libraries).
#### Some are more wanted than others, depending on the market.
#### You often sacrifice either depth (quality) or breadth (quantity) in what you learn.

---

### Frontend vs Backend in Web Development

In general, programming languages in web development are often split into two sides:
**frontend development languages** and **backend development languages**.

Each side has many languages, libraries, and frameworks.
Each comes with its own benefits, trade-offs, and communities.
There is no single "best" solution that works for everything.

---

### Frontend (Client-Side)

In web development, the main frontend languages are:
- **HTML, CSS, and JavaScript**

Along with libraries and frameworks like:
- React, Bootstrap, Sass, Tailwind

These all work directly in the **browser** (the client side).
We’ll talk more about the difference between client-side and server-side in a moment — but for now, remember:
**frontend = what the user sees and interacts with in the browser.**

---

### Backend (Server-Side)

For the backend, there are usually more choices.
Almost any language could be used at some point:
- PHP, SQL, Python, Java, even C or C++ in the past.

Some languages or frameworks are better for **speed**, some for **security**, and some balance both — but always with trade-offs.

The backend is about what happens **behind the scenes**: storing data, handling logic, and serving the right content to the user.

---

### What Does “Coding” Mean?

When we say *coding*, we mean:
- Writing instructions in a programming language (syntax) inside files.
- Then, another program (like a browser or server) reads and processes those files.
- Finally, it **displays the result** of what you built.

Think of it like **Microsoft Word**:
- You type text, then you style and format it.
- In coding, you write instructions, style things, and then see the result live.

---

### Example

Let’s look at a small example.
Don’t worry about understanding the details — this is just to show how code turns into something visual.

---

### Where Do We Put the Code?

Now that we have a small idea of what code looks like...
the question is: **where do we put this code so it can run?**

---

### What Is a Server?

We use something called a **server**.

Think of a server as a giant computer that is optimized to do one main job:
- Stay awake 24/7
- Respond whenever someone types its address (a URL or IP address)
- Display the content and results of your code

---

### How Do Servers Work?

Servers are designed to handle **thousands of users at the same time**.
They are built for:
- **Speed**
- **Security**
- **Performance**

That’s why they usually come with huge storage capacity, lots of RAM, and powerful CPUs to run your code.
One key feature: **servers are always on** — they don’t shut down.

---

### Why Can’t Servers Turn Off?

If a server is turned off, your website instantly disappears from the internet.
The site exists only while the server is powered and connected.

Servers can run different systems:
- Different versions of **Windows**
- Different versions of **Linux**
- Or other operating systems you configure, depending on your project.

---

### For Beginners

This can sound like a lot. Don’t worry.
For now, it’s best to focus on the **frontend** side.

That way you can learn faster, build visual projects, and understand the basics.
Later, once you’re comfortable, you’ll explore how your own computer can act like a mini-server.

---

# Small Intro into HTML, CSS, and JavaScript

---

### Before We Start Coding

To write code, we need two simple tools:

1. **VS Code** – a code editor that helps us write code better and avoid errors.
2. **A Browser** – I recommend Chrome or Firefox. They’re more than enough.

---

### First Lines of Code

Now that we have VS Code installed and a browser ready, we can write our first lines of code in **HTML**.

But first… what even is HTML?

---

# What Is HTML?

Let’s go through an example to explain it in detail.

---

HTML, in short, is the **skeleton of your website**.

It gives structure and content to whatever you’re building.
It’s old, it’s plain, and honestly—it looks ugly.

But it’s also the most **necessary** thing ever.
Without HTML, you wouldn’t see anything in your browser.

---

### The Structure of a Website

Every website starts here:
- Buttons
- Lists
- Images
- Input fields
- Forms

All of these are defined in HTML.
But at this point, it still looks nothing like Instagram or YouTube.

---

### Making It Look Good – CSS

So how do we make it *look* like a real app?

We use another language: **CSS**.

CSS is all about **style**.
It makes buttons, images, backgrounds, and text look nice.
It’s also what adds animations and polish to a site.

---

### Making It Think – JavaScript

Now we have structure (HTML) and style (CSS).
But a website still needs logic.

That’s where **JavaScript** comes in.

- It’s not Java — it’s **JavaScript**.
- It handles logic, interactions, memory, and checks.
- It’s what validates forms, adds interactivity, and makes your site feel alive — all on the **client side** (in the browser).

---

### A Good Roadmap for Beginners

#### What to Do

- Start with **HTML, CSS, and JavaScript**.
  - With about **1 hour of practice per day**, you can learn the basics in roughly a month.
- If possible, learn the very basics of **GitHub** (just enough to save and share code).
- Use simple tools: **Chrome + VS Code + Live Server** are more than enough.
- Work during the day if you can. Night learning is possible, but not ideal for focus and memory.
- Build small projects as you go — they give you motivation and real results.
- Use AI tools wisely (for help, not to replace learning).

---

### A Good Roadmap for Beginners

#### What Not to Do

- Don’t start with something complex. Keep it **simple and achievable**.
- Don’t waste time learning Figma or other advanced tools at this stage.
- Don’t follow multiple playlists or tutorials at once — **stick to one clear resource**.
- Don’t jump into big projects like “building Spotify” or “cloning Twitter” as your first steps.
- Don’t overload your computer with unnecessary tools.```