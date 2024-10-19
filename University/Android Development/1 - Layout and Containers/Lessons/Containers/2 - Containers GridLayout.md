
- **GridLayout** allows you to place elements on a grid, providing a structured way to arrange UI elements.
- Two essential attributes are required:
  - `android:columnCount`: Specifies the number of columns in the grid.
  - `android:rowCount`: Specifies the number of rows in the grid.
- Grid elements are automatically inserted into the layout, following the specified grid structure.

Example usage:

```xml
<GridLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/GridLayout1"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:columnCount="3"
    android:rowCount="3"
    android:orientation="horizontal">

    <Button android:text="Button 1" />
    <Button android:text="Button 2" />
    <Button android:text="Button 3" />
    <Button android:text="Button 4" />
    <Button android:text="Button 5" />
    <Button android:text="Button 6" />
    <Button android:text="Button 7" />
    <Button android:text="Button 8" />
    <Button android:text="Button 9" />
</GridLayout>
```

In this example, a `GridLayout` with 3 columns and 3 rows is defined, and buttons are placed within it. The grid layout automatically arranges the buttons according to the specified grid structure.


![[37.png]]


<center>
`android:orientation="vertical">`

</center>


 
![[38.png]]

check the pdf [Les interfaces graphiques]

![[39.png]]



