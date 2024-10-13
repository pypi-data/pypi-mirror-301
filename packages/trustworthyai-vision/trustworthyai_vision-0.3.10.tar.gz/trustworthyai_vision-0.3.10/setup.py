# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

import setuptools

# Version will be read from version.py
version = ''
name = 'trustworthyai-vision'
# Fetch Version
with open('trustworthyai_vision/version.py') as f:
    code = compile(f.read(), f.name, 'exec')
    exec(code)

# Fetch ReadMe
with open('README.md', 'r') as fh:
    long_description = fh.read()

# Use requirements.txt to set the install_requires
with open('requirements.txt') as f:
    install_requires = [line.strip() for line in f]

setuptools.setup(
    name=name,
    version=version,
    author="AL360°",
    author_email="developer@affectlog.com",
    description="SDK API to assess image "
                "Machine Learning models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/affectlog/trustworthy-ai-toolbox",
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ]
)
