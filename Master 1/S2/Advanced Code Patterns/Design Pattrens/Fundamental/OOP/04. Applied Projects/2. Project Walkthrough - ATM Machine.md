### 1. The Goal

A console-based banking application using **Exception Handling** and **HashMaps**.

### 2. Key Components

- **HashMap:** Used as a database to store `Customer Number (Key)` -> `PIN (Value)`.
  - `HashMap<Integer, Integer> data = new HashMap<>();`
- **Exception Handling:**
  - Used in the login flow. If the user enters a letter instead of a number for the PIN, the program catches the error inside a `try-catch` block to prevent a crash.
- **Logic Flow:**
  1.  **Login:** Validate ID and PIN against HashMap.
  2.  **Account Selection:** User chooses Checking or Savings.
  3.  **Action:** Withdraw or Deposit.

### 3. Business Logic (Validation)

The project emphasizes logic validation inside Setters/Methods.

- _Negative Balance Check:_ When withdrawing, the code checks:
  `java
    if ((balance - amount) >= 0) {
        calcWithdraw(amount);
    } else {
        System.out.println("Balance cannot be negative.");
    }
    `
  This ensures the object (Account) never enters an invalid state.
