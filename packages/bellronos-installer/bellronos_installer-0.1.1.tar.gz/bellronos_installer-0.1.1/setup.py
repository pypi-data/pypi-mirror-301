from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys
import shutil

def post_install():
    # Define the source and destination paths
    src_path = os.path.join(sys.prefix, 'bin', 'bellronos_installer')
    dest_path = '/usr/local/bin/bellronos_installer'

    if os.path.exists(src_path):
        try:
            # Copy the script to /usr/local/bin
            shutil.copy2(src_path, dest_path)
            # Set execute permissions
            os.chmod(dest_path, 0o755)
            print(f"Installed bellronos_installer to {dest_path}")
        except PermissionError:
            print("Error: Unable to copy script to /usr/local/bin. Try running the installation with sudo.")
    else:
        print(f"Warning: Could not find {src_path}")

    # Ensure correct shebang
    if os.path.exists(dest_path):
        with open(dest_path, 'r+') as f:
            content = f.read()
            if not content.startswith('#!/usr/bin/env python3'):
                f.seek(0, 0)
                f.write('#!/usr/bin/env python3\n' + content)

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        post_install()

# Read long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bellronos_installer",
    version="0.1.1",
    description="Install Bellronos Scripting Languages into your Operating System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="RonaldsonBellande",
    author_email="ronaldsonbellande@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "requests",
        "packaging",
    ],    
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],    
    keywords="bellronos installer scripting languages",
    python_requires=">=3.0",
    extras_require={
        "dev": ["pytest", "pytest-cov[all]", "mypy", "black"],
    },
    entry_points={
        'console_scripts': [
            'bellronos_installer = bellronos_installer.bellronos_installer:main',
        ],
    },
    project_urls={
        "Home": "https://github.com/Architecture-Mechanism/bellronos_installer",
        "Homepage": "https://github.com/Architecture-Mechanism/bellronos_installer",
        "documentation": "https://github.com/Architecture-Mechanism/bellronos_installer",
        "repository": "https://github.com/Architecture-Mechanism/bellronos_installer",
        "Bug Reports": "https://github.com/Architecture-Mechanism/bellronos_installer/issues",
        "Source": "https://github.com/Architecture-Mechanism/bellronos_installer",
    },
    cmdclass={
        'install': PostInstallCommand,
    },
)
