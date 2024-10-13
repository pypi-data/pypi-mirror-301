from setuptools import setup, find_packages

setup(
    name="jarvislabs",
    version="0.1.2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pydantic>=2.7.0",
        "fastapi>=0.111.0",
        "uvicorn>=0.24.0",
        "boto3",
        "typer"
    ],
        entry_points={
        "console_scripts": [
            "jarvislabs=jarvislabs.cli:app",
        ],
    },
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.8",
)