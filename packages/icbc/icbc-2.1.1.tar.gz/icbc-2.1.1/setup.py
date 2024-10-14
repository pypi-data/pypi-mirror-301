# -*- coding:utf-8 -*-
import platform
requires = []
import setuptools
##with open("README.md", "r") as fh:
##    long_description = fh.read()
setuptools.setup(
    name="icbc", 
    version="2.1.1",
    author='lhyweb',
    install_requires=requires,
    author_email="lhyweb@gmail.com",
    keywords=['icbc', 'tool', 'gui', 'ie', "mouse"],
    description="""personal utilities code""",
##    long_description=long_description,
##    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={"":["*.ico"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
##    python_requires='>=3.6',
)
