This is a *single*, merged Table of Contents that combines the content from both the handwritten notes AND the PDF slides .

do not summarize or anything but later on i will ask you for clarification and i want you to explain things

**Merged Table of Contents - Android Development Course**

**Part 1: Foundations of Android Development**

**Chapter 1: Introduction to Android and Development Environment**

* **1.1 Module Content Overview (PDF)**
    * 1.1.1 Mobile Operating Systems (iOS, WindowsPhone, Android)
    * 1.1.2 Overview of the Android Platform
    * 1.1.3 The Development Environment
    * 1.1.4 Structure and Components of Mobile Applications
    * 1.1.5 Building the User Interface
    * 1.1.6 Use of Resources: XML, Images, Files, etc.
    * 1.1.7 Mobile Programming (JSON, SQLite, etc.)
    * 1.1.8 Deploying a Mobile Application
* **1.2 Introduction to Mobile Operating Systems (PDF)**
    * 1.2.1 Mobile Technologies in Daily Life
    * 1.2.2 Smartphones/Tablets as Small Computers
    * 1.2.3 Popularity of Mobile Operating Systems (Android, iOS, Windows Phone)
    * 1.2.4 Mobile Applications as Essential Services
* **1.3 Smartphones Explained (PDF)**
    * 1.3.1 "Smart Phones" Definition
    * 1.3.2 Touchscreen and Keyboard Options
    * 1.3.3 Functionality Beyond Calling and Messaging (Internet, Email, Multimedia, Games)
    * 1.3.4 Personalization with Applications
* **1.4 Smartphone, Phablette, Tablette - Size Categories (PDF)**
    * 1.4.1 Visual Size Comparison (Diagram)
    * 1.4.2 Smartphones (5-inch and less)
    * 1.4.3 Phablets (Between 5-7 inches)
    * 1.4.4 Tablets (7-inches and above)
* **1.5 What is a Mobile OS? (PDF)**
    * 1.5.1 Platform Controlling Device Features
    * 1.5.2 Definition as Operating System for Mobile Devices
    * 1.5.3 Basic Operations Control (Touchscreen, Bluetooth, Wi-Fi, Camera)
    * 1.5.4 Examples: iOS, Windows Phone, Android, BlackBerryOS, Symbian
* **1.6 Mobile OS Landscape (PDF)**
    * 1.6.1 Android (Google): Developed in 2007, Open Platform in 2008, Free and Open Source, Major Manufacturers Use
    * 1.6.2 iOS (Apple): Derived from Mac OS, Developed in 2007, Used in Apple Devices
    * 1.6.3 Windows Phone (Microsoft): Appeared in 2010, Successor to Windows Mobile, Limited Market Share
* **1.7 Programming Languages for Mobile OS (PDF)**
    * 1.7.1 Android: Java, Kotlin
    * 1.7.2 iOS: Swift
    * 1.7.3 Windows Phone: C#
* **1.8 Global Market Share of Mobile OS (PDF)**
    * 1.8.1 Market Share Charts (Visual Representations - Historical and Recent Data)
* **1.9 Types of Mobile Applications (PDF)**
    * 1.9.1 Native Application: Custom-developed, Native Language (Java/Kotlin for Android), OS-Specific, Optimal Performance
    * 1.9.2 Web Application: HTML and CSS, Accessed via Browser, Cross-Device, Less Functionality
    * 1.9.3 Hybrid Application: Merges Web and Native, HTML Development, Multiplatform, Cheaper/Quicker, Less Performance
    * 1.9.4 Mobile Application Types Diagram (Visual Representation)
* **1.10 Android Development Lifecycle (PDF & Notes)**
    * 1.10.1 Code
    * 1.10.2 Build App
    * 1.10.3 Test
    * 1.10.4 Signing
    * 1.10.5 Deploy
* **1.11 Preliminary Steps for Publishing (PDF & Notes)**
    * 1.11.1 Generate Application (APK File)
    * 1.11.2 Sign Application with Digital Signature
    * 1.11.3 Create Play Store Account and Publish Signed APK
* **1.12 Android Play Store Account Creation (PDF & Notes)**
    * 1.12.1 Essential for Publishing Applications
    * 1.12.2 25$ One-Time Payment
    * 1.12.3 Payment is Per Account, Not Per Application

**Chapter 2: Setting Up the Android Development Environment (PDF)**

* **2.1 Android Studio IDE (PDF)**
    * 2.1.1 Official IDE for Android
    * 2.1.2 Tools for Creating Apps on All Android Devices
    * 2.1.3 Free Availability (Link Provided)
    * 2.1.4 Development Languages: Java, Kotlin, XML
    * 2.1.5 JDK Class Availability (Note on Limited JDK Classes)
* **2.2 Required Configuration for Android Studio (PDF)**
    * 2.2.1 Operating System Requirements (Windows, Ubuntu, macOS)
    * 2.2.2 RAM Recommendations (Minimum and Recommended)
    * 2.2.3 Disk Space Requirements
    * 2.2.4 64-bit OS for Accelerated Emulator
    * 2.2.5 Java Development Kit (JDK) Requirement
* **2.3 Software Development Kit (SDK) (PDF)**
    * 2.3.1 Set of Software Tools for Developers
    * 2.3.2 Facilitates Android Platform Software Development
    * 2.3.3 Android SDK Provides:
        * 2.3.3.1 Java Libraries for Android
        * 2.3.3.2 Images of the Android System
        * 2.3.3.3 Emulator for Testing Applications
* **2.4 Android Virtual Device (AVD) (PDF)**
    * 2.4.1 Allows Launching and Running Applications on Virtual Device
    * 2.4.2 Emulates Android Device Behavior
* **2.5 IDE Installation Steps (PDF)**
    * 2.5.1 Download and Install 64-bit JDK (Uninstall Previous JDK Versions)
    * 2.5.2 Download Android Studio (Contains IDE, SDK, Emulator) - Link Provided
    * 2.5.3 Run Executable and Follow Installation Wizard
* **2.6 Remark on First Launch (PDF)**
    * 2.6.1 IDE Automatically Downloads Necessary Tools (SDK, Gradle)

**Chapter 3: Your First Android Studio Project (PDF)**

* **3.1 Creating a New Project: File/New/New Project (PDF)**
    * 3.1.1 Android Studio New Project Wizard Screenshots (Visual Guide)
* **3.2 Choice of Android Version (PDF)**
    * 3.2.1 Project Configuration Dialog Screenshot (Name, Package Name, Save Location, Language, Minimum SDK)
* **3.3 Result of Project Creation Wizard (PDF)**
    * 3.3.1 Android Studio Project Structure Screenshot
* **3.4 Structure of an Android Project (PDF & Notes)**
    * 3.4.1 `manifests`: Application Description (`AndroidManifest.xml`)
    * 3.4.2 `java`: Sources, Ordered by Package (`MainActivity.java` example)
    * 3.4.3 `ressources`: XML Files and Images of Interface
        * 3.4.3.1 `drawable`: Images Used in Interface (`ic_launcher.png` examples)
        * 3.4.3.2 `layout`: Graphical Interfaces (`activity_main.xml` example)
        * 3.4.3.3 `mipmap`: Icons Used in Interface
        * 3.4.3.4 `values`: Configuration Values, Texts, Styles (`colors.xml`, `dimens.xml`, `strings.xml`, `styles.xml`)
    * 3.4.4 `Gradle Scripts`: Project Compilation Tool
* **3.5 Java Source Code (`MainActivity.java`) (PDF)**
    * 3.5.1 `MainActivity.java` Code Snippet Example
    * 3.5.2 `setContentView` Method Loads Interface on Screen
* **3.6 `AndroidManifest.xml` File (PDF & Notes)**
    * 3.6.1 XML Structure and Content (`AndroidManifest.xml` code example)
    * 3.6.2 `<manifest>` Tag: Root of the File
    * 3.6.3 Android Namespace Declaration
    * 3.6.4 Application Package Declaration
    * 3.6.5 `android:versionCode`: Integer Version Code (Play Store)
    * 3.6.6 `android:versionName`: String Version Name (User Visible)
    * 3.6.7 `<uses-sdk>` Tag: Minimum and Target SDK Versions
    * 3.6.8 `<application>` Tag: Application Attributes (Icon, Label, Theme)
    * 3.6.9 `<activity>` Tag: Activity Declaration (`MainActivity` example)
    * 3.6.10 `<intent-filter>`: Intent Filter for Launcher Activity (Indicates Entry Point)

**Chapter 4: Running Your Android Application (PDF)**

* **4.1 Running the App on a Real Device Connected by USB (PDF)**
    * **4.1.1 Enable Developer Mode on Android Device:**
        * 4.1.1.1 Go to Settings
        * 4.1.1.2 Go to About Device
        * 4.1.1.3 Tap "Build number" 7 times
        * 4.1.1.4 "Developer options" submenu appears in Settings
    * 4.1.2 Android Device Screenshots Showing Developer Options Steps (Visual Guide)
* **4.2 Running the Application on a Virtual Device (AVD) (PDF)**
    * **4.2.1 Creating a Virtual Device:**
        * 4.2.1.1 Android Studio AVD Manager Button (Toolbar)
        * 4.2.1.2 Android Virtual Device Manager Dialog
        * 4.2.1.3 "Create Virtual Device..." Button
    * 4.2.2 Choose a Device Definition (Device Selection Dialog)
    * 4.2.3 Choose the Android OS Version (System Image Selection Dialog)
    * 4.2.4 Verify Configuration and Virtual Device Name (Verify Configuration Dialog)
    * 4.2.5 Advanced Settings in Virtual Device Configuration (Advanced Settings Dialog - Memory, CPU, Camera, Network)
* **4.3 Running the Application (PDF)**
    * 4.3.1 Android Studio "Run" Button (Toolbar)
    * 4.3.2 Select Deployment Target Dialog (Choose Real or Virtual Device)

**Part 2: Building User Interfaces**

**Chapter 5: User Interface Basics and Layouts (Notes & PDF)**

* **5.1 Units of Measurement in Android UI (Notes & PDF)**
    * 5.1.1 Pounces (Inches - *in*)
    * 5.1.2 Millimètre (Millimeters - *mm*)
    * 5.1.3 Points (Points - *pt*)
    * 5.1.4 Pixel à densité indépendante (Density-Independent Pixel - *dp*)
    * 5.1.5 Expressing Units as Strings (e.g., "24.5mm", "65px")
* **5.2 Common Properties of Interface Elements (Notes & PDF)**
    * 5.2.1 Identifier (`android:id`)
        * 5.2.1.1 Purpose of Identifiers
        * 5.2.1.2 XML Example: `android:id="@+id/mon_ident"`
        * 5.2.1.3 Java Retrieval: `findViewById(R.id.mon_ident)`
    * 5.2.2 Size (`android:layout_width`, `android:layout_height`)
        * 5.2.2.1 Fixed Size (e.g., "50px")
        * 5.2.2.2 `match_parent`
        * 5.2.2.3 `wrap_content`
    * 5.2.3 Gravity (`android:gravity`)
        * 5.2.3.1 `center_horizontal`, `center_vertical`, `top`, `bottom`, `left`, `right`
        * 5.2.3.2 Combining Values with `|` (e.g., "top|left")
    * 5.2.4 Text (`android:text`)
        * 5.2.4.1 Adding Text to UI Elements
        * 5.2.4.2 Example: `android:text="Cancel"`
    * 5.2.5 Spacing (`android:padding`, `android:layout_margin`)
        * 5.2.5.1 `android:padding` (Internal Margins)
        * 5.2.5.2 `android:layout_margin` (External Margins)
        * 5.2.5.3 Side-Specific Spacing (`paddingLeft`, `layout_marginLeft`, etc.)
* **5.3 Layout Containers (PDF & Notes)**
    * 5.3.1 LinearLayout (PDF & Notes)
        * 5.3.1.1 Vertical and Horizontal Orientation (`android:orientation`)
        * 5.3.1.2 Weight (`android:layout_weight`) for Space Distribution
        * 5.3.1.3 Examples and Exercises
    * 5.3.2 RelativeLayout (PDF & Notes)
        * 5.3.2.1 Positioning Relative to Container (`android:layout_alignParentTop`, etc.)
        * 5.3.2.2 Positioning Relative to Other Elements (`android:layout_below`, etc.)
        * 5.3.2.3 Examples and Exercises
    * 5.3.3 TableLayout (PDF & Notes)
        * 5.3.3.1 Table Structure with `<TableRow>`
        * 5.3.3.2 Examples
    * 5.3.4 GridLayout (PDF & Notes)
        * 5.3.4.1 Grid Arrangement with `android:columnCount`, `android:rowCount`
        * 5.3.4.2 Examples and Exercises (Calculator Layout)

**Chapter 6: Basic UI Widgets (Notes & PDF)**

* **6.1 TextView (Notes & PDF)**
    * 6.1.1 Displaying Text
    * 6.1.2 Text Styling (`android:textStyle`, `android:typeface`, `android:textSize`, `android:textColor`)
* **6.2 EditText (Notes & PDF)**
    * 6.2.1 User Text Input
    * 6.2.2 `android:hint` (Placeholder Text)
    * 6.2.3 `android:inputType` (Input Type Control - List of Values)
    * 6.2.4 `android:text` (Initial Text Value)
    * 6.2.5 Java Methods: `getText()`, `setText()`
* **6.3 Button / ImageButton (Notes & PDF)**
    * 6.3.1 User Interaction
    * 6.3.2 `android:text` (Button Text)
    * 6.3.3 `android:src` (ImageButton Source)
* **6.4 CheckBox (Notes & PDF)**
    * 6.4.1 Boolean Selection
    * 6.4.2 Checking State in Java (`isChecked()`)
* **6.5 RadioButton / RadioGroup (Notes & PDF)**
    * 6.5.1 Mutually Exclusive Selection
    * 6.5.2 Vertical and Horizontal RadioGroup Orientation
    * 6.5.3 Checking State in Java (`isChecked()`)
* **6.6 Toast (Notes & PDF)**
    * 6.6.1 Short Pop-up Messages
    * 6.6.2 Java Implementation (`Toast.makeText()`, `toast.show()`)

**Chapter 7: Event Handling - Click Events (Notes & PDF)**

* **7.1 Handling Button Clicks (Notes & PDF)**
    * 7.1.2 Using `OnClickListener` Interface (Java Approach)
        * 7.1.2.1 Activity Implementing `OnClickListener`
        * 7.1.2.2 Anonymous `OnClickListener`
    * 7.1.3 Using `android:onClick` Attribute (XML Approach)
        * 7.1.3.1 XML Button Example
        * 7.1.3.2 Corresponding Java Method
* **7.2 Example: Addition Application (La Somme) (Notes)**
    * 7.2.1 XML Layout Code
    * 7.2.2 Java Activity Code (OnClickListener and android:onClick Solutions)

**Part 3: Advanced Android Concepts**

**Chapter 8: Resources (Notes & PDF)**

* **8.1 Introduction to Resources (Notes & PDF)**
    * 8.1.1 External Files (Non-Code Instructions)
    * 8.1.2 `R` Class for Resource Access
    * 8.1.3 Syntax: `R.type_de_ressource.nom_ressource`
    * 8.1.4 Examples and `R` Class Structure
* **8.2 String Resources (Notes & PDF)**
    * 8.2.1 Storing in `res/values/strings.xml`
    * 8.2.2 Adding String Resources (`<string>`)
    * 8.2.3 Using String Resources in Java and XML
    * 8.2.4 Localization with String Resources
* **8.3 Mipmap Resources (Icons) (Notes & PDF)**
    * 8.3.1 Storing in `res/mipmap/`
    * 8.3.2 Referencing in XML (`@mipmap/`) and Java (`R.mipmap.`)
* **8.4 Drawable Resources (Images) (Notes & PDF)**
    * 8.4.1 Storing in `res/drawable/`
    * 8.4.2 Referencing in XML (`@drawable/`) and Java (`R.drawable.`)
* **8.5 Color Resources (Notes & PDF)**
    * 8.5.1 Storing in `res/values/colors.xml`
    * 8.5.2 Adding Color Resources (`<color>`)
    * 8.5.3 Referencing in XML (`@color/`)
* **8.6 Style Resources (Notes & PDF)**
    * 8.6.1 Storing in `res/values/styles.xml`
    * 8.6.2 Creating Styles (`<style>`)
    * 8.6.3 Applying Styles in XML (`android:theme="@style/"`)
    * 8.6.4 Example Styles (TextStyle1, TextStyle2)
* **8.7 Menu Resources (Notes & PDF)**
    * 8.7.1 Storing in `res/menu/`
    * 8.7.2 Creating Menu XML Files (`<menu>`, `<item>`)
    * 8.7.3 Example Menu (Toolbar Menu)

**Chapter 9: Menus and Action Bar (Notes & PDF)**

* **9.1 Action Bar / Toolbar (Notes & PDF)**
    * 9.1.1 Toolbar in Layout XML (`<Toolbar>`)
    * 9.1.2 Toolbar in Java (Setting Title, Icon, Visibility)
    * 9.1.3 Menu in Toolbar (`toolbar_menu.xml`)
    * 9.1.4 Inflating Menu in Java (`onCreateOptionsMenu`)
    * 9.1.5 Handling Menu Item Clicks (`onOptionsItemSelected`)
* **9.2 Option Menu (PDF)**
    * 9.2.1 Creating Option Menu (`onCreateOptionsMenu`)
    * 9.2.2 `MenuInflater` and `inflate` Method
    * 9.2.3 `showAsAction` Attribute (Menu Item Visibility)
    * 9.2.4 Reactions to Item Selections (`onOptionsItemSelected`)
    * 9.2.5 `onOptionsItemSelected` Code Example (Switch Statement)
* **9.3 Contextual Menu (PDF & Notes)**
    * 9.3.1 Context Menu Definition (Long Press on GUI Object)
    * 9.3.2 Associating Context Menu with Widget (`registerForContextMenu`)
    * 9.3.3 Creation of Contextual Menu (`onCreateContextMenu` - Inflating Menu XML)
    * 9.3.4 Reactions to Context Menu Item Selections (`onContextItemSelected`)
* **9.4 Pop-up Menu (PDF & Notes)**
    * 9.4.1 Pop-up Menu Definition (Click on a View)
    * 9.4.2 Activity Implementing `PopupMenu.OnMenuItemClickListener`
    * 9.4.3 Java Class: `PopupMenu`
    * 9.4.4 `PopupMenu` Class Methods (`setOnMenuItemClickListener`, `inflate`, `show`)
    * 9.4.5 Example: Showing Popup on Button Click (`showMyMenu` method)
    * 9.4.6 Handling Pop-up Menu Item Clicks (`onMenuItemClick` method)

**Chapter 10: Lists and Adapters - ListView (Notes & PDF)**

* **10.1 Introduction to ListView (Notes & PDF)**
    * 10.1.1 Managing Lists of Items
    * 10.1.2 ListView as a Group of Views Displaying List
    * 10.1.3 List Items Automatically Inserted Using Adapter
    * 10.1.4 Adapter Extracts Data and Converts to Views
* **10.2 Reminder: Java ArrayList (PDF)**
    * 10.2.1 Generic Data Type `<type>`
    * 10.2.2 Creating ArrayList (`ArrayList<TYPE> list = new ArrayList<TYPE>();`)
    * 10.2.3 Example with `Book` Class
    * 10.2.4 Useful ArrayList Methods (`size()`, `clear()`, `add()`, `remove()`, `get()`, `contains()`, `indexOf()`)
* **10.3 Creating a ListView (PDF & Notes)**
    * 10.3.1 Create Layout for Screen (Identified ListView)
    * 10.3.2 Create Layout for Items (List Elements, Identified Widgets)
    * 10.3.3 Create Adapter to Access Data
* **10.4 Adapter Role (Notes & PDF)**
    * 10.4.1 Object Displaying Item in ListView
    * 10.4.2 Fetches Data, Instantiates Item Layout with Data Values
    * 10.4.3 Accesses Data (Table, Database)
    * 10.4.4 Creates Item Display Views (Inflate Layout)
* **10.5 Predefined Adapters (PDF & Notes)**
    * 10.5.1 `ArrayAdapter` for Simple Array (Dynamic List)
    * 10.5.2 `SimpleCursorAdapter` for Database Access
    * 10.5.3 Both Extend `BaseAdapter`
* **10.6 ArrayAdapter<Type> for Lists (PDF & Notes)**
    * 10.6.1 Displays Data from ArrayList (Single String Per Item)
    * 10.6.2 Constructor: `ArrayAdapter(Context context, int item_layout_id, int textview_id, List<T> data)`
    * 10.6.3 Constructor Parameters Explained
* **10.7 Notes on Simple List Elements (PDF & Notes)**
    * 10.7.1 Android Layout for Simple List Elements: `android.R.layout.simple_list_item_1`
    * 10.7.2 Single TextView Layout, Identifier: `android.R.id.text1`
    * 10.7.3 Minimalist Display Style (List of Strings Only)
* **10.8 Example: ArrayAdapter Implementation (PDF & Notes)**
    * 10.8.1 Layout for Items (`simpleitem.xml` - LinearLayout with TextView)
    * 10.8.2 Layout for Activity (`activity_simpleliste.xml` - LinearLayout with ListView)
    * 10.8.3 Java Code - Creating and Initializing ArrayList
    * 10.8.4 Java Code - Creating ArrayAdapter
    * 10.8.5 Java Code - Associating ListView and Adapter
* **10.9 Handle Click on ListView Items (PDF & Notes)**
    * 10.9.1 Implement `ListView.OnItemClickListener` Interface
    * 10.9.2 Override `onItemClick` Method
    * 10.9.3 Add Click Listener to ListView Element (`setOnItemClickListener`)
    * 10.9.4 `onItemClick` Method Parameters Explained (`AdapterView parent`, `View view`, `int position`, `long id`)
* **10.10 Custom ListView and Adapter (PDF & Notes)**
    * 10.10.1 Custom Adapter for More Information Display
    * 10.10.2 Extend `BaseAdapter` Class and Redefine `getView` Method
    * 10.10.3 Constructor Parameters (Context, ArrayList)
    * 10.10.4 Example with `Book` Class
    * 10.10.5 Layout for Activity (with ListView - `activity_list.xml`)
    * 10.10.6 Layout for Items (`item_list.xml` - LinearLayout with TextViews for Title and Author)
    * 10.10.7 Creating Custom Adapter (`BookAdapter.java` - Constructor, `getView` implementation)
    * 10.10.8 Activity Java Code (Creating List, Adapter, Associating ListView and Adapter)

**Chapter 11: CursorAdapter and SQLite Integration (PDF & Notes)**

* **11.1 CursorAdapter (PDF & Notes)**
    * 11.1.1 Adapter Exposing Data from Cursor to ListView
    * 11.1.2 Cursor Browses SELECT Query Result
    * 11.1.3 Extend `CursorAdapter`, Redefine `newView()` and `bindView()`
    * 11.1.4 Constructor Parameters (Context, Cursor)
    * 11.1.5 `newView()` Method (Instantiate New View)
    * 11.1.6 `bindView()` Method (Link Data to View)
* **11.2 Retrieve the Cursor (PDF & Notes)**
    * 11.2.1 Interrogate SQLite Database and Recover Cursor
    * 11.2.2 Use `SQLiteOpenHelper`
    * 11.2.3 Use `rawQuery` Method
    * 11.2.4 Example Code for Retrieving Cursor
* **11.3 Attach Adapter to ListView (PDF & Notes)**
    * 11.3.1 `setAdapter` Method to Attach ListView and Adapter
    * 11.3.2 Example Code for Attaching Adapter
* **11.4 Example: CursorAdapter Implementation (PDF & Notes)**
    * 11.4.1 `liste_etudiant.xml` (Layout with ListView)
    * 11.4.2 `Item_layout.xml` (Layout for ListView Items)
    * 11.4.3 `MyCursorAdapter.java` (Constructor, `newView()`, `bindView()` implementations)
    * 11.4.4 `Liste_Etudiant.java` (Activity - Get Cursor, Create Adapter, Set Adapter)

**Chapter 12: JSON Data Handling (Notes & PDF)**

* **12.1 Introduction to JSON (Notes & PDF)**
    * 12.1.1 JSON - JavaScript Object Notation
    * 12.1.2 Data Exchange Format
    * 12.1.3 Lightweight, Easy to Read/Write
    * 12.1.4 "Name/Value" Pair Structure
    * 12.1.5 Android JSON Libraries
* **12.2 JSON Elements (PDF & Notes)**
    * 12.2.1 JSONArray (`[ ]` Square Brackets)
    * 12.2.2 JSONObject (`{ }` Curly Brackets)
    * 12.2.3 Key/Value Pairs in JSONObject
    * 12.2.4 Key as String, Value Types (String, Integer, Double, etc.)
* **12.3 JSON Example (PDF & Notes)**
    * 12.3.1 Example JSON Array String
    * 12.3.2 Table Representation of JSON Data
* **12.4 Read JSON Data (PDF & Notes)**
    * 12.4.1 Android Classes for JSON Manipulation (`JSONArray`, `JSONObject`)
    * 12.4.2 Parsing JSONArray (`length()`, `getJSONObject(i)`)
    * 12.4.3 Parsing JSONObject (`getString()`, `getInt()`, `getDouble()`, etc.)
    * 12.4.4 Example Code Snippets for Parsing JSON Array and Objects
    * 12.4.5 Reading All JSON Data in a Loop
* **12.5 Write JSON Data (PDF & Notes)**
    * 12.5.1 Simple JSON Writing Process
    * 12.5.2 Create JSONObject or JSONArray and Use `put()` Method
    * 12.5.3 Example Code for Creating JSONObject

**Chapter 13: Connecting to a Database Server and AsyncTask (PDF)**

* **13.1 Connecting to a Database Server (PDF)**
    * 13.1.1 Procedures for Android Client-Server Database Connection
    * 13.1.2 PHP File for JSON Conversion
    * 13.1.3 `json_encode()` in PHP
    * 13.1.4 Server-Side and Client-Side Architecture Diagram
* **13.2 Server-Side Implementation (PDF)**
    * 13.2.1 Database Setup (DBMS, `dbtest` database, `etudiant` table)
    * 13.2.2 PHP File (SQL Queries, JSON Encoding)
    * 13.2.3 PHP Script Example Code
* **13.3 Android Client-Side Implementation (PDF)**
    * 13.3.1 Using `HttpURLConnection` (Path to PHP File)
    * 13.3.2 Local Emulator Address (`10.0.2.2`)
    * 13.3.3 Reading Input Stream (Server Response) - `InputStreamReader`, `BufferedReader`, `StringBuilder`
    * 13.3.4 Converting InputStream to String (`lireFlux` method example)
    * 13.3.5 Decoding JSON Data (JSONArray, JSONObject)
    * 13.3.6 Internet Permission (`<uses-permission android:name="android.permission.INTERNET"/>`)
    * 13.3.7 Android Client Code Example (Asking Server, Reading Input Stream)
* **13.4 AsyncTask for Background Tasks (PDF)**
    * 13.4.1 Problem: Main Thread Blocking
    * 13.4.2 Solution: Asynchronous Task `AsyncTask`
    * 13.4.3 AsyncTask Workflow (Activity Callback, AsyncTask Thread, UI Update)
    * 13.4.4 Structure of AsyncTask Thread (`onPreExecute`, `doInBackground`, `onProgressUpdate`, `onPostExecute`)
    * 13.4.5 Parameters of AsyncTask (`Params`, `Progress`, `Result` Types)
    * 13.4.6 Launching AsyncTask (`execute` method)
    * 13.4.7 Example: `onCreate` Method with AsyncTask (`GetData` class)
    * 13.4.8 AsyncTask Code Example (`GetData.java` - `doInBackground`, `onPostExecute` placeholders)

**Chapter 14: Publishing an Android App (PDF)**

* **14.1 Preliminary Steps for Publishing (PDF & Notes - Repetition for Emphasis)**
    * 14.1.1 Generate Application (APK File)
    * 14.1.2 Sign Application with Digital Signature
    * 14.1.3 Create Play Store Account and Publish Signed APK
* **14.2 Android Package (apk) (PDF & Notes - Repetition for Emphasis)**
    * 14.2.1 An Android application takes the form of a file with .apk extension
    * 14.2.2 APK is a ZIP archive containing different elements (Classes.dex, META-INF, res, jni and lib)
* **14.3 Why Sign APKs? (PDF & Notes - Repetition for Emphasis)**
    * 14.3.1 Applications (APK files) need to be digitally signed for installation on Android
    * 14.3.2 Signature allows you to: Guarantee Integrity, Identify Author, Guarantee Security during updates
* **14.4 Signing the APK (PDF & Notes - Repetition and Visual Guide)**
    * 14.4.1 Android Studio Build Menu: Generate Signed APK... (Visual Guide)
    * 14.4.2 Generate Signed APK Dialog - Key store path: Create new... (Visual Guide)
    * 14.4.3 New Key Store Dialog - Key store path, Password, Alias, Certificate details (Visual Guide)
    * 14.4.4 Generate Signed APK Dialog - Key store path filled, Key alias, Next button (Visual Guide)
    * 14.4.5 Generate Signed APK Dialog - APK Destination Folder, Build Type, Finish button (Visual Guide)

This merged Table of Contents should provide a more complete and structured overview of the Android development topics covered in both your handwritten notes and the PDF slides.  Let me know if you'd like any further refinement or adjustments!