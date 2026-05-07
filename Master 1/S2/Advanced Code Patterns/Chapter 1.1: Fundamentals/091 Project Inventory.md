### 1. The Goal

Create a game inventory system demonstrating **Encapsulation** and **Polymorphism**.

### 2. Class Structure

```mermaid
classDiagram
    class Item {
        <<Abstract>>
        -String name
        -int quantity
        +Item(name, quantity)
        +toString()
    }
    class Weapon {
        -int damage
        -String type
        +Weapon(name, quantity, damage, type)
        +toString()
    }
    class Fruit {
        -String type
        +Fruit(name, quantity, type)
        +toString()
    }
    class Inventory {
        -ArrayList<Item> items
        +addItem(Item)
        +displayInventory()
    }

    Item <|-- Weapon
    Item <|-- Fruit
    Inventory o-- Item : Aggregation
```

### 3. Key Concepts Applied

- **Encapsulation:** The `Item` class has `private` name and quantity. Access is strictly via Getters.
- **Inheritance:** `Weapon` extends `Item`.
  - It uses `super(name, quantity)` to store data in the parent class.
  - It adds unique data: `damage` and `weaponType`.
- **Polymorphism (Overriding):**
  - The `toString()` method in `Item` is overridden in `Weapon` to display damage stats.
  - The `Inventory` class holds a list of `Item` objects (`ArrayList<Item>`). Because of polymorphism, this list can hold both `Fruit` objects and `Weapon` objects simultaneously.

**Code Highlight: Dynamic Binding in Inventory**

```java
// Inventory.java
for (Item i : items) {
    // This calls the specific toString() of Weapon or Fruit
    // depending on what the object actually is.
    System.out.println(i.toString());
}
```
