from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = "0.0.1"
DESCRIPTION = (
    "Update Fabric Workspace From Git Repo using A user with Email And Password"
)
# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="updatefromgit",
    version=VERSION,
    author="Muhammad Samy",
    author_email="muhssamy@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    packages=find_packages(),
    install_requires=["msal"],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    keywords=["python", "updatefromgit"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
