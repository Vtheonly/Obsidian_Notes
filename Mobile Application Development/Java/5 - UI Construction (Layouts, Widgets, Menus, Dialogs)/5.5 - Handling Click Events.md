### Handling Click Events

There are two common approaches to handle click events in Android:


#### 1. Using a Click Listener (OnClickListener Interface)



Certainly! Here's the improved presentation:

We follow the following steps:

1. Implement the Java interface `OnClickListener` (use the keyword `implements`).
   - Example:
     ```java
     public class MainActivity extends AppCompatActivity implements OnClickListener {
     ```
2. Redefine the method `onClick(View v)` of the interface `OnClickListener`.
   - This method is called when a click event is detected (captured).
3. Add a click listener to a widget to listen and capture the click event.
   - Use the method `setOnClickListener()`.
   - Example:
     ```java
     Button b = this.findViewById(R.id.button);
     b.setOnClickListener(this);
     ```




Example:

```java
public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button button = findViewById(R.id.button);
        button.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        // Handle the click event here
        switch (v.getId()) {
            case R.id.button:
                // Code to execute when the button is clicked
                break;
            // Add cases for other views if needed
        }
    }
}
```

---
#### 2. Use the attribute `android:onClick` in a GUI xml file


To handle click events using the `android:onClick` attribute in a GUI XML file, follow these steps:

1. Define the method in your activity or fragment class that you want to execute when the button is clicked.
2. In the XML layout file, set the `android:onClick` attribute of the button to the name of the method.

Example:

#### MainActivity.java

```java
public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void calculate(View v) {
        // Insert your code here to perform the calculation
    }
}
```

#### activity_main.xml

```xml
<Button
    android:id="@+id/button"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:text="Add"
    android:onClick="calculate" />
```

In this example, when the button is clicked, the `calculate(View v)` method in the `MainActivity` class will be invoked automatically. You can then implement the necessary logic inside the `calculate()` method to perform the desired action when the button is clicked.

---


### Example: Sum of Two Integers

This example demonstrates an Android application that calculates the sum of two integers. Two solutions are provided: one using a click listener and the other using the XML attribute `android:onClick`.

#### Solution 1: Using a Click Listener (Graphical Interface)

```xml
<LinearLayout ...>
    <EditText
        android:id="@+id/edita"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Enter the value of a" />
    <EditText
        android:id="@+id/editb"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Enter the value of b" />
    <Button
        android:id="@+id/btn"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Add"
        />
    <EditText
        android:id="@+id/edits"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Sum"
        />
</LinearLayout>
```

#### Java Source Code (Solution 1)

```java
public class MainActivity extends AppCompatActivity implements OnClickListener {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button b = this.findViewById(R.id.btn);
        b.setOnClickListener(this);
    }

    public void onClick(View v) {
        EditText op1 = this.findViewById(R.id.edita);
        EditText op2 = this.findViewById(R.id.editb);

        String a = op1.getText().toString();
        String b = op2.getText().toString();
        
        int s = Integer.parseInt(a) + Integer.parseInt(b);
        
        EditText sum = this.findViewById(R.id.edits);
        sum.setText(String.valueOf(s));
    }
}
```

This implementation sets up a button click listener in the activity to handle the addition of two integers entered by the user.



![[13.png]]



---


Here's the second solution:

```xml
<LinearLayout ...>
    <EditText
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/edita"
        android:hint="Donner la valeur de a" />
    <EditText
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/editb"
        android:hint="Donner la valeur de b" />
    <Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Additionner"
        android:onClick="calculerSomme" />
    <EditText
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/edits"
        android:hint="La somme" />
</LinearLayout>
```

```java
public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
    
    public void calculerSomme(View v) {
        EditText op1 = this.findViewById(R.id.edita);
        EditText op2 = this.findViewById(R.id.editb);
        String a = op1.getText().toString();
        String b = op2.getText().toString();
        int s = Integer.parseInt(a) + Integer.parseInt(b);
        EditText somme = this.findViewById(R.id.edits);
        somme.setText(String.valueOf(s));
    }
}
```