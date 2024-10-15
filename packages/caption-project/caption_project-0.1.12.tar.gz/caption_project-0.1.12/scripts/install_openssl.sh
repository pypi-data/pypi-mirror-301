#!/bin/bash

# Function to install OpenSSL
install_openssl() {
    if [ -f /etc/arch-release ]; then
        # Arch Linux
        pacman -Sy --noconfirm openssl
    elif [ -f /etc/debian_version ]; then
        if [ -f /etc/lsb-release ] && grep -q "Ubuntu" /etc/lsb-release; then
            # Ubuntu
            apt-get update
            apt-get install -y openssl
        else
            # Debian
            apt-get update
            apt-get install -y openssl
        fi
    elif [ -f /etc/fedora-release ]; then
        # Fedora
        dnf install -y openssl
    elif [ -f /etc/alpine-release ]; then
        # Alpine Linux
        apk add --no-cache openssl
    elif [ -f /etc/SuSE-release ] || [ -f /etc/os-release ] && grep -q "ID=opensuse" /etc/os-release; then
        # openSUSE
        zypper install -y openssl
    else
        echo "Unsupported distribution"
        # exit 1
    fi
}

# Main script
echo "Installing OpenSSL..."
install_openssl

if [ $? -eq 0 ]; then
    echo "OpenSSL installed successfully"
else
    echo "Failed to install OpenSSL"
    # exit 1
fi

# Verify installation
openssl version

exit 0