# Quiz 2 - Processes and Shell

> [!info] About This Quiz
> This quiz covers processes, signals, systemd, the shell, pipelines, and text tools (grep, sed, awk, find).

Related: [[03 - Processes and Services/1. Processes and the Process Tree]] | [[03 - Processes and Services/3. systemd and journalctl]] | [[04 - Shell and Text Tools/4. grep, sed, and awk]] | [[Quizzes/Quiz 1 - Fundamentals]]

---

## Section A — True or False

> [!question] 1. The `kill -9 <pid>` command can be caught and handled by the process.
>> [!success]- Answer
>> **False.**
>> SIGKILL (9) cannot be caught, blocked, or ignored. The kernel terminates the process immediately. This is why `kill -9` always works (unless the process is in uninterruptible sleep, state `D`).

> [!question] 2. Every process has a parent process (except PID 1).
>> [!success]- Answer
>> **True.**
>> Every process is created by `fork()` from a parent. The PPID field in `/proc/<pid>/status` shows the parent. PID 1 (systemd) is the only process without a parent (it is started by the kernel).

> [!question] 3. The `Ctrl+Z` keyboard shortcut sends SIGKILL to the foreground process.
>> [!success]- Answer
>> **False.**
>> Ctrl+Z sends SIGTSTP (terminal stop), which suspends the process. The process is paused but still exists; resume it with `bg` (background) or `fg` (foreground). Ctrl+C sends SIGINT (interrupt); `kill -9` sends SIGKILL.

> [!question] 4. The `chmod 644 file.txt` command gives the owner read and write permissions, and gives group and others read-only.
>> [!success]- Answer
>> **True.**
>> 6 = rw- (owner), 4 = r-- (group), 4 = r-- (others). So `644` = `rw-r--r--`. This is the standard permission for regular files (world-readable, only owner can modify).

> [!question] 5. In a pipeline `A | B | C`, the exit code of the pipeline is the exit code of A.
>> [!success]- Answer
>> **False.**
>> By default, the exit code of a pipeline is the exit code of the **last** command (C). To make the pipeline fail if any stage fails, use `set -o pipefail`. To see each stage's exit code, use the `PIPESTATUS` array.

> [!question] 6. `sed -i` modifies the file in place, with no backup by default.
>> [!success]- Answer
>> **True.**
>> `sed -i 's/old/new/g' file.txt` modifies `file.txt` directly. Use `sed -i.bak` to save a backup as `file.txt.bak`. Always test `sed` without `-i` first to verify the output.

> [!question] 7. The `awk` command splits each line into fields using whitespace by default.
>> [!success]- Answer
>> **True.**
>> Default field separator is whitespace (any sequence of spaces or tabs). Use `-F,` for comma-separated, `-F:` for colon-separated, `-F'\t'` for tab-separated.

> [!question] 8. The `find . -name "*.py"` command searches for files ending in `.py` in the current directory and all subdirectories.
>> [!success]- Answer
>> **True.**
>> `find` recursively walks the directory tree by default. `.` is the starting directory; `-name "*.py"` is the pattern (must be quoted to prevent shell glob expansion).

---

## Section B — Multiple Choice

> [!question] 9. What does the `ps aux` command show?
> a) Only the current user's processes
> b) All processes on the system, BSD-style
> c) Only running processes (not sleeping)
> d) Processes in the current shell
>> [!success]- Answer
>> **b) All processes on the system, BSD-style.**
>> `ps aux` shows every process on the system, with BSD-style columns (USER, PID, %CPU, %MEM, VSZ, RSS, TTY, STAT, START, TIME, COMMAND). `ps -ef` is the System V-style equivalent.

> [!question] 10. Which command would you use to run a command as root for the first time, when you have sudo privileges?
> a) `su root`
> b) `sudo command`
> c) `login root`
> d) `exec root command`
>> [!success]- Answer
>> **b) `sudo command`.**
>> `sudo` runs a single command as root, prompting for YOUR password (not root's). `su root` requires root's password (which should be disabled on modern systems).

> [!question] 11. What is the default `PATH` separator on Linux?
> a) `;` (semicolon)
> b) `:` (colon)
> c) `,` (comma)
> d) `|` (pipe)
>> [!success]- Answer
>> **b) `:` (colon).**
>> PATH is a colon-separated list of directories: `/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin`. (On Windows, it is `;`.)

> [!question] 12. Which `grep` flag performs case-insensitive search?
> a) `-v`
> b) `-i`
> c) `-c`
> d) `-n`
>> [!success]- Answer
>> **b) `-i`.**
>> `-i` makes the search case-insensitive (so `grep -i error` matches "ERROR", "Error", "error"). `-v` inverts the match (lines NOT matching); `-c` counts matches; `-n` shows line numbers.

> [!question] 13. Which command extracts the second column of a comma-separated file?
> a) `cut -d, -f2 file.csv`
> b) `awk -F, '{print $2}' file.csv`
> c) Both a and b
> d) `sed -d, -c2 file.csv`
>> [!success]- Answer
>> **c) Both a and b.**
>> Both `cut -d, -f2 file.csv` and `awk -F, '{print $2}' file.csv` extract the second column of a CSV. `cut` is simpler; `awk` is more powerful (can do arithmetic, conditions, etc.).

> [!question] 14. Which `tar` flag creates a gzip-compressed archive?
> a) `tar cjf`
> b) `tar czf`
> c) `tar cJf`
> d) `tar cf`
>> [!success]- Answer
>> **b) `tar czf`.**
>> `z` = gzip compression (`.tar.gz` or `.tgz`). `j` = bzip2 (`.tar.bz2`). `J` = xz (`.tar.xz`). No compression flag = plain `.tar` (uncompressed).

> [!question] 15. Which file is sourced when you open a new terminal (non-login shell) on Ubuntu?
> a) `~/.bash_profile`
> b) `~/.bash_login`
> c) `~/.profile`
> d) `~/.bashrc`
>> [!success]- Answer
>> **d) `~/.bashrc`.**
>> Interactive non-login shells (like opening a new terminal in a GUI) source `~/.bashrc`. Login shells (SSH, `su -`) source `~/.bash_profile` (or `~/.bash_login` or `~/.profile`). Most users put customizations in `~/.bashrc` and have `~/.bash_profile` source it.

> [!question] 16. Which command searches for files modified in the last 7 days?
> a) `find . -mtime 7`
> b) `find . -mtime -7`
> c) `find . -mtime +7`
> d) `find . -mmin 7`
>> [!success]- Answer
>> **b) `find . -mtime -7`.**
>> `-mtime -7` means "modified less than 7 days ago." `-mtime 7` means "modified exactly 7 days ago." `-mtime +7` means "modified more than 7 days ago." `-mmin` uses minutes instead of days.

> [!question] 17. The `>>` operator in shell does what?
> a) Redirects STDOUT to a file, overwriting
> b) Redirects STDOUT to a file, appending
> c) Redirects STDIN from a file
> d) Pipes the output to another command
>> [!success]- Answer
>> **b) Redirects STDOUT to a file, appending.**
>> `>` overwrites the file (truncates first). `>>` appends to the file (creates if it does not exist). `<` redirects STDIN from a file. `|` pipes output to another command.

---

## Section C — Scenario-Based

> [!question] 18. You have a log file `/var/log/app.log` with millions of lines. You want to find the top 10 IP addresses that appear in the file. How?
>> [!success]- Answer
>> Assuming the IP address is the first field on each line:
>> ```bash
>> awk '{print $1}' /var/log/app.log | sort | uniq -c | sort -rn | head -10
>> ```
>> Step by step:
>> 1. `awk '{print $1}'` extracts the first field (the IP).
>> 2. `sort` sorts the IPs alphabetically (so identical IPs are adjacent).
>> 3. `uniq -c` counts consecutive identical lines (producing `count IP`).
>> 4. `sort -rn` sorts numerically, reverse order (highest count first).
>> 5. `head -10` takes the top 10.
>>
>> If the IP is in a more complex position, you might use a regex:
>> ```bash
>> grep -oE '\b[0-9]{1,3}(\.[0-9]{1,3}){3}\b' /var/log/app.log | sort | uniq -c | sort -rn | head -10
>> ```

> [!question] 19. You want to schedule a backup script `/usr/local/bin/backup.sh` to run every day at 2 AM. Write the cron entry and explain each field.
>> [!success]- Answer
>> ```cron
>> 0 2 * * * /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1
>> ```
>> Fields:
>> - `0` — minute (top of the hour).
>> - `2` — hour (2 AM, 24-hour clock).
>> - `*` — day of month (every day).
>> - `*` — month (every month).
>> - `*` — day of week (every day of the week).
>> - `/usr/local/bin/backup.sh` — the command (absolute path, because cron has a minimal PATH).
>> - `>> /var/log/backup.log 2>&1` — append STDOUT and STDERR to a log file.
>>
>> Add this with `crontab -e` (for personal) or to `/etc/cron.d/backup` (for system-wide, with a user column: `0 2 * * * root /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1`).

> [!question] 20. A user complains they cannot write to `/shared`, even though they are in the `developers` group which owns the directory. The permissions are `drwxr-xr-x`. What is wrong, and how do you fix it?
>> [!success]- Answer
>> **The problem:** The directory permissions are `drwxr-xr-x` (755). The owner (root or whoever) has `rwx`, but the group has only `r-x` — no write. So members of the `developers` group cannot add or remove files.
>>
>> **The fix:** Give the group write permission:
>> ```bash
>> sudo chmod g+w /shared
>> # Now permissions are drwxrwxr-x (775)
>> ```
>>
>> **Bonus — set the setgid bit so new files inherit the `developers` group:**
>> ```bash
>> sudo chmod g+s /shared
>> # Now permissions are drwxrwsr-x (2775)
>> # Files created in /shared will have group "developers" (not the creator's primary group)
>> ```
>>
>> **Verify the user is in the group:**
>> ```bash
>> id alice
>> # Should list "developers" in the groups
>> ```
>> If not, add them: `sudo usermod -aG developers alice` (they must log out and back in).

---

## Section D — Fill in the Blank

> [!question] 21. The signal sent by `Ctrl+C` is **__________** (number **__________**).
>> [!success]- Answer
>> SIGINT, number 2.

> [!question] 22. The `find` flag that runs a command on each matched file is **__________**.
>> [!success]- Answer
>> `-exec` (followed by `command {} \;` for one invocation per file, or `command {} +` for one invocation with all files).

> [!question] 23. The `sed` command to replace all occurrences of "foo" with "bar" in a file is **__________**.
>> [!success]- Answer
>> `sed 's/foo/bar/g' file.txt` (or `sed -i 's/foo/bar/g' file.txt` for in-place editing).

> [!question] 24. The systemd command to show all active timers is **__________**.
>> [!success]- Answer
>> `systemctl list-timers` (add `--all` to include inactive timers).

> [!question] 25. The `grep` flag to recursively search files in a directory is **__________**.
>> [!success]- Answer
>> `-r` (or `-R` for following symlinks). Example: `grep -r "error" /var/log/`.

---

Related: [[03 - Processes and Services/1. Processes and the Process Tree]] | [[04 - Shell and Text Tools/4. grep, sed, and awk]] | [[08 - Automation/1. Cron and systemd Timers]] | [[Quizzes/Quiz 1 - Fundamentals]]
