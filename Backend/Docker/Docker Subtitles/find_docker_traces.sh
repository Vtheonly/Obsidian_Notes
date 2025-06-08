#!/bin/bash

echo "============================================================"
echo "Docker Component & Configuration Identification Script"
echo "This script is for IDENTIFICATION ONLY and does NOT delete anything."
echo "Review output carefully. Some results might be false positives."
echo "============================================================"
echo ""
echo "Press Enter to continue..."
read

# Function to print a header for each section
print_header() {
    echo ""
    echo "------------------------------------------------------------"
    echo "$1"
    echo "------------------------------------------------------------"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 1. Core Docker Engine and Components
print_header "1. Core Docker Engine & Components (System-wide)"
echo "Docker Daemon Data Directory (/var/lib/docker/):"
sudo ls -ld /var/lib/docker/ 2>/dev/null || echo "  Not found or no permission."
echo ""
echo "containerd Data Directory (/var/lib/containerd/):"
sudo ls -ld /var/lib/containerd/ 2>/dev/null || echo "  Not found or no permission."
echo ""
echo "Docker Configuration Directory (/etc/docker/):"
sudo ls -l /etc/docker/ 2>/dev/null || echo "  Not found or no permission."
echo ""
echo "Docker Socket (/var/run/docker.sock):"
ls -l /var/run/docker.sock 2>/dev/null || echo "  Not found."
echo ""
echo "Systemd Service Files:"
echo "  docker.service:"
ls -l /lib/systemd/system/docker.service /etc/systemd/system/docker.service.d/* /etc/systemd/system/docker.service 2>/dev/null || echo "    Not found."
echo "  docker.socket:"
ls -l /lib/systemd/system/docker.socket /etc/systemd/system/docker.socket.d/* /etc/systemd/system/docker.socket 2>/dev/null || echo "    Not found."
echo "  containerd.service:"
ls -l /lib/systemd/system/containerd.service /etc/systemd/system/containerd.service.d/* /etc/systemd/system/containerd.service 2>/dev/null || echo "    Not found."
echo ""
echo "Executables (Binaries):"
for cmd in docker docker-compose docker-buildx containerd runc; do
    echo -n "  $cmd: "
    command_exists $cmd && which $cmd || echo "Not found in PATH."
done

# 2. Docker Desktop Specific Locations
print_header "2. Docker Desktop Specific Locations"
echo "Possible Docker Desktop Installation Directory (/opt/docker-desktop):"
ls -ld /opt/docker-desktop 2>/dev/null || echo "  Not found."
echo ""
echo "User-Specific Configuration for Docker Desktop (~/.docker/desktop/):"
ls -ld ~/.docker/desktop/ 2>/dev/null || echo "  Not found."
echo ""
echo "Docker Desktop CLI Helper (/usr/local/bin/com.docker.cli):"
ls -l /usr/local/bin/com.docker.cli 2>/dev/null || echo "  Not found."
echo ""
echo "Application Launcher (.desktop files):"
ls -l /usr/share/applications/*docker-desktop*.desktop ~/.local/share/applications/*docker-desktop*.desktop 2>/dev/null || echo "  Not found."

# 3. User-Specific Docker CLI Configuration
print_header "3. User-Specific Docker CLI Configuration (~/.docker/)"
ls -ld ~/.docker/ 2>/dev/null || echo "  Not found."
if [ -d ~/.docker ]; then
    echo "Contents of ~/.docker/:"
    ls -lA ~/.docker/
fi

# 4. APT Package Management Information
print_header "4. APT Package Management Information"
echo "Installed packages matching 'docker', 'containerd', 'runc':"
apt list --installed 2>/dev/null | grep -E -i 'docker|containerd|runc' || echo "  No relevant packages found or apt not available."
echo ""
echo "APT Repository Files (/etc/apt/sources.list.d/):"
ls -l /etc/apt/sources.list.d/*docker* /etc/apt/sources.list.d/*download.docker.com* 2>/dev/null || echo "  No Docker-specific APT sources found."
echo ""
echo "APT GPG Keys (/etc/apt/keyrings/):"
ls -l /etc/apt/keyrings/*docker* 2>/dev/null || echo "  No Docker-specific GPG keys found."

# 5. System Groups
print_header "5. System Groups"
echo "Docker group in /etc/group:"
grep docker /etc/group 2>/dev/null || echo "  'docker' group not found."

# 6. Running Processes
print_header "6. Running Processes"
echo "Processes matching 'docker':"
ps aux | grep -i '[d]ocker' || echo "  No running processes found matching 'docker'." # [d] to avoid grep itself
echo ""
echo "Processes matching 'containerd':"
ps aux | grep -i '[c]ontainerd' || echo "  No running processes found matching 'containerd'."

# 7. Network Configuration (Informational)
print_header "7. Network Configuration (Informational)"
echo "Network interfaces potentially related to Docker (look for 'docker0', 'br-'):"
ip a | grep -E 'docker|br-' || echo "  No obvious Docker network interfaces found."
echo ""
echo "IPTables rules (this can be very long, showing first 20 Docker-related):"
if command_exists iptables; then
    sudo iptables -L -n -v 2>/dev/null | grep -i 'docker' | head -n 20 || echo "  No iptables rules found matching 'docker' or iptables not available."
else
    echo "  iptables command not found."
fi


# 8. Log Files (Showing if systemd journal has entries)
print_header "8. Log Files (Systemd Journal Check)"
echo "Checking Systemd Journal for docker.service (last 5 lines if present):"
if command_exists journalctl; then
    sudo journalctl -u docker.service -n 5 --no-pager 2>/dev/null || echo "  No journal entries for docker.service or journalctl not available."
    echo ""
    echo "Checking Systemd Journal for containerd.service (last 5 lines if present):"
    sudo journalctl -u containerd.service -n 5 --no-pager 2>/dev/null || echo "  No journal entries for containerd.service."
else
    echo "  journalctl command not found."
fi

# 9. General File System Search (can be slow and produce many results)
print_header "9. General File System Search (Examples - CAUTION: Can be slow)"
echo "This section demonstrates 'find' commands. They can be slow and verbose."
echo "Uncomment and run them manually if needed, with caution."
echo ""
echo "# Example: sudo find /etc -name \"*docker*\" -print 2>/dev/null"
echo "# Example: sudo find /var -name \"*docker*\" -print 2>/dev/null"
echo "# Example: find ~ -name \"*docker*\" -print 2>/dev/null"
echo ""
echo "Consider using 'locate' if it's installed and its database is updated ('sudo updatedb')."
echo "# Example: locate docker"

echo ""
echo "============================================================"
echo "Identification script finished."
echo "Remember to review the output carefully."
echo "============================================================"
