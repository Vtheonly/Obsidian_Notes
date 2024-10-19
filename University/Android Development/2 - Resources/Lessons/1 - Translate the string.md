To translate the string resources in an Android application, you typically follow these steps:

1. **Define String Resources**: First, you define your string resources in XML files located in the `res/values` directory. These files are typically named `strings.xml`.

2. **Create Translations**: Next, you create additional XML files in directories with the appropriate language or region code, such as `res/values-fr` for French translations or `res/values-es-rMX` for Spanish in Mexico. In these files, you provide translated versions of your string resources.

3. **Use Resource IDs**: In your application code, instead of hardcoding strings directly, you reference the string resources by their resource IDs. For example, instead of `"Hello"`, you would use `R.string.hello`.

4. **Locale Handling**: Android automatically selects the appropriate string resources based on the user's device locale settings. If the user's preferred language matches one of the available translations in your app, Android will use that translation. Otherwise, it will default to the base language (typically English).

Here's an example of how you would define a string resource and its translations in XML:

In `res/values/strings.xml`:
```xml
<resources>
    <string name="hello">Hello</string>
</resources>
```

In `res/values-fr/strings.xml`:
```xml
<resources>
    <string name="hello">Bonjour</string>
</resources>
```

And in your application code, you would reference the string resource like this:
```java
String greeting = getString(R.string.hello);
```

When the device is set to French, the `greeting` variable would contain "Bonjour" instead of "Hello".

This approach makes it easy to maintain multiple language versions of your app without the need to recompile it each time a translation is updated.