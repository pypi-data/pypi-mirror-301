from setuptools import setup, find_packages

setup(
    name="auth_key_manager",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["mysql-connector-python", "pymongo", "requests"],
    description="A robust and flexible license key management system for Python applications, enabling secure license validation, renewal, and revocation with ease.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="IbrahimBkt",
    author_email="AuthForge@outlook.com",
    url="https://github.com/AuthForge/AuthKeyManager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
