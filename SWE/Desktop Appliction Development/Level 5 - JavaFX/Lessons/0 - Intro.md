
**INSTALLATION PROCESS**

1. **DOWNLOAD JAVA FX SDK FROM THE WEBSITE OPENJAVAFX.IO**
    1. Navigate to openjfx.io.
    2. Select the appropriate SDK version (e.g., for Windows 64-bit, choose the ZIP file).
    3. After downloading, extract the files to a location of your choice. It's recommended to keep it separate from your project directory for better organization.

2. **CREATE A NEW JAVA FX PROJECT IN INTELLIJ IDEA**
    1. Open IntelliJ IDEA.
    2. Go to `Files` > `New` > `Project`.
    3. Choose `JavaFX` project.
    4. Select the appropriate Java SDK version (15, 16, 17, etc.).
    5. Give your project a name and click `Finish`.

3. **ADD THE SDK LIBRARY**
    1. Go to `Files` > `Project Structure`.
    2. Under `Libraries`, click the `+` button and choose `Java`.
    3. Navigate to the path where you extracted the JavaFX SDK, and select the `lib` folder.
    4. Click `OK` and `Apply`. Any library referencing errors should now be resolved.

4. **ADD VM OPTIONS**
    1. Visit the JavaFX website and go to the section "JavaFX and IntelliJ IDEA - Non-modular from IDE".
    2. Scroll down to find the VM options.
    3. Copy the appropriate VM option for your operating system.


```shell

--module-path "\path\to\javafx-sdk-22.0.1\lib" --add-modules javafx.controls,javafx.fxml

```

	
4. add to vm at run > edit configuration > add configiration > more > add vm option 