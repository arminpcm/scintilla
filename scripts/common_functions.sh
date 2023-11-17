#!/bin/bash

################################################################################
# Title: Common shell functions that can be used by other scripts
# 
# Copyright (c) 2023 Scintilla. All rights reserved.
#
# The contents of this script are proprietary and confidential. Unauthorized
# reproduction, distribution, or disclosure of this material is strictly
# prohibited without the express written permission of Scintilla.
#
################################################################################

# Colors
# Reset
RESET='\033[0m'       # Text Reset
# Regular Colors
BLACK='\033[0;30m'    # Black
RED='\033[0;31m'      # Red
GREEN='\033[0;32m'    # Green
YELLOW='\033[0;33m'   # Yellow
BLUE='\033[0;34m'     # Blue
PURPLE='\033[0;35m'   # Purple
CYAN='\033[0;36m'     # Cyan
WHITE='\033[0;37m'    # White

# Function to print an error message
function error() {
    echo -e "${RED}[Error]: $1${RESET}"
}

# Function to print a warning message
function warning() {
    echo -e "${YELLOW}[Warning]: $1${RESET}"
}

# Function to print a very light blue info message
function info() {
    echo -e "${CYAN}[Info]: $1${RESET}"
}

# Function to check if the script is run as root
function check_root() {
    if [ "$EUID" -ne 0 ]; then
        error "Script must be run as root."
        return 1
    fi
    return 0
}

# Function to ask yes/no question and return the value
function ask_yes_no() {
    read -p "${GREEN}$1 (y/n): ${RESET}" response
    case "$response" in
        [yY]|[yY][eE][sS]) return 0 ;;
        *) return 1 ;;
    esac
}

# Get the current date and time
function current_datetime() {
    date +"%Y-%m-%d %H:%M:%S"
}

# Get the parent directory of a running shell script
get_script_parent_directory() {
    # Get the directory containing the script
    script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    
    # Get the parent directory
    parent_dir="$(dirname "$script_dir")"
    eval "$1=${parent_dir}"
}

print_header() {
    echo -e "${PURPLE}"
    echo "      .--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--."
    echo "     / .. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\"
    echo "     \\ \\/\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \\/ /"
    echo "     \\/ /\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\\/ /"
    echo "     / /\\    ________   ________   ___   ________    _________   ___   ___        ___        ________        / /\\"
    echo "     / /\\ \\  |\\   ____\\ |\\   ____\\ |\\  \\ |\\   ___  \\ |\\___   ___\\|\\  \\ |\\  \\      |\\  \\      |\\   __  \\      / /\\ \\"
    echo "     \\ \\/ /  \\ \\  \\___|_\\ \\  \\___| \\ \\  \\\\ \\  \\\\ \\  \\\\|___ \\  \\_|\\ \\  \\\\ \\  \\     \\ \\  \\     \\ \\  \\|\\  \\     \\ \\/ /"
    echo "     \\/ /    \\ \\_____  \\\\ \\  \\     \\ \\  \\\\ \\  \\\\ \\  \\    \\ \\  \\  \\ \\  \\\\ \\  \\     \\ \\  \\     \\ \\   __  \\     \\/ /"
    echo "     / /\\     \\|____|\\  \\\\ \\  \\____ \\ \\  \\\\ \\  \\\\ \\  \\    \\ \\  \\  \\ \\  \\\\ \\  \\____ \\ \\  \\____ \\ \\  \\ \\  \\    / /\\"
    echo "     / /\\ \\      ____\\_\\  \\\\ \\_______\\\\ \\__\\\\ \\__\\\\ \\__\\    \\ \\__\\  \\ \\__\\\\ \\_______\\\\ \\_______\\\\ \\__\\ \\__\\  / /\\ \\"
    echo "     \\ \\/ /     |\\_________\\\\|_______| \\|__| \\|__| \\|__|     \\|__|   \\|__| \\|_______| \\|_______| \\|__|\\|__|  \\ \\/ /"
    echo "     \\/ /      \\|_________|                                                                                  \\/ /"
    echo "     / /\\.--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--./ /\\"
    echo "     / /\\ \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\/\\ \\"
    echo "     \\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`'\\ \`' /"
    echo "     \`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'\`--'"
    echo -e "${RESET}"
}
