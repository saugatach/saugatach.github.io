---
layout: post
title: "How to convert python script to a python package"
date: 2021-03-02
background: '/img/bg-posts-black-blur.jpg'
---


# TLDR
1. Cluster codes with similar functionality into one directory
2. Create a package
   1. Create setup files
       1. Create a setup.py file
       2. Create a README.md file
       3. Create a LICENSE.txt file
   2. Install setup tools
       1. Install setuptools
       2. Install wheels
3. Test package in a virtual environment

Create a setup.py file
This is the most important file. It usually looks like this.
```commandline
from setuptools import setup, find_packages

setup(name='[packagename]',
      version='[version]',
      description='[What the package does]',
      url='[https://github.com/you/stockanalysis]',
      author='[your name]',
      author_email='[you@gmail.com]',
      license='MIT',
      packages=find_packages(include=['stockanalysis']),
      python_requires='>=3'
      )
```
To install the package in developer mode go to the parent folder of your 
package directory and run
```commandline
python -m pip install -e .
```
-------------------
## Introduction

During any phase of any project it is efficient to create libraries of past code, which we often reuse. 
However, for some projects we are always in a development stage, and we want to keep updating
the code, while keep using it as a library at the same time. The following steps are the most efficient way
of doing this.
1. Cluster codes with similar functionality into one directory
2. Create a package
3. Test package in a virtual environment
4. Deploy locally

We will be using python for our discussion. 

## Cluster codes with similar functionality into one directory
Once you have collected all python scripts into one directory that you want to convert into a package add the test.py 
and init.py files. The directory structure should look like this. 
```commandline
├── DividendData.py
├── getstockdata.py
├── __init__.py
├── portfolioanalysis.py
└── test.py
```
The ```__init__.py``` can be empty at this point. The ```test.py``` should import the packages and make function calls 
to make sure everything loads properly. For example, here we load the packages ```getstockdata``` and ```DividendData```
and create objects from the classes contained in those packages. If the package is not installed properly, ```test.py```
will generate errors which are easily traceable.

```commandline
from getstockdata import GetStockData
from DividendData import DividendData

gdobj = GetStockData('AAPL')
dobj = DividendData('AAPL')
```

## Create a package
Once we have our python files in a single folder, creating a python package involves these steps.
1. Create setup files
    1. Create a setup.py file
    2. Create a README.md file
    3. Create a LICENSE.txt file
2. Install setup tools
    1. Install setuptools
    2. Install wheel
3. Generating the build

### Create setup files
We need at least 3 files to create the package build; setup.py, README.md, LICENSE.txt in the parent directory of our 
package. 

#### Create a setup.py file
This is the most important file. It usually looks like this.
```commandline
from setuptools import setup, find_packages

setup(name='[packagename]',
      version='[version]',
      description='[What the package does]',
      url='[https://github.com/you/stockanalysis]',
      author='[your name]',
      author_email='[you@gmail.com]',
      license='MIT',
      packages=find_packages(include=['stockanalysis']),
      python_requires='>=3'
      )
```
The fields are self-explanatory, so replace the ```[ ]``` by the appropriate values. ```find_packages``` is not necessary 
but helps if there are lots of similar named packages. 

####  Create a README.md file
The README.md is a markdown file which should contain detailed description for the package. Commonly, developers include
usage description, bugs, workarounds in the README.md. For our purpose, a short description is sufficient 
(it can also be blank, although that is not recommended). 

####  Create a LICENSE.txt file
Head over to [choosealicense](https://choosealicense.com/) to select a license of your choice, and copy the license text.
The common choice is MIT. After you copy the license to your ```LICENSE.txt``` file, update the author and date.
```commandline
MIT License

Copyright (c) 2021 Me

Permission is hereby granted, free of charge, to 
```
The project directory will look like this
```commandline
├── LICENSE.txt
├── README.md
├── setup.py
└── stockanalysis
    ├── DividendData.py
    ├── getstockdata.py
    ├── helpers.py
    ├── __init__.py
    ├── portfolioanalysis.py
    ├── settings
    └── test.py
```


### Install setup tools
If you do not have already installed setuptools, then install them.
```commandline
pip install --upgrade setuptools wheel
```

## Generating the build
Now, we can generate a build that can be distributed or install the package in developer mode. 
To generate the build that can be distributed run
```commandline
python setup.py sdist bdist_wheel
```

# Test package in a virtual environment
We are more interested in installing the package in developer mode. However, to avoid damage to the system we need to
load up a virtual environment to test run the package.
```commandline
virtualenv -p python3 randomtest
source randomtest/bin/activate
```
Once we are in the virtual environment, to install the package in developer mode go to the parent folder of your 
package directory and run
```commandline
python -m pip install -e .
```
This will let test the package in the virtual environment. Once you are satisfied that everything is working as they 
should, deactivate the virtual environment and repeat the install process.


References: [Packaging and distributing projects](https://packaging.python.org/guides/distributing-packages-using-setuptools/)