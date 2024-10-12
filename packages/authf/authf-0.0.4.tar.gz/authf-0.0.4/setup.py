from setuptools import setup, find_packages
from authf import __version__

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='authf',
    version=__version__,
    author="Darshan P.",
    license="MIT",
    description="Authenticator Application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/1darshanpatil/authf",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "authf = authf.cli:main"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    keywords="authenticator, authentication, Two Step Authentication",
    install_requires=[
        "cffi==1.16.0",
        "cryptography==42.0.5",
        "pycparser==2.21",
        "pyotp==2.9.0",
        "pyperclip==1.8.2"
    ],
    project_urls={
        "Documentation": "https://github.com/1darshanpatil/authf#readme",
        "Source": "https://github.com/1darshanpatil/authf",
        "Tracker": "https://github.com/1darshanpatil/authf/issues"
    },
)
