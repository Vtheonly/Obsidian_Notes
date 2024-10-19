

**dpkg** (Debian Package) is a fundamental command-line tool used in Debian and its derivatives (like Ubuntu) for managing software packages. It operates directly on `.deb` files and provides essential functionalities, including:

- **Installation**: Install software packages using `.deb` files with `dpkg -i package.deb`.
- **Removal**: Uninstall packages using `dpkg -r package-name`.
- **Information Retrieval**: Get details about installed packages using `dpkg -l` to list packages or `dpkg -s package-name` for specific information.

While dpkg handles individual packages, it does not automatically resolve dependencies. This is typically managed by higher-level tools like APT (Advanced Package Tool), which streamline the installation process and manage package repositories.
