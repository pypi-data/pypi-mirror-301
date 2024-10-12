from setuptools import setup, find_packages


# Read the requirements from requirements.txt
def parse_requirements(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        return [line.strip() for line in lines if not line.startswith("#") and not line.startswith("git+")]


setup(
    name="dappier-py",
    version="0.2.0",
    description="Dappier Python SDK for interacting with Dappier APIs",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Maddy Arvapally",
    author_email="support@dappier.com",
    url="https://github.com/DappierAI/dappier-py",
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),  # Read dependencies from requirements.txt
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
