from setuptools import setup, find_packages

setup(
    name="magics-python",
    version="0.0.1",
    description="Python client for Magics's Cloud Platform!",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Magics AI",
    author_email="support@magics.ai",
    license="Apache-2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "typer>=0.9,<0.13",
        "requests>=2.31.0",
        "rich>=13.8.1,<14.0.0",
        "tqdm>=4.66.2",
        "tabulate>=0.9.0",
        "pydantic>=2.6.3",
        "aiohttp>=3.9.3",
        "filelock>=3.13.1",
        "eval-type-backport>=0.1.3,<0.3.0",
        "click>=8.1.7",
        "pillow>=10.3.0",
        "pyarrow>=10.0.1",
        "numpy>=1.23.5; python_version<'3.12'",
        "numpy>=1.26.0; python_version>='3.12'",
    ],
    entry_points={
        "console_scripts": [
            "magics=magics.cli.cli:main",
        ],
    },
    python_requires=">=3.8",
)
