# Location of Apps Installed from the Terminal

When you install applications using the terminal, particularly with package managers like APT (for Debian-based systems such as Ubuntu), the applications and their associated files are distributed across several standard system directories. This organized approach follows the Filesystem Hierarchy Standard (FHS), which defines the purpose and structure of each directory in a Linux filesystem. Understanding where installed applications are placed helps you locate executables, configuration files, libraries, and documentation, which is essential for system administration, troubleshooting, and development.

The separation of executables, configuration files, libraries, and documentation into distinct directories is a deliberate design choice that offers several advantages. It allows multiple applications to share common libraries without duplication, makes it straightforward to back up or modify configuration files independently of the application binaries, and ensures that the system remains organized even when hundreds of packages are installed. This structure also supports the principle of least privilege, as different directories can have different permission requirements.

## Executable Binary Directories

When you install an application through the terminal, the main executable is placed in one of several directories, each serving a specific purpose within the filesystem hierarchy:

### /bin/

The `/bin/` directory contains essential user command binaries that must be available even when the system is in single-user mode. These are fundamental utilities required for basic system operation, such as `ls`, `cp`, `mv`, `cat`, and `bash`. In modern Ubuntu and many other distributions, `/bin/` is actually a symbolic link to `/usr/bin/`, reflecting a historical merge of these directories. Applications installed via APT generally do not place their executables directly in `/bin/` unless they are considered essential for system boot and repair.

### /sbin/

The `/sbin/` directory holds system administration binaries that are typically used by the root user. Commands like `fdisk`, `ifconfig`, `iptables`, and `systemctl` reside here. Like `/bin/`, this directory is often a symlink to `/usr/sbin/` on modern distributions. Regular users can still execute commands from `/sbin/` if they have the appropriate permissions, but these tools are generally not needed for day-to-day use.

### /usr/bin/

The `/usr/bin/` directory is the primary location for user-facing executables installed by the system package manager. When you run `sudo apt install <package>`, the resulting binary is almost always placed here. This directory contains the vast majority of installed applications and tools, including compilers, interpreters, text editors, web browsers, and productivity software. It is always included in the default PATH environment variable, so any executable placed here can be invoked directly from the command line without specifying the full path.

### /usr/sbin/

The `/usr/sbin/` directory contains non-essential system administration binaries. These are tools that are not required for basic system operation but are needed for system management tasks, such as web server daemons, database servers, and network services. Applications like `apache2`, `nginx`, and `mysql` typically place their daemon executables here.

### /usr/local/bin/

The `/usr/local/bin/` directory is used for locally installed software that is managed outside the distribution's package manager. If you compile software from source and run `sudo make install`, the resulting binaries will typically be placed here. This directory is intentionally kept separate from `/usr/bin/` so that locally compiled software does not conflict with or overwrite packages managed by APT. Like `/usr/bin/`, this directory is included in the default PATH.

### /opt/

The `/opt/` directory is intended for the installation of add-on software packages from third-party vendors. Some commercial or proprietary applications install their entire directory structure under `/opt/`, including their own `bin/`, `lib/`, and `share/` subdirectories. Examples include Google Chrome (which installs to `/opt/google/chrome/`) and some Oracle products. To run applications installed in `/opt/`, you typically need to add their `bin/` directory to your PATH or create symbolic links in `/usr/local/bin/`.

## Configuration Files

Configuration files for applications are stored separately from the executables, which allows administrators to modify settings without touching the binary files:

- **/etc/**: This directory contains system-wide configuration files. Nearly every application installed via APT places its configuration files in a subdirectory under `/etc/`. For example, Nginx uses `/etc/nginx/`, SSH uses `/etc/ssh/`, and so on. These files often require root privileges to modify.
- **~/.config/**: User-specific configuration files are stored in the user's home directory under `~/.config/`. This follows the XDG Base Directory Specification and allows individual users to customize application behavior without affecting other users.

## Library Files

Shared libraries that applications depend on are stored in dedicated directories to facilitate sharing and reduce duplication:

- **/usr/lib/**: Contains shared libraries required by applications installed in `/usr/bin/` and `/usr/sbin/`. These library files typically have the `.so` (shared object) extension.
- **/usr/local/lib/**: Contains libraries for locally compiled software installed in `/usr/local/bin/`.

## The PATH Environment Variable

The PATH environment variable is a colon-separated list of directories that the shell searches through when you type a command. Understanding PATH is critical for knowing why some executables can be invoked by name while others require their full path. You can inspect your current PATH with:

```bash
echo $PATH
# Output: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

When you type a command like `python3`, the shell searches through each directory in PATH from left to right and executes the first matching binary it finds. This means that if you have two versions of a program installed in different directories, the one that appears earlier in PATH takes precedence. You can add a custom directory to your PATH by adding a line like the following to your shell configuration file (`~/.bashrc` or `~/.zshrc`):

```bash
export PATH="$PATH:/my/custom/directory"
```

## How to Find Where an App Is Installed

There are several ways to locate where an application is installed on your system. The `which` command shows the full path of the executable that will be run when you type a command name. The `whereis` command provides a broader search, returning the locations of the binary, source, and manual pages. The `dpkg -L <package-name>` command lists all files installed by a specific package, which is useful for finding configuration files and documentation in addition to the main executable. See [[0 - dpkg]] in Tools and Commands for more details on using dpkg to inspect installed packages.

```bash
which firefox
# Output: /usr/bin/firefox

whereis firefox
# Output: firefox: /usr/bin/firefox /usr/lib/firefox /usr/share/man/man1/firefox.1

dpkg -L firefox
# Lists all files installed by the firefox package
```
