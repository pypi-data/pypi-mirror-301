from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bellande_format",
    version="0.1.8",
    description="Bellande Format is a file format type",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="RonaldsonBellande",
    author_email="ronaldsonbellande@gmail.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=[
        "numpy>=1.18.0",
        "typing-extensions>=3.7.4",
    ],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords=["package", "setuptools", "bellande", "format"],
    python_requires=">=3.6",
    extras_require={
        "dev": ["pytest", "pytest-cov[all]", "mypy", "black"],
    },
    entry_points={
        "console_scripts": [
            "Bellande_Format = bellande_format.bellande_parser:Bellande_Format",
        ],
    },
    project_urls={
        "Home": "https://github.com/Architecture-Mechanism/bellande_format",
        "Homepage": "https://github.com/Architecture-Mechanism/bellande_format",
        "Documentation": "https://github.com/Architecture-Mechanism/bellande_format",
        "Repository": "https://github.com/Architecture-Mechanism/bellande_format",
    },
)
