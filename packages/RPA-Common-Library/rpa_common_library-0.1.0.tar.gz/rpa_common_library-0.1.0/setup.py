from setuptools import setup
from setuptools import find_packages
import re
from pathlib import Path


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open(Path("src/Library", "Custom_Controls.py"), encoding="utf-8") as f:
    VERSION = re.search('\n__version__ = "(.*)"', f.read())

setup(
    name="RPA-Common-Library",
    version='0.1.0',
    author="Gowrishankar Venkatesan",
    author_email="Gowrishankar.Venkatesan@Ltimindtree.com",
    description="A library for Common Keywords.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://dev.azure.com/bpx/Data%20Science%20and%20Digital%20Solutions/_git/RPA-Common-Library",
    package_dir={"": "src"},
    packages=find_packages("src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Framework :: Robot Framework",
    ],
    install_requires=["robotframework >= 4.0.2, < 8.0", "docutils", "Pygments"],
    extras_require={"xls": ["pandas", "xlrd >= 1.2.0", "openpyxl"]},
    python_requires=">=3.8.0",
)