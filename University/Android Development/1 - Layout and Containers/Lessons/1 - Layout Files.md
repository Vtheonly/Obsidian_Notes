- XML files that describe an interface are placed in the `res/layout` directory.
- They are referenced by `R.layout.XML_file_name`.
- Activities can use the `setContentView(R.layout.XML_file_name)` method to set up the interface described by an XML file.
- The basic block for building user interfaces is an object of the View class that occupies an area on the screen and is responsible for drawing and handling events.
- View is the base class for widgets, which are used to create interactive UI (User Interface) components such as buttons, text fields, etc.
- ViewGroup is a subclass of View and provides an invisible container that holds other Views or other ViewGroups and sets their layout properties.

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- This is a comment -->
<Main_container_class
    xmlns:android="http://schemas.android.com/apk/res/android"
    main container properties >

    <Container_or_interface_element_class
        properties />
    <!-- Other elements -->
    <Container_or_interface_element_class
        properties />

</Main_container_class>
```

- When one of the elements is a container, you must indicate the elements it contains:
```xml
<Container_class
    container properties >
    <Container_or_interface_element_class
        properties />
    <!-- Other elements -->
    <Container_or_interface_element_class
        properties />
</Container_class>
```

- The dimensions of interface elements (size, margins, etc.) can be expressed in:
  - Pixels (px)
  - Inches (in)
  - Millimeters (mm)
  - Points (pt) = 1/72 pouce
  - Independent density pixel (dp)
- Units are expressed in the form: "24.5mm" or "65px", etc.



----


- An ID can be associated with each element described in an XML file, allowing the referencing of the object created in other XML files.
- Elements that should not be referenced may not have an ID.
- To create an ID, the attribute `android:id` is used. For example: `android:id="@+id/my_ident"`.
- To find this element, the Java method `findViewById(R.id.my_ident)` is used.

### Size
- All elements of the UI must provide a size, using the following two attributes: `android:layout_height` and `android:layout_width`.
- These attributes can take three types of values:
  - A fixed size: for example, `50px` (pixels).
  - `match_parent`: The element occupies all available space in its parent container.
  - `wrap_content`: The element occupies the necessary space (the size of its content).

### Positioning
- By default, elements are placed in the layout at the top and left.
- To position an element, the attribute `android:gravity` is used.
- This attribute can take different values:
  - `android:gravity="center_horizontal"`
  - `android:gravity="center_vertical"`
  - `android:gravity="top"`
  - `android:gravity="bottom"`
  - `android:gravity="left"`
  - `android:gravity="right"`
- It is possible to combine the values using the symbol `|`, for example: `android:gravity="top|right"`.

### Text
- Text can be added to an interface element using the attribute `android:text`. For example: `android:text="Cancel"`.


![[3.png]]


![[4.png]]


- By default, different elements created are tight.
- Spacing can be adjusted using the properties `android:padding` (internal margins) and `android:layout_margin` (external margins).
- For example:
  - `android:padding="5px"` specifies the space between the outline of the element and its content.
  - `android:layout_margin="5px"` specifies the space between the outline of the element and the outline of its neighbors.
- It's also possible to create an offset only on one side of the widget:
  - Left with `paddingLeft` or `layout_marginLeft`.
  - Right with `paddingRight` or `layout_marginRight`.
  - Top with `paddingTop` or `layout_marginTop`.
  - Bottom with `paddingBottom` or `layout_marginBottom`.



![[5.png]]


