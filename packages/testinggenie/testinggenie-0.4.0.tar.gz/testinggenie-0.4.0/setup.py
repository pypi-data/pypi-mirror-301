from setuptools import setup, find_packages

setup(
    name="testinggenie",
    version="0.4.0",
    author="Meesala Sai Dhanush",
    author_email="saidhanushm1@gmail.com",
    description="A package to generate unit test cases from code snippets using the Anthropic API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "tqdm",
        "anthropic",
    ],
)
