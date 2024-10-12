from setuptools import setup, find_packages

setup(
    name="kamla-cli",
    version="0.1.0",
    description="Inhouse Ten CLI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="NurTasin",
    author_email="nmuatasin2005@gmail.com",
    url="https://github.com/nurtasin/kamla-cli",  # Replace with your repo URL
    packages=find_packages(),  # This will find all sub-packages (like kamla_cli)
    include_package_data=True,  # Include non-Python files from MANIFEST.in
    install_requires=[          # External dependencies (if any)
        "pwinput>=1.0.0",
        "texttable>=1.6.3",
        "pytz>=2021.3",
        "requests>=2.26.0",
    ],
    entry_points={
        "console_scripts": [
            "kamla-cli=kamla_cli.cli:main",  # This defines your CLI entry point
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version requirement
)
