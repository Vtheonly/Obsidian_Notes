# Types of Mobile Applications

## Native Application
- Custom-developed using a native language (e.g. Java for Android) and must be adapted to each operating system.
- A different version for each type of phone.
- Functions optimally.

## Web Application
- Designed with HTML and CSS.
- Created to be consulted from a smartphone’s internet browser.
- Accessible from any mobile device.
- Offers less functionality and performance.

## Hybrid Application
- A mobile application that merges the characteristics of the web application (development in HTML) and those of the native application.
- Multiplatform.
- Compared to native applications, hybrid applications are cheaper and quicker to develop but offer less performance.

![Mobile Applications](1.png)

---

# Android Platform Architecture

## Applications
- IM
- Dialer
- SMS/MMS
- Browser
- Camera
- Calculator
- Contacts
- Voice Dial
- Email

## Application Framework
- Activity Manager
- Package Manager
- Content Providers
- Resource Manager
- Surface Manager
- OpenGLIES
- SGL
- Window Manager
- Telephony Manager
- Media Framework
- Calendar
- Media Player
- Albums
- Alarm Clock
- SQLite
- View System
- Location Manager
- Notification Manager

## Android Runtime
- Core Libraries
- Free Type
- SSL
- WebKit
- Dalvik Virtual Machine
- Display Driver
- USB Driver
- Camera Driver
- Keypad Driver
- Bluetooth Driver
- WiFi Driver
- Libc

## Linux Kernel
- Shared Memory Driver
- Audio Driver
- Binder (IPC) Driver
- Power Management

---

# Additional Information

## Applications
- Android comes with a set of basic programs (called native applications) allowing access to features such as emails, SMS, calendar, photos, theWeb…
- These applications are developed using the Java programming language
- For the end user, it is the only accessible and visible layer

## Application Framework
- Offers developers the ability to create extremely rich and innovative applications
- Developers are free to take advantage of hardware, location information, background services, set alarms, add notifications,..

## Libraries
- A set of libraries used by many components of the Android platform.
- Accessible to the developer via the Android framework.
- Examples:
  - Skia: 2D graphics library
  - OpenGL: 3D graphics library
  - SQLite: Application data storage
  - WebKit: Web navigation engine (used in the browser)

## Android Runtime
- DalvikVM:
  - Provides a virtual machine adapted to the limitations of mobile devices.
  - Dalvik allows multiple applications to run simultaneously.
  - It executes bytecode dedicated to it (the .dex bytecode)
  - From Android version 5, Dalvik was replaced by ART (Android RunTime)

## Linux Kernel
- Android is based on a Linux kernel which manages
  - System services, memory, processes, drivers,...
  - Hardware, sensors (camera, GPS, wifi, etc.)
- It acts as an abstraction layer between hardware and software

---

# Structure of an Android Project

## Manifests
- Application description

## Java
- Sources, ordered by package

## Resources
- XML files and images of the interface
  - **Drawable**: Images used in the interface
  - **Layout**: Graphical interfaces
  - **Mipmap**: Icons used in the interface
  - **Values**: Configuration values, texts, etc.

## Gradle Scripts
- Project compilation tool

![[2.png]] 



