## Docker Core Concepts: Parent Images & Docker Hub

### Introduction
In this lesson, we dive deeper into how **Docker images** are constructed, focusing on the concept of **parent images** and the role of **Docker Hub** in sourcing them. This lesson builds on the previous introduction to images and containers by showing how Docker layers images and uses parent images as the foundation for new custom images.

---

### 1. **Image Layers**
Docker images are built in **layers**, with each layer adding incremental functionality to the image. The **order of layers** is crucial, as Docker reads them from top to bottom, applying changes and dependencies in sequence. Typically, the first layer is a **parent image**, which acts as the base for your custom image.

#### Parent Image
- A **parent image** is usually a pre-existing image that defines a **lightweight operating system** and the **runtime environment** needed for your application.
- For example, a parent image could include a specific version of Node.js (e.g., Node 16 or Node 17) running on a Linux distribution.

Docker provides a vast repository of pre-built parent images through Docker Hub, which we'll explore next.

---

### 2. **Docker Hub**
**Docker Hub** is an online repository (similar to GitHub) where developers can upload, share, and download Docker images. It hosts a large variety of pre-made images for different software stacks, including databases, web servers, and programming language environments. 

#### Searching for Parent Images
If you need a **Node.js** environment, you can search for "node" on Docker Hub to find the official Node image. Docker Hub also provides official images for various technologies such as:
- **MongoDB**
- **MySQL**
- **WordPress**
- **Strapi**

---

### 3. **Pulling Images from Docker Hub**
To use a parent image from Docker Hub in your project, you'll need to **pull** it to your local machine. For example, to pull the Node.js image, you can use the following command in a terminal:
```bash
docker pull node
```
This command downloads the latest version of the Node.js image. If you don't specify a version, Docker automatically pulls the **latest** tag, which corresponds to the latest Node.js release.

#### Tags
**Tags** are used to specify different versions or configurations of an image. For example, the Node.js image has tags for various:
- **Node versions**: e.g., Node 17, Node 16
- **Linux distributions**: e.g., Alpine, Debian

By using tags, you can ensure that your image uses a specific version of Node and a lightweight Linux distribution like **Alpine**.

Example:
```bash
docker pull node:17-alpine
```
This command pulls Node.js version 17 running on the Alpine Linux distribution.

---

### 4. **Using Parent Images**
Once you have pulled a parent image, you can use it as the base layer of your own Docker image. For instance, if you're building a Node.js application, you would start with a **Node parent image**. You can then add additional layers to:
- **Copy your source code** into the image.
- **Install dependencies** using package managers like `npm` or `yarn`.
- **Define commands** to run when the container starts.

---

### 5. **Running the Node Image**
You can run a downloaded Docker image directly by using Docker Desktop or the terminal. For example, after pulling the Node.js image:
1. Go to Docker Hub, find the **Node image**, and click **Run**.
2. The image runs as a **container** with Node.js installed inside it.
3. You can then access an **interactive terminal** inside the container, where you can run Linux commands or execute Node.js code.

Example of using Node in the terminal:
```bash
node
```
This command opens an interactive Node.js session where you can execute JavaScript commands like:
```javascript
5 + 10 // Returns 15
```

---

### 6. **Building Custom Images Using a Parent Image**
The parent image serves as the first layer for your custom images. For example, if you're creating a custom image for a Node.js application:
1. The **first layer** is the parent Node.js image (e.g., `node:17-alpine`).
2. You can then add additional layers to:
   - **Copy your application code** to the image.
   - **Install dependencies** such as npm packages.
   - **Specify commands** (e.g., how to start the Node.js server).

To automate this process, you will use a **Dockerfile**, which we'll cover in the next lesson.

---

### Conclusion
In this lesson, we explored the importance of **parent images** and the role of **Docker Hub** in Docker's ecosystem. Parent images, such as the official Node.js image, provide the foundation for creating custom images. Docker Hub acts as a repository of these images, offering a wide range of pre-built environments for different use cases. In the next lesson, we'll dive into **Dockerfiles** and how to build custom images using parent images.

