# Copyright (c) AffectLog SAS
# Licensed under the MIT License.
import setuptools

VERSION = "0.1.0"

# supply contents of our README file as our package's long description
with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = []
with open("requirements.txt", "r") as fr:
    requirements = list(filter(
        lambda rq: rq != "",
        map(lambda r: r.strip(), fr.read().split("\n"))))

setuptools.setup(
    # this is the name people will use to "pip install" the package
    name="affectlog_feature_extractors",

    version=VERSION,
    author="AL360°",
    author_email="developer@affectlog.com",
    description="AffectLog NLP Feature Extractors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/affectlog/trustworthy-ai-widgets",
    # Packages
    packages=[
        "affectlog_feature_extractors",
        "affectlog_feature_extractors.data"
    ],
    # this forces our txt files to be included
    package_data={'': ['*.txt']},
    include_package_data=True,
    # the packages that our package is dependent on
    install_requires=requirements,
    # used to identify the package to various searches
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ],
)
