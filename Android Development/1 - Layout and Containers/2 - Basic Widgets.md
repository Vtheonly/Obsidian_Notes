
Basic widgets are fundamental components used to create graphical user interfaces (GUI). Each type of widget is a class that derives from the "View" class and is systematically placed in layouts.

### TextView
The TextView widget is used to display text on the screen.

```xml
<TextView
    android:text="TextView"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:id="@+id/textView" />
```

#### Text Style
- The attribute `android:textStyle` can take values like "normal", "bold", or "italic".
  - Example: `android:textStyle="italic"`

#### Typeface
- The attribute `android:typeface` allows you to choose the font, such as "sans", "serif", etc.
  - Example: `android:typeface="sans"`

There are other attributes available for the TextView widget, such as text color, font size, etc., which can be further customized to meet specific design requirements.



### EditText

The EditText widget is used for accepting user input through text.

#### Basic EditText
```xml
<EditText
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:hint="Enter your Name" />
```
- The `android:hint` attribute allows displaying a hint or placeholder text within the EditText to guide the user.

#### EditText for Phone Number
```xml
<EditText
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:inputType="phone"
    android:text="0367569867"/>
```
- The `android:inputType` attribute allows choosing an entry type, such as text, password, number, date, etc.

#### Password EditText
```xml
<EditText
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:hint="Enter your password"
    android:inputType="textPassword"/>
```
- The `android:inputType="textPassword"` attribute hides the entered text and displays it as asterisks for privacy.

These EditText widgets provide flexibility in collecting various types of user input and can be further customized to suit specific application requirements.



![[6.png]]



The `android:inputType` attribute specifies the type of data that can be entered into an EditText widget. Here are some common values for the `android:inputType` attribute:

- `text`: Standard text input.
- `textMultiLine`: Allows for multiline text input.
- `textUri`: Input type for entering a URI.
- `textEmailAddress`: Input type for entering an email address.
- `textPassword`: Input type for entering a password. Characters are displayed as asterisks for privacy.
- `textWebEmailAddress`: Input type for entering an email address in a web form.
- `number`: Input type for entering a numeric value.
- `numberSigned`: Input type for entering a signed numeric value (positive or negative).
- `numberDecimal`: Input type for entering a decimal numeric value.
- `numberPassword`: Input type for entering a numeric password.
- `phone`: Input type for entering a phone number.
- `datetime`: Input type for entering a date and time.
- `date`: Input type for entering a date.
- `time`: Input type for entering a time.

These input types provide hints to the system about the type of keyboard that should be displayed and can help improve the user experience by providing appropriate input controls and validation.


![[7.png]]

### Button

The Button widget is used to create a clickable button in the user interface.

```xml
<Button
    android:text="Button"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:id="@+id/button"
    android:layout_gravity="center"/>
```
- The `android:text` attribute sets the text displayed on the button.
- The `android:layout_width` and `android:layout_height` attributes define the dimensions of the button.
- The `android:id` attribute assigns a unique identifier to the button.
- The `android:layout_gravity` attribute positions the button within its parent layout.

### ImageButton

The ImageButton widget is used to create a clickable image button in the user interface.

```xml
<ImageButton
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    app:srcCompat="@mipmap/ic_launcher"
    android:id="@+id/imageButton"
    android:layout_gravity="center"/>
```
- The `app:srcCompat` attribute sets the image displayed on the button. Here, `@mipmap/ic_launcher` refers to the launcher icon of the application.
- Other attributes such as `android:layout_width`, `android:layout_height`, `android:id`, and `android:layout_gravity` function similarly to those of the Button widget.

These widgets provide interactive elements that users can interact with by clicking or tapping, allowing for user interaction within the application's user interface.



![[8.png]]




### CheckBox

The CheckBox widget is used to allow users to make a binary choice, such as selecting or deselecting an option.

#### CheckBox 1
```xml
<CheckBox
    android:text="I am a checkbox 1"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:id="@+id/checkBox1" />
```

#### CheckBox 2
```xml
<CheckBox
    android:text="I am a checkbox 2"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:id="@+id/checkBox2" />
```

- The `android:text` attribute sets the text displayed next to the checkbox.
- The `android:layout_width` and `android:layout_height` attributes define the dimensions of the checkbox.
- The `android:id` attribute assigns a unique identifier to the checkbox.

To check if a checkbox is checked programmatically, you can use the following code:

```java
CheckBox checkBox = findViewById(R.id.checkBox1);
boolean isChecked = checkBox.isChecked();
```

This retrieves the CheckBox object by its ID and then checks whether it is currently checked or not.



![[9.png]]




---



### RadioButton

The RadioButton widget is used to allow users to select one option from a set of mutually exclusive options.

```xml
<RadioButton
    android:text="RadioButton"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:id="@+id/radioButton1" />
```

- The `android:text` attribute sets the text displayed next to the radio button.
- The `android:layout_width` and `android:layout_height` attributes define the dimensions of the radio button.
- The `android:id` attribute assigns a unique identifier to the radio button.

To check if a radio button is checked programmatically, you can use the following code:

```java
RadioButton radioButton = findViewById(R.id.radioButton1);
boolean isChecked = radioButton.isChecked();
```

This retrieves the RadioButton object by its ID and then checks whether it is currently selected or not.

### RadioGroup

The RadioGroup widget is used to group multiple radio buttons together so that only one radio button within the group can be selected at a time.

```xml
<RadioGroup
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:orientation="vertical">

    <RadioButton
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="YES"
        android:checked="true"/>

    <RadioButton
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="NO"/>

</RadioGroup>
```

- The `android:orientation` attribute defines the orientation of the radio buttons within the group, either vertical or horizontal.
- Each RadioButton within the RadioGroup will automatically become part of the same group, and only one RadioButton within the group can be selected at a time.




![[10.png]]


![[11.png]]

---

### Toast

A Toast is a small pop-up message that appears on the screen to convey information to the user. It typically appears for a short duration and disappears automatically without requiring any user interaction.

```java
Toast toast = Toast.makeText(this, "Here is our first toast", Toast.LENGTH_LONG);
toast.show();
```

- `Toast.makeText()`: This method creates a new Toast object with the specified text message.
- `this`: The first parameter represents the context in which the Toast should appear.
- `"Here is our first toast"`: The second parameter is the text message to be displayed in the Toast.
- `Toast.LENGTH_LONG`: The third parameter specifies the duration for which the Toast should be displayed. It can be either `Toast.LENGTH_SHORT` for a shorter duration or `Toast.LENGTH_LONG` for a longer duration.
- `toast.show()`: Finally, the `show()` method is called to display the Toast on the screen.

Using Toasts can provide users with quick feedback or information without interrupting their workflow, making them a useful tool for enhancing the user experience in an Android application.

![[12.png]]



