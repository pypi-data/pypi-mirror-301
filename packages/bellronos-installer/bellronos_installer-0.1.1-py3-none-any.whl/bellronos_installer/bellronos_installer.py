# Copyright (C) 2024 Bellande Architecture Mechanism Research Innovation Center, Ronaldson Bellande

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

#!/usr/bin/env python3

import os
import shutil
import sys
import requests
import argparse
import subprocess
from packaging import version

GITHUB_API_URL = "https://api.github.com/repos/Architecture-Mechanism/bellronos/branches"
GITHUB_RAW_URL = "https://raw.githubusercontent.com/Architecture-Mechanism/bellronos"
BELLRONOS_INSTALL_PATH = "/usr/local/bin/bellronos"

def get_available_versions():
    try:
        response = requests.get(GITHUB_API_URL)
        response.raise_for_status()
        branches = response.json()
        return [branch['name'] for branch in branches]
    except requests.RequestException as e:
        print(f"Error fetching branches: {e}")
        print(f"Response status code: {e.response.status_code if e.response else 'N/A'}")
        print(f"Response content: {e.response.content if e.response else 'N/A'}")
        return []

def download_bellronos(branch):
    url = f"{GITHUB_RAW_URL}/{branch}/executable/bellronos"
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open("bellronos_executable", "wb") as f:
            f.write(response.content)
        return True
    except requests.RequestException as e:
        print(f"Error downloading bellronos from branch {branch}: {e}")
        return False

def setup_bellronos(version=None):
    if version:
        if not download_bellronos(version):
            return
        bellronos_executable = "bellronos_executable"
    else:
        bellronos_executable = "executable/bellronos"
    
    if not os.path.exists(bellronos_executable):
        print(f"Error: {bellronos_executable} not found.")
        return
    
    try:
        shutil.copy2(bellronos_executable, BELLRONOS_INSTALL_PATH)
        os.chmod(BELLRONOS_INSTALL_PATH, 0o755)  # Make it executable
        print(f"bellronos has been copied to {BELLRONOS_INSTALL_PATH}")
    except IOError as e:
        print(f"Error copying file: {e}")
        return
    
    if version:
        os.remove(bellronos_executable)
    
    print("Bellronos has been set up successfully.")

def list_versions():
    versions = get_available_versions()
    if versions:
        print("Available Bellronos versions:")
        for v in versions:
            print(f"- {v}")
    else:
        print("No versions found or unable to fetch versions.")

def install_latest():
    versions = get_available_versions()
    if versions:
        latest = max(versions, key=lambda x: version.parse(x) if x != 'main' else version.parse('0'))
        if latest == 'main':
            print("No versioned branches found. Installing from main branch.")
        else:
            print(f"Installing latest version: {latest}")
        setup_bellronos(latest)
    else:
        print("Unable to determine the latest version. Installing from main branch.")
        setup_bellronos()

def get_current_version():
    try:
        result = subprocess.run([BELLRONOS_INSTALL_PATH, "--version"], capture_output=True, text=True)
        return result.stdout.strip()
    except FileNotFoundError:
        return "Not installed"
    except subprocess.CalledProcessError:
        return "Unknown"

def get_latest_version():
    versions = get_available_versions()
    if versions:
        return max(versions, key=lambda x: version.parse(x) if x != 'main' else version.parse('0'))
    return "main"

def update_bellronos():
    current_version = get_current_version()
    latest_version = get_latest_version()
    
    if current_version == "Not installed":
        print("Bellronos is not installed. Installing the latest version.")
        install_latest()
    elif current_version == "Unknown":
        print("Unable to determine the current version. Proceeding with update.")
        setup_bellronos(latest_version)
    elif current_version == latest_version:
        print(f"bellronos is already up to date (version {current_version}).")
    else:
        print(f"Updating Bellronos from version {current_version} to {latest_version}")
        setup_bellronos(latest_version)

def main():
    if os.geteuid() != 0:
        print("This script must be run with sudo privileges.")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description="Bellronos Setup Script")
    parser.add_argument("action", choices=["install", "list", "latest", "update"],
                        help="Action to perform: install, list versions, install latest, or update")
    parser.add_argument("--version", help="Specify version to install")
    
    args = parser.parse_args()
    
    if args.action == "install":
        if args.version:
            setup_bellronos(args.version)
        else:
            print("Please specify a version to install with --version, or use 'latest' to install the latest version.")
    elif args.action == "list":
        list_versions()
    elif args.action == "latest":
        install_latest()
    elif args.action == "update":
        update_bellronos()

if __name__ == "__main__":
    main()
