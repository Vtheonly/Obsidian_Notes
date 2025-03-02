## Location of Apps Installed from the Terminal
When you install applications using the terminal, particularly with package managers like **APT** (for Debian-based systems like Ubuntu), the applications are typically installed in standard system directories:

- **Executable Binaries**: These are usually located in directories like:
  - `/usr/bin/`: This directory contains the majority of executable files accessible to all users.
  - `/usr/local/bin/`: Used for installing software locally on the machine, often for custom software or software that isn’t managed by the system’s package manager.
  
- **Configuration Files**: Configuration files for applications are often stored in:
  - `/etc/`: This directory contains system-wide configuration files.
  
- **Library Files**: Shared libraries that applications depend on are typically located in:
  - `/usr/lib/` or `/usr/local/lib/`.

- **User-specific Applications**: If you install applications specifically for your user account (using `--user` with pip, for example), they may be located in:
  - `~/.local/bin/`: For user-installed binaries.