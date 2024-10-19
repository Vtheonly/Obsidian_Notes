
Menus in Android serve as lists of options accessible via the menu button or action bar, with some items permanently present in the latter. Selecting an item triggers a callback, invoking specific methods. Here's a breakdown of menu creation and management:

1. **Menu Creation**:
   - To craft a menu, create a file named `menu_name.xml` in the `res/menu` directory.
   - Define menu items within the `<menu>` tag, specifying attributes like `android:id`, `android:title`, and `android:icon` for each `<item>`.

2. **Example**:
   ```xml
   <menu>
       <item properties />
       <item properties />
       <!-- Additional items -->
   </menu>
   ```

3. **Properties of Menu Items**:
   - Each `<item>` in the menu can have attributes such as identifier, icon, title, and more. These attributes define the appearance and behavior of the menu items.

Menus play a vital role in enabling users to perform actions within an app, such as sharing content, deleting items, or editing information. They enhance user experience by providing convenient access to app functionality.

2. **Example**:
   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <menu xmlns:android="http://schemas.android.com/apk/res/android">
       <item
           android:id="@+id/itemshare"
           android:title="Share"
           android:icon="@drawable/iconshare"/>

       <item
           android:id="@+id/itemdelete"
           android:title="Delete"
           android:icon="@drawable/icondelete"/>

       <item
           android:id="@+id/itemedit"
           android:title="Edit"
           android:icon="@drawable/iconedit" />
   </menu>
   ```

3. **Menu Callbacks**:
   - There are two principal callbacks for menu management:
     - **Menu Creation**: Inflate the XML menu resource to construct the menu.
     - **Events Management (Item Selection)**: Handle user actions when selecting menu items.

Menus play a vital role in enabling users to perform actions within an app, such as sharing content, deleting items, or editing information. They enhance user experience by providing convenient access to app functionality.

## 1. Option menu :
1. `onCreateOptionsMenu(Menu menu)`
2. `onOptionsItemSelected(MenuItem item)`
## 2. Context menu :
1. `registerForContextMenu(Button)`
2. 
```java

onCreateContextMenu(ContextMenu menu, View v, ContextMenu.ContextMenuInfo menuInfo) ;
super.onCreateContextMenu(menu, v, menuInfo);

```

3. `onContextItemSelected(MenuItem item)`

## 3. Pop-up menu : 

> The activity must implement the interface: `PopupMenu.OnMenuItemClickListener` (to handle the item selections)

1. `PopupMenu.setOnMenuItemClickListener`
2. `onMenuItemClick(MenuItem item)`






```java
@Override
public boolean ##########(MenuItem item){ 
    switch (item.getItemId()) { 
        case R.id.item1: …………………; 
            return true; 
        case R.id.item2: …………………;
            return true;
        ………… 
        default: 
            return super.onOptionsItemSelected(item);
    } 
}

```

## 1. Option menu :
1. `onCreateOptionsMenu(Menu menu)`
2. `onOptionsItemSelected(MenuItem item)`
## 2. Context menu :
1. `registerForContextMenu(Button)`
2. 
```java
onCreateContextMenu(ContextMenu menu, View v, ContextMenu.ContextMenuInfo menuInfo) 
```

3. `onContextItemSelected(MenuItem item)`

## 3. Pop-up menu : 

> The activity must implement the interface: `PopupMenu.OnMenuItemClickListener` (to handle the item selections)

1. `PopupMenu.OnMenuItemClickListener`
2. `onMenuItemClick(MenuItem item)`
