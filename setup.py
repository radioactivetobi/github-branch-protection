"""Setup configuration for GitHub branch protection automation package."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="github-branch-protection",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Automate GitHub branch protection rules across repositories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/github-branch-protection",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "PyGithub>=1.55",
        "python-dotenv>=0.19.0"
    ],
    entry_points={
        "console_scripts": [
            "github-protect=src.main:main",
        ],
    },
)
