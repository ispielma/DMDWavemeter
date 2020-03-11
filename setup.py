import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DMDWavemeter", # Replace with your own username
    version="0.0.1",
    author="Ian Spielman",
    author_email="ian.spielman@nist.gov",
    description="Softare to use a DMD as a optical wavemeter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ispielma/DMDWavemeter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
