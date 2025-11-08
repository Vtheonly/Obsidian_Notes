# The Structure of the Cloud

**DataCenter**: it's the main and the brain for the whole thing. It mainly does the heavy lifting when it comes to computing and doing the non-"where to" operations, and is more about "what to do". It has a lot of hosts of VMs and also handles the resource allocation (how much power for a said task).

**Virtual Machine (VM)**: this is the down-bottom single block unit that runs one or more tasks. This is kinda where the whole dynamic movement and circulation of computation is. A data center is made up of a lot of VMs connected to it; it manages them, but the one that is more like a single neuron is the VM. A VM can do more than one task.

**Broker**: this one does what its name says; it's like a manager (nothing like a scheduler). He basically tells who (which VM) does what (the task) because a single VM is not all the time empty, not all the time closed, and not all the time able to handle the said task. Some are big and some need more than one VM to do that, so a broker is the one who hires/solidifies the needed VM to do what needs to be done.

**Scheduler**: a scheduler, on the other hand, does in fact do a bit of management, but he tells which one goes first and which goes when, while the broker decides which goes where. It kinda does exactly what it does in a normal CPU but now does it on a larger scale with higher frequency and higher parallelism.


## Limitations of  IaaS

| **Aspect**           | **Limitation**                                                | **Impact**                                             |
| -------------------- | ------------------------------------------------------------- | ------------------------------------------------------ |
| **Latency**          | DataCenter centralization increases request round-trip times. | Poor performance for globally distributed users.       |
| **Scalability**      | Manual provisioning of VMs and resources.                     | Difficult to adapt dynamically to traffic spikes.      |
| **Load Balancing**   | Limited scheduling logic and no auto-scaling features.        | Risk of overloaded nodes and inefficient resource use. |
| **Fault Tolerance**  | Failure recovery handled manually.                            | Increased downtime and complexity.                     |
| **Maintenance Cost** | High operational management (VMs, OS updates, etc.).          | Reduced agility and developer productivity.            |


### **The Problem with Just Renting Computers (Pure IaaS)**

1. **You do the whole thing.**  
    So you've got your empty building (the VM). Now YOU have to go out and buy the oven, install the plumbing, set up the cash register, get the phone line working... as in you have to install Windows or Linux, make sure you don't get hacked, install all the code libraries, set up the server... buy the whole thing and do the whole thing and it may or may not work depending on your skill set as a software engineer.
    
2. **The Workload Problem.**  
    Your "computer" is running okay with a normal load. But what happens when the workload peaks suddenly or the task takes more than expected, or many requests happen at a continuous time and you fulfill all the requests? If you get a sudden rush of users, your one "computer" gets overwhelmed. Getting another one ready takes time—you have to configure a few things here and there, wait for it to start up, and do all that all over again.
    
3. **Distance.**  
    Let's say your website is hosted on a server in Algeria (terrible choice by the way), like a flight or an airport website. The people in Algeria can view the website at a "good enough" speed, but the people in Egypt or Japan, not so much, because their requests need to go across countries or even the other side of the planet to get to the server in Algeria. By doing your work in one point, that one point is where all the traffic needs to go no matter how far it is and how long it takes, so you get latency depending on where you are at.
    
4. **Paying for 10 and you use just 1.**  
    Let's say you make a streaming website, something that's likely expected to take a giant workload, right? So you get a big component server or maybe even 10. Now you have a lot of resources that can handle the peak times and rush, and performance is no longer an issue for you. But now you're wasting it because most of the time you only use a fraction of it. It's a fact that at some point you will use full potential, but most of the time that whole computing resource is just doing nothing, waiting. And you cannot turn them off and on partially to lower the cost (and if you can, you might risk the startup time taking too long to boot up).
    

renting the IaaS gives you total control, but you end up doing all the boring, hard work yourself, you can't react to surprises very fast, you annoy your faraway customers, and you probably end up paying for a bunch of stuff you don't need.


### PaaS Solutions 

| PaaS Solution | Ease of Deployment | Autoscaling | Pricing | Microservice Compatibility |
| :--- | :--- | :--- | :--- | :--- |
| **Render** | Super easy. Connect your GitHub account and it deploys automatically. | Yes on paid plans. Simple to set up, scales based on CPU and RAM. | Free plan available. A basic web server starts at 7 dollars a month. Very predictable. | Excellent. You can define all your services like web, workers, database in one render.yaml file. |
| **Heroku** | The original easy one. The classic git push heroku main command. | Yes you scale the number of dynos or servers. It's simple but can get expensive fast. | Free plan is very limited now. A basic server dyno also starts around 7 dollars a month. | Good. You usually run each microservice as its own separate app and connect them. |
| **GCP App Engine** | A bit more work. You need to use Google Cloud tools and an app.yaml config file. | The best and most powerful. Can scale automatically from 0 instances up to thousands. | Pay for exactly what you use. Can be very cheap almost 0 dollars for low traffic, but the bill can be confusing. | Excellent. It's designed from the ground up to run multiple services inside one application. |
| **Vercel** | Also super easy just connect GitHub. It's famous for being fast for websites. | It's serverless so it scales automatically for every single user request. You don't manage servers at all. | Generous free plan. The Pro plan is 20 dollars a month per user, plus you pay for heavy usage. | Very good, especially for the front-end part of a system. Perfect for the AADL website itself. |

# Case Study to the AADL "App"

I am designing the **~~New~~ Better AADL Application Platform** the official government website for citizens to apply for housing.

- A user must complete do these:
    
    1. Filling in a form with their personal information.
        
    2. Taking a picture of their national ID card
        
    3. and uploading it.
        
    4. The system uses an **OCR Engine** to automatically read the ID card.
        
    5. The system **verifies** if the name and ID number from the card match the information the user typed in the form.
        
    6. The user uploads other required **PDF documents**.
        
    7. The user finally **submits** the complete application file.
        

The goal is make this smooth, fast, and not crash under load.

A single server trying to do all this would be ~~a disaster~~ slow and I need a better approach.

**Layer IaaS**

- It's where the heavy and secret work gets done on powerful machines that we control completely. We'll use **AWS Amazon ** because we need total control for security and the raw power for the heavy OCR work.
    
- **What goes here:**
    
    - **The OCR Engine:** When the user uploads a picture of their ID, it gets sent here. This is a powerful VM whose only job is to run the complex OCR software that reads the text from the image
        
    - **The Verification Logic:** After the OCR gets the text, another process here compares it against the main database and the user's input
        
    - **The Main Citizen Database:** The central database holding all the official application data. It's the system's brain
        

OCR and data verification are specialized, heavy computations. They need a powerful, dedicated environment. And the citizen database is too sensitive; it must be in our most secure, controlled space, away from the public

▪ **Layer PaaS**

- **What it is:** This is the "reception". It's the actual website the user interacts with, designed to be fast. We'll use **Vercel** because it's built to be super fast for users and it automatically scales up when lots of people apply at once.
    
- **What goes here:**
    
    - **The AADL Website and Forms:** The entire user interface. This is what shows the input fields, the upload file buttons and the submit button
        
    - **The Application's "Conectrctoor" (API):** This is when the user uploads an ID picture, this PaaS application catches the file then sends it to the IaaS "engine room" for OCR, and shows a "Processing, please wait..." message and when the OCR is done the IaaS layer tells the PaaS
        

PAAS layer is all about ux. It needs to be fast and handle many users at once without slowing down. The PaaS takes care of this automatically. The user feels like they are interacting with a quick, modern website


![[Pasted image 20251022232036.png]]