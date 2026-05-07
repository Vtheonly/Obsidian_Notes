# dpkg

**dpkg** (Debian Package) is a fundamental command-line tool used in Debian and its derivatives (like Ubuntu) for managing software packages. It operates directly on `.deb` files and serves as the low-level foundation of the Debian package management system. While higher-level tools like APT provide dependency resolution and repository management, dpkg handles the core operations of installing, removing, querying, and configuring individual packages on the system. Understanding dpkg is essential for troubleshooting package issues, working with locally downloaded `.deb` files, and gaining insight into how the Debian package management stack works under the hood.

dpkg was originally created in 1993 and has been a core component of the Debian project ever since. It maintains a database of installed packages in `/var/lib/dpkg/`, which tracks the status, configuration files, and file lists for every package on the system. This database is the single source of truth for what is installed on your system, and both dpkg and APT rely on it for their operations. When you install a package with dpkg, it unpacks the `.deb` file, runs any pre-installation scripts, copies files to their target locations, runs post-installation scripts, and updates the package database accordingly.

## Core dpkg Commands

### Installing a Package: dpkg -i

The `-i` (or `--install`) option is used to install a `.deb` package file. This is the most common dpkg operation when you have downloaded a `.deb` file manually and need to install it:
```bash
sudo dpkg -i package.deb
```
When you run this command, dpkg will unpack the archive, install the files to their target locations, and run any maintainer scripts included in the package. However, dpkg does not automatically resolve dependencies. If the package requires other packages that are not installed, dpkg will report an error and the package may be left in an unconfigured state. You can fix this by running `sudo apt install -f` afterward, which instructs APT to resolve and install any missing dependencies.

Example of a typical installation workflow:
```bash
sudo dpkg -i code_1.85.0_amd64.deb
# If dependency errors occur:
sudo apt install -f
```

### Removing a Package: dpkg -r

The `-r` (or `--remove`) option removes an installed package by its package name (not the `.deb` filename). It removes the package binaries but leaves configuration files behind, which allows you to reinstall the package later without losing your custom configuration:
```bash
sudo dpkg -r package-name
```
For example, to remove the VLC media player while keeping its configuration files:
```bash
sudo dpkg -r vlc
```

### Purging a Package: dpkg -P

The `-P` (or `--purge`) option removes an installed package along with all of its configuration files. This is useful when you want to completely remove a package and start fresh, or when you are trying to free up disk space and do not intend to reinstall the software:
```bash
sudo dpkg -P package-name
```
The difference between `-r` and `-P` is significant: after `-r`, the package is in a "residual config" state and will still appear in the package database. After `-P`, all traces of the package are removed from the system.

### Listing Installed Packages: dpkg -l

The `-l` (or `--list`) option displays a list of all installed packages, along with their status, version, and description. This is one of the most frequently used dpkg commands for getting an overview of what is installed on your system:
```bash
dpkg -l
```
You can filter the output by providing a package name pattern:
```bash
dpkg -l | grep python
dpkg -l firefox*
```
The output includes a two-character status indicator in the first column. Common status codes include:
- `ii` -- properly installed
- `rc` -- removed but configuration files remain (residual config)
- `un` -- not installed

The `rc` status is particularly important to recognize, as it indicates packages that have been removed but not purged. You can clean up these residual packages by running `dpkg -l | grep '^rc'` to identify them and then using `sudo dpkg -P <package>` to purge each one.

### Showing Package Status: dpkg -s

The `-s` (or `--status`) option displays detailed status information about an installed package, including its version, dependencies, maintainer, installed size, and description:
```bash
dpkg -s package-name
```
Example output for the curl package:
```bash
dpkg -s curl
# Package: curl
# Status: install ok installed
# Priority: optional
# Section: web
# Installed-Size: 428
# Maintainer: Ubuntu Developers
# Architecture: amd64
# Version: 7.81.0-1ubuntu1.13
# Depends: libbrotli1, libcurl4 (= 7.81.0-1ubuntu1.13), ...
# Description: command line tool for transferring data with URL syntax
```
This command is extremely useful when you need to verify which version of a package is installed or check its dependency list without connecting to a repository.

### Listing Files Installed by a Package: dpkg -L

The `-L` (or `--listfiles`) option shows all files that were installed on the system by a particular package. This is invaluable for locating configuration files, documentation, and executables associated with a package:
```bash
dpkg -L package-name
```
Example:
```bash
dpkg -L nginx
# /.
# /etc
# /etc/nginx
# /etc/nginx/nginx.conf
# /usr/sbin/nginx
# /usr/share/doc/nginx
# ...
```

### Finding Which Package Owns a File: dpkg -S

The `-S` (or `--search`) option searches for the package that owns a specific file on your system. This is particularly useful when you encounter a file and want to know which package installed it:
```bash
dpkg -S /usr/bin/curl
# Output: curl: /usr/bin/curl

dpkg -S nginx.conf
# Output: nginx-core: /etc/nginx/nginx.conf
```
This command helps you trace any file back to its owning package, which is essential for understanding software dependencies and resolving file conflicts between packages.

## Relationship Between dpkg and APT

dpkg and APT work together as complementary layers of the Debian package management system. The relationship can be understood as follows:

- **dpkg** is the low-level tool that handles the mechanical operations of installing, removing, and querying individual packages. It works directly with `.deb` files and the local package database. dpkg does not understand repositories, does not download packages from the internet, and does not resolve dependencies automatically.

- **APT** is the high-level tool that provides repository management, dependency resolution, and package downloading. When you run `sudo apt install package-name`, APT calculates the full dependency tree, downloads all required `.deb` files from repositories, and then invokes dpkg to perform the actual installation.

In practice, you should use APT for most package management tasks because it handles dependencies automatically. Use dpkg directly when you need to install a locally available `.deb` file, inspect package details, troubleshoot package issues, or perform operations that APT does not expose. See [[6 - Understanding APT]] in Installing in Linux for a comprehensive guide to APT.

## Troubleshooting Common dpkg Issues

### Broken Packages

When dpkg reports that a package is in a broken state (often due to interrupted installations or unresolved dependencies), you can attempt to fix the issue with:
```bash
sudo dpkg --configure -a
sudo apt install -f
```
The `--configure -a` option tells dpkg to configure any packages that have been unpacked but not yet configured. The `apt install -f` command instructs APT to fix broken dependencies.

### Lock File Issues

If dpkg reports that it cannot acquire a lock, it usually means another package management process is running in the background. You should wait for the other process to finish. If the lock persists after the other process has ended (which can happen after a crash), you may need to remove the lock files manually:
```bash
sudo rm /var/lib/dpkg/lock-frontend
sudo rm /var/lib/dpkg/lock
sudo dpkg --configure -a
```
Removing lock files should only be done as a last resort, as it can lead to database corruption if another process is legitimately using the lock.

### Reconfiguring an Installed Package

If you need to re-run the initial configuration prompts for a package (for example, to change the default settings that were presented during installation), you can use:
```bash
sudo dpkg-reconfigure package-name
```
This command re-executes the package's configuration scripts, allowing you to modify settings such as default ports, service behavior, or locale preferences.
