from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bellos_installer",
    version="0.1.1",
    description="Install Bellos Scripting Languages into your Operating System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="RonaldsonBellande",
    author_email="ronaldsonbellande@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "numpy",
    ],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
    ],
    keywords=["package", "setuptools"],
    python_requires=">=3.0",
    extras_require={
        "dev": ["pytest", "pytest-cov[all]", "mypy", "black"],
    },
    entry_points={
        'console_scripts': [
            'bellos_installer = bellos_installer.bellos_installer:main',
        ],
    },
    project_urls={
        "Home": "https://github.com/Architecture-Mechanism/bellos_installer",
        "Homepage": "https://github.com/Architecture-Mechanism/bellos_installer",
        "documentation": "https://github.com/Architecture-Mechanism/bellos_installer",
        "repository": "https://github.com/Architecture-Mechanism/bellos_installer",
    },
)
