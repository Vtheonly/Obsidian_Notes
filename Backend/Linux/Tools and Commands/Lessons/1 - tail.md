

# Note on the `tail` Command

**`tail`** is a command-line utility in Unix/Linux used to display the last part of files. It is particularly useful for viewing the most recent entries in log files.

### Key Features:
- **Default Behavior**: Displays the last 10 lines of a specified file.
  ```bash
  tail filename.txt
  ```

- **Specify Number of Lines**: Use the `-n` option to show a specific number of lines from the end.
  ```bash
  tail -n 20 filename.txt
  ```

- **Follow Mode**: The `-f` option allows real-time monitoring of file updates, displaying new lines as they are added.
  ```bash
  tail -f filename.log
  ```

### Usage:
- **Log Monitoring**: Ideal for checking logs in real time or viewing the most recent entries without opening the entire file.

---

Feel free to adjust or expand this note as needed!