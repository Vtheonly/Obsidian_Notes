Containers, known as layouts in Android development, are crucial components for organizing elements within the graphical interface. They serve as containers for various UI elements like TextViews, Buttons, etc., allowing developers to arrange these elements effectively on the screen.

There are several types of layouts available in Android, each with its unique characteristics. One common layout is the LinearLayout, which is a ViewGroup that arranges its child views in a single direction, either vertically or horizontally. The direction of arrangement can be specified using the `android:orientation` attribute.

![[14.png]]

![[15.png]]

![[16.png]]

---

Assigning a weight:

- The attribute `android:layout_weight` assigns a weight to an element.
- The remaining space in the layout is allocated according to the declared weight proportion. The default weight is zero.

```xml
<LinearLayout
    android:orientation="horizontal"
    android:layout_width="match_parent"
    android:layout_height="wrap_content">

    <Button
        android:text="Button1"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_weight="1" />

    <Button
        android:text="Button2"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" />

    <Button
        android:text="Button3"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" />

</LinearLayout>
```

In the example above, three buttons are placed horizontally within a LinearLayout. The first button has a weight of 1, indicating that it should occupy any remaining space after the other views have been measured. The other buttons do not have a weight specified, so they will take up only the space required by their content.



![[18.png]]



----



```xml
<LinearLayout
    android:orientation="vertical"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <Button
        android:text="Button1"
        android:layout_width="match_parent"
        android:layout_height="wrap_content" />

    <Button
        android:text="Button2"
        android:layout_width="match_parent"
        android:layout_height="wrap_content" />

    <LinearLayout
        android:orientation="horizontal"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="center">

        <Button
            android:text="Button3"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content" />

        <Button
            android:text="Button4"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content" />

        <Button
            android:text="Button5"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content" />
            
    </LinearLayout>

    <Button
        android:text="Button6"
        android:layout_width="match_parent"
        android:layout_height="wrap_content" />

</LinearLayout>
```

In this layout:
- Buttons 1 and 2 are placed vertically in the parent LinearLayout.
- Buttons 3, 4, and 5 are placed horizontally in a nested LinearLayout, which itself is centered horizontally within the parent LinearLayout.
- Button 6 is placed below the nested LinearLayout, occupying the remaining vertical space in the parent LinearLayout.



![[19.png]]

----


```xml
<LinearLayout 
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >

    <EditText 
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="to" />

    <EditText 
        android:layout_height="wrap_content"
        android:layout_width="match_parent"
        android:hint="subject" />

    <EditText 
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_weight="1"
        android:gravity="top"
        android:hint="message" />

    <Button 
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="right"
        android:text="send" />
        
</LinearLayout>
```
In this layout:
- Three EditText fields are stacked vertically, each taking the full width of the parent LinearLayout.
- The third EditText field, designated with a layout_weight of 1, will expand to fill any remaining vertical space.
- The Button is aligned to the right within the LinearLayout.

The `android:gravity` attribute is used to position the content of an element within its own boundaries. For example, setting `android:gravity="top"` will align the content of the element to the top.

On the other hand, the `android:layout_gravity` attribute is used to position an element within its parent container. For instance, setting `android:layout_gravity="right"` will position the element to the right side of its parent container.

![[20.png]]