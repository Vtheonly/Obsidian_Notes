- Allows us to define the position of elements relative to other elements.
- The position of each view is specified relative to sibling elements or relative to the container.

![[21.png]]


RelativeLayout allows us to define the position of elements relative to other elements or relative to the container itself. When positioning relative to the container, we utilize specific attributes such as :

| Property                           | Description                                                                                                        |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `android:layout_alignParentTop`    | Specifies whether the upper edge of the element must be aligned with that of its container (the value is Boolean). |
| `android:layout_alignParentBottom` | Specifies the alignment at the bottom of the container.                                                            |
| `android:layout_alignParentLeft`   | Specifies the left alignment of the container.                                                                     |
| `android:layout_alignParentRight`  | Specifies the right alignment of the container.                                                                    |
| `android:layout_centerHorizontal`  | Indicates whether the element should be centered horizontally in its container.                                    |
| `android:layout_centerVertical`    | Indicates whether the element should be centered vertically in its container.                                      |
| `android:layout_centerInParent`    | Indicates that the element should be centered horizontally and vertically in the container.                        |


![[22.png]]



![[23.png]]



![[24.png]]



![[25.png]]



## Positioning relative to other elements : 
- We can position an element relative to another using its id Here's how they can be structured:

|                  CODE                  |                                           Description                                            |
| :------------------------------------: | :----------------------------------------------------------------------------------------------: |
|     `android:layout_above="@id/x"`     |                   Place the element above that indicated by its id (`@id/x`).                    |
|     `android:layout_below="@id/x"`     |                   Place the element below that indicated by its id (`@id/x`).                    |
|   `android:layout_toLeftOf="@id/x"`    |               Place the element to the left of that indicated by its id (`@id/x`).               |
|   `android:layout_toRightOf="@id/x"`   |              Place the element to the right of that indicated by its id (`@id/x`).               |
|   `android:layout_alignLeft="@id/x"`   |  The left side of the element is aligned with the left side of the indicated element (`@id/x`).  |
|  `android:layout_alignRight="@id/x"`   | The right side of the element is aligned with the right side of the indicated element (`@id/x`). |
|   `android:layout_alignTop="@id/x"`    |        The top of the element is aligned with the top of the indicated element (`@id/x`).        |
|  `android:layout_alignBottom="@id/x"`  |     The bottom of the element is aligned with the bottom of the indicated element (`@id/x`).     |
| `android:layout_alignBaseline="@id/x"` |             Indicates that the baselines of the two elements are aligned (`@id/x`).              |


![[26.png]]



![[27.png]]


![[28.png]]


![[29.png]]


![[30.png]]



![[31.png]]


Write the xml code for the following GUI using a RelativeLayout:

![[32.png]]