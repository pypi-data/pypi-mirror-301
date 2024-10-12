from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dabarqus",
    version="1.1.0",
    author="Xavier Gray",
    author_email="xay@electricpipelines.com",
    description="A Python SDK for interacting with the Dabarqus REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/electricpipelines/dabarqus-python",
    packages=find_packages(where="src", exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0,<3.0.0",
        "tqdm>=4.0.0,<5.0.0",
        "py7zr>=0.11.0,<1.0.0",
    ],
    extras_require={
        "dev": ["pytest>=6.0.0", "pytest-cov>=2.10.0"],
    },
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "dabarqus-install-service=dabarqus.install_service:main",
        ],
    },
)