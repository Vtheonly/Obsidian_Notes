
## Main Components

### 1. `manifests`

-   **What it is:** This folder contains the `AndroidManifest.xml` file.
-   **Purpose:**
    -   Acts as the control center for your Android app.
    -   Declares essential information about the application to the Android system, build tools, and Google Play Store.
    -   Specifies components (activities, services, etc.), required permissions (e.g., camera, location), and the minimum API level the app supports.

### 2. `java`

-   **What it is:** The folder where all your Java (or Kotlin) source code lives.
-   **Purpose:**
    -   Contains the core logic and functionality of your app.
    -   Organized into packages to structure and manage the code.
    -   Includes activities (for UI screens), services (for background tasks), and other classes.

### 3. `ressources` (res)

-   **What it is:** A crucial directory housing all non-code resources.
-   **Purpose:**
    -   Provides a way to separate resources from code, allowing for easier management and localization.
    -   Contains subfolders for various resource types:
    -   `drawable`: Contains image files (PNG, JPG, GIF) and XML files defining shapes, selectors, and other graphical elements. Used for icons, backgrounds, and other UI elements.
    -   `layout`: Contains XML files that define the layout and structure of the user interface. Each file represents the layout of a single screen or part of a screen.
    -   `mipmap`: Holds app icons in various densities to ensure sharpness on different screen resolutions.
    -   `values`: Stores XML files that define simple values like strings, colors, dimensions, and styles. This allows for easy modification and reuse of values across the app.

### 4. `Gradle Scripts`

-   **What it is:** Contains files related to the Gradle build system.
-   **Purpose:**
    -   Gradle is used to automate the build process of your Android app.
    -   The `build.gradle` files define project and module dependencies, build configurations, and other build-related settings.
    -   Gradle handles tasks like compiling code, packaging resources, and generating the final APK (Android Package Kit) file for distribution.

## Sub-components within `res`

### `drawable`

-   Contains images and XML drawables for the user interface.

### `layout`

-   XML files that define the graphical layouts of your app's screens.

### `mipmap`

-   Houses application icons in different resolutions to support various screen densities.

### `values`

-   XML files storing configuration values like:
    -   `colors.xml`: Defines color resources.
    -   `strings.xml`: Contains localized string resources for text displayed in the app.
    -   `dimens.xml`: Stores dimension values (e.g., margins, font sizes).
    -   `styles.xml`: Defines styles and themes to customize the appearance of UI elements.

## Summary

This structure helps organize an Android project effectively. By separating code, resources, and build configurations, Android projects become more manageable, scalable, and maintainable.