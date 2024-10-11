from setuptools import setup, find_packages
import os
import sys

# Explicitly set the version
VERSION = '0.1.2'

def post_install():
    script_path = os.path.join(sys.prefix, 'bin', 'bellos_installer')
    if os.path.exists(script_path):
        os.chmod(script_path, 0o755)
        with open(script_path, 'r+') as f:
            content = f.read()
            if not content.startswith('#!/usr/bin/env python3'):
                f.seek(0, 0)
                f.write('#!/usr/bin/env python3\n' + content)
    else:
        print(f"Warning: Could not find {script_path}")

# Read long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bellos_installer",
    version=VERSION,
    description="Install Bellos Scripting Languages into your Operating System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="RonaldsonBellande",
    author_email="ronaldsonbellande@gmail.com",
    url="https://github.com/Architecture-Mechanism/bellos_installer",
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
    keywords="bellos installer scripting languages",
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'bellos_installer=bellos_installer.bellos_installer:main',
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/Architecture-Mechanism/bellos_installer/issues",
        "Source": "https://github.com/Architecture-Mechanism/bellos_installer",
    },
)

if __name__ == '__main__':
    setup()
    post_install()
