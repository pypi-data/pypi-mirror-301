from setuptools import setup, find_packages

setup(
    name="vector_db_pkg",               # Package name
    version="0.1.0",                    # Initial version
    description="A vector database builder and search tool",  # Short description
    author="Nwoka Ajinwo",
    author_email="nwoka05@gmail.com",
    packages=find_packages(),           # Automatically find all modules in your package
    install_requires=[                  # List your dependencies here
        "pandas",
        "sqlalchemy",
        "scikit-learn",
        "faiss-cpu",
        "numpy"
    ],
    classifiers=[                       # Optional metadata for PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',            # Minimum Python version
)