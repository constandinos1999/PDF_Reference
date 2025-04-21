from setuptools import setup, find_packages

setup(
    name="pdf_python",
    version="0.1",
    packages=find_packages(),
    install_requires=[  # Remove 'tkinter' here
        "pdfminer.six",
        "pdfplumber",
        "PyPDF2",
        "requests",
    ],
)