
## `ob_start()` in PHP

### 📌 Definition

`ob_start()` is a PHP function that **starts output buffering**. When output buffering is active, any output (like `echo`, `print`, or HTML) is not immediately sent to the browser. Instead, it is stored in an internal buffer.

---

### 🔧 Syntax

```php
bool ob_start([callable $callback = null, int $chunk_size = 0, int $flags = PHP_OUTPUT_HANDLER_STDFLAGS])
```

- **`$callback`** (optional): A function to process the buffer contents before it's sent or cleaned.
    
- **`$chunk_size`** (optional): Size in bytes to automatically flush the buffer.
    
- **`$flags`** (optional): Controls buffer behavior.
    

---

### 📖 How It Works

1. `ob_start()` is called to begin buffering.
    
2. Any output is saved in memory, not sent to the browser.
    
3. You can retrieve the buffered content using `ob_get_contents()`.
    
4. You can clean (`ob_clean()`), end (`ob_end_clean()`), or flush (`ob_flush()`, `ob_end_flush()`) the buffer.
    

---

### 📌 Use Cases

- Modify output before sending (e.g., compressing HTML).
    
- Capture output to a variable.
    
- Prevent premature output before headers are sent.
    
- Templating systems.
    

---

### ✅ Example

```php
ob_start();
echo "Hello, world!";
$content = ob_get_contents(); // Captures the output
ob_end_clean(); // Cleans the buffer
file_put_contents('log.txt', $content); // Saves the output to a file
```

---

Let me know if you want the internal workings or use in templating systems.