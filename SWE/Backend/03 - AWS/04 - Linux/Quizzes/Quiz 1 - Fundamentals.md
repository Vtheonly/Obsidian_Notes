# Quiz 1 - Linux Fundamentals

> [!info] About This Quiz
> This quiz covers the foundational Linux topics: filesystem hierarchy, paths, permissions, and basic commands. Try to answer before revealing.

Related: [[01 - Installing Apps/1. Linux Overview and Distributions]] | [[01 - Installing Apps/3. The Filesystem Hierarchy Standard]] | [[02 - File System and Permissions/2. Permissions and Ownership]] | [[Quizzes/Quiz 2 - Processes and Shell]]

---

## Section A — True or False

> [!question] 1. The Linux kernel is the same thing as a Linux distribution.
>> [!success]- Answer
>> **False.**
>> The kernel is the core program that talks to hardware. A distribution is a complete OS built around the kernel — it adds the package manager, userspace tools, init system, shell, and libraries. Ubuntu, Fedora, and Alpine are distributions; they all use the Linux kernel but differ in everything else.

> [!question] 2. `/etc` is where configuration files live.
>> [!success]- Answer
>> **True.**
>> Per the Filesystem Hierarchy Standard, `/etc` contains system-wide configuration files (plain text). Examples: `/etc/passwd`, `/etc/nginx/nginx.conf`, `/etc/ssh/sshd_config`, `/etc/fstab`.

> [!question] 3. `/tmp` files persist across reboots.
>> [!success]- Answer
>> **False.**
>> `/tmp` is cleared on reboot (on most distros). For temporary files that should survive reboot, use `/var/tmp`. Never store anything important in `/tmp`.

> [!question] 4. The `chmod 755 file` command gives the owner read, write, and execute permissions, and gives group and others read and execute.
>> [!success]- Answer
>> **True.**
>> 7 = rwx (owner), 5 = r-x (group), 5 = r-x (others). So `755` = `rwxr-xr-x`. Common for executables and directories.

> [!question] 5. A hard link can point to a file on a different filesystem.
>> [!success]- Answer
>> **False.**
>> Hard links point to inodes, and inode numbers are per-filesystem. You cannot hard-link across filesystem boundaries. Use a symbolic link instead.

> [!question] 6. The `sudo` command caches your password for 15 minutes (by default) so you do not have to re-enter it for subsequent `sudo` commands.
>> [!success]- Answer
>> **True.**
>> After you enter your password for `sudo`, subsequent `sudo` commands within 15 minutes (configurable) do not re-prompt. Use `sudo -k` to clear the cache and force re-prompt.

> [!question] 7. The `/etc/shadow` file is world-readable.
>> [!success]- Answer
>> **False.**
>> `/etc/shadow` contains password hashes and is only readable by root. `/etc/passwd` is world-readable (it contains user info but only an `x` placeholder for the password).

> [!question] 8. The `journalctl` command shows logs collected by systemd.
>> [!success]- Answer
>> **True.**
>> systemd collects logs from all services into a central journal. `journalctl` is the viewer. Use `journalctl -u <service>` to filter by service, `journalctl -f` to follow live.

---

## Section B — Multiple Choice

> [!question] 9. Which directory contains user home directories?
> a) `/etc`
> b) `/var`
> c) `/home`
> d) `/usr`
>> [!success]- Answer
>> **c) `/home`.**
>> Each regular user has a directory under `/home` (e.g., `/home/alice`). The root user's home directory is `/root` (not `/home/root`).

> [!question] 10. What is the meaning of `drwxr-xr-x`?
> a) A regular file; owner can read/write, group and others can read.
> b) A directory; owner can list/add/remove files, group and others can list and `cd` in.
> c) A symlink; everyone can read.
> d) A device file; only root can access.
>> [!success]- Answer
>> **b) A directory; owner can list/add/remove files, group and others can list and `cd` in.**
>> The leading `d` means directory. `rwx` for owner (full access), `r-x` for group and others (can list and `cd` in, but cannot add/remove files).

> [!question] 11. Which command would you use to find which package installed `/usr/bin/curl`?
> a) `which curl`
> b) `dpkg -S /usr/bin/curl`
> c) `find /usr/bin/curl`
> d) `locate curl`
>> [!success]- Answer
>> **b) `dpkg -S /usr/bin/curl`** (on Debian/Ubuntu).
>> `dpkg -S <path>` searches the package database for which package owns the file. On Fedora/RHEL, the equivalent is `rpm -qf /usr/bin/curl`.
>> `which curl` only tells you where the `curl` command is found in PATH — not which package installed it.

> [!question] 12. What does `chmod 1777 /shared` do?
> a) Sets permissions to rwxrwxrwx, no special bits.
> b) Sets the sticky bit; only file owners can delete their own files in /shared.
> c) Sets the setuid bit; the directory runs as root.
> d) Makes the directory read-only.
>> [!success]- Answer
>> **b) Sets the sticky bit; only file owners can delete their own files in /shared.**
>> The `1` prefix is the sticky bit. The `777` is rwxrwxrwx (everyone can write). With the sticky bit, users can create files but can only delete their own. This is the permission pattern on `/tmp`.

> [!question] 13. Which file stores the system's static hostname-to-IP mappings (overriding DNS)?
> a) `/etc/resolv.conf`
> b) `/etc/hosts`
> c) `/etc/hostname`
> d) `/etc/networks`
>> [!success]- Answer
>> **b) `/etc/hosts`.**
>> `/etc/hosts` is checked before DNS. If `10.0.0.42 myapp.com` is in `/etc/hosts`, every request to `myapp.com` goes to `10.0.0.42`, regardless of what DNS says. `/etc/resolv.conf` configures the DNS resolver (which servers to query).

> [!question] 14. Which signal does `Ctrl+C` send to the foreground process?
> a) SIGKILL (9)
> b) SIGTERM (15)
> c) SIGINT (2)
> d) SIGHUP (1)
>> [!success]- Answer
>> **c) SIGINT (2).**
>> Ctrl+C sends SIGINT (interrupt). Most applications handle SIGINT by cleaning up and exiting. SIGTERM (15) is what `kill <pid>` sends by default. SIGKILL (9) is force kill (cannot be caught).

> [!question] 15. What is PID 1 on a modern Linux system?
> a) The kernel
> b) The shell
> c) systemd (the init system)
> d) The first user process
>> [!success]- Answer
>> **c) systemd (the init system).**
>> When the kernel boots, it starts a single process: PID 1, which is the init system. On most modern Linux distributions, this is systemd. PID 1 is responsible for starting all other services and reaping orphaned zombie processes.

> [!question] 16. Which command shows TCP listening sockets along with the process name?
> a) `netstat -tln`
> b) `ss -tlnp`
> c) `lsof -i`
> d) All of the above
>> [!success]- Answer
>> **d) All of the above.**
>> All three commands can show listening TCP sockets. `ss -tlnp` is the modern preferred tool (it replaced `netstat`). `lsof -i` shows all network connections (listening and established). `netstat -tlnp` is the older alternative (deprecated).

> [!question] 17. Which file defines filesystems that should be mounted at boot?
> a) `/etc/mtab`
> b) `/etc/fstab`
> c) `/etc/mounts`
> d) `/proc/mounts`
>> [!success]- Answer
>> **b) `/etc/fstab`.**
>> `/etc/fstab` defines persistent mounts. `/etc/mtab` and `/proc/mounts` show currently mounted filesystems (runtime state, not configuration).

---

## Section C — Scenario-Based

> [!question] 18. You try to SSH into a server and get "Permission denied (publickey)." You have a key at `~/.ssh/id_ed25519`. What are the most likely causes?
>> [!success]- Answer
>> **Cause 1: Public key not in the server's `~/.ssh/authorized_keys`.**
>> You must copy your public key (`id_ed25519.pub`, not the private key!) to `~/.ssh/authorized_keys` on the server. Use `ssh-copy-id alice@server` to do this.
>>
>> **Cause 2: Wrong permissions on `~/.ssh/` or `authorized_keys`.**
>> SSH refuses to use keys if permissions are too open. `~/.ssh` must be `700`, `authorized_keys` must be `600`. Fix with `chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys`.
>>
>> **Cause 3: Wrong username or hostname.**
>> Check `ssh alice@server` vs `ssh alice@server.example.com`.
>>
>> **Cause 4: Password authentication is disabled and you have no key on the server.**
>> Some servers (`PasswordAuthentication no`) require key authentication. Without your public key in `authorized_keys`, you cannot log in.
>>
>> **Cause 5: The key has a passphrase you have not unlocked.**
>> If your private key has a passphrase, you must enter it (or use `ssh-agent`). Forgetting the passphrase means you must regenerate the key.

> [!question] 19. A service named `myapp` fails to start. You run `sudo systemctl start myapp` and get "Job for myapp.service failed." How do you diagnose?
>> [!success]- Answer
>> Step-by-step diagnosis:
>>
>> 1. Check the status:
>>    ```bash
>>    sudo systemctl status myapp
>>    ```
>>    This shows the last few log lines and the exit code.
>>
>> 2. Check the full logs:
>>    ```bash
>>    sudo journalctl -u myapp -n 50 --no-pager
>>    sudo journalctl -u myapp --since "5 minutes ago"
>>    ```
>>
>> 3. Check the unit file:
>>    ```bash
>>    systemctl cat myapp
>>    ```
>>    Look for typos in `ExecStart=`, `User=`, `WorkingDirectory=`.
>>
>> 4. Try running the `ExecStart` command manually:
>>    ```bash
>>    sudo -u myapp /usr/bin/node /opt/myapp/server.js
>>    ```
>>    This often reveals the actual error (missing file, missing env var, etc.).
>>
>> 5. Check dependencies:
>>    ```bash
>>    systemctl list-dependencies myapp
>>    ```
>>    If `myapp` depends on `network.target` and networking is not up, it will fail.
>>
>> 6. Check disk space and inodes:
>>    ```bash
>>    df -h
>>    df -i
>>    ```
>>    A full disk can cause services to fail to start.
>>
>> 7. Check the syntax of the unit file:
>>    ```bash
>>    sudo systemd-analyze verify /etc/systemd/system/myapp.service
>>    ```

> [!question] 20. The `df -h` command shows `/` at 95% full. How do you find what is consuming the space?
>> [!success]- Answer
>> Step 1: Identify the largest top-level directories:
>> ```bash
>> sudo du -sh /* 2>/dev/null | sort -rh | head -10
>> ```
>> Typical culprits: `/var`, `/home`, `/usr`, `/tmp`.
>>
>> Step 2: Drill into the largest one:
>> ```bash
>> sudo du -sh /var/* 2>/dev/null | sort -rh | head -10
>> # If /var/log is big:
>> sudo du -ah /var/log 2>/dev/null | sort -rh | head -20
>> ```
>>
>> Step 3: Find the largest individual files:
>> ```bash
>> sudo find / -xdev -type f -size +500M -exec ls -lh {} \; 2>/dev/null
>> ```
>>
>> Step 4: Check for common disk hogs:
>> ```bash
>> docker system df                       # Docker images/containers
>> sudo du -sh /var/lib/docker            # Docker's storage
>> sudo du -sh /var/log/journal           # systemd journal
>> sudo du -sh /var/cache/apt             # APT cache
>> sudo du -sh ~/.cache                   # user cache
>> ```
>>
>> Step 5: Clean up:
>> ```bash
>> docker system prune -a                 # remove unused Docker resources
>> sudo journalctl --vacuum-size=500M     # limit journal to 500 MB
>> sudo apt clean                          # clean APT cache
>> sudo find /var/log -name "*.gz" -mtime +30 -delete   # delete old rotated logs
>> ```

---

## Section D — Fill in the Blank

> [!question] 21. The directory `/__________` contains system-wide configuration files.
>> [!success]- Answer
>> `/etc`. Per the FHS, `/etc` is for configuration files (plain text).

> [!question] 22. The Linux kernel feature that limits a process's CPU and memory consumption is called **__________**.
>> [!success]- Answer
>> **cgroups** (control groups).

> [!question] 23. The shell command to find files larger than 100 MB in `/var` is **__________**.
>> [!success]- Answer
>> `find /var -type f -size +100M`

> [!question] 24. The file **__________** defines which public keys can log into a user account over SSH.
>> [!success]- Answer
>> `~/.ssh/authorized_keys` (must be `chmod 600`).

> [!question] 25. The `systemctl` command that starts a service at boot is **__________**.
>> [!success]- Answer
>> `sudo systemctl enable <service>` (or `sudo systemctl enable --now <service>` to also start it immediately).

---

Related: [[01 - Installing Apps/1. Linux Overview and Distributions]] | [[02 - File System and Permissions/2. Permissions and Ownership]] | [[03 - Processes and Services/3. systemd and journalctl]] | [[Quizzes/Quiz 2 - Processes and Shell]]
