from setuptools import setup, find_packages

setup(
    name="peckish",  # The name of the package
    version="0.0.1",  # Initial version
    author="Sebastien Pradier",
    author_email="sebastien@example.com",
    description="A dummy package to reserve the name",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/peckish",  # Replace with your repo link (optional)
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
