# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

import os

import setuptools

# Version will be read from version.py
version = ""
# Fetch Version
with open(os.path.join('affectlog_widgets', '__version__.py')) as f:
    code = compile(f.read(), f.name, 'exec')
    exec(code)

# Fetch ReadMe
with open("README.md", "r") as fh:
    long_description = fh.read()

# Use requirements.txt to set the install_requires
with open('requirements.txt') as f:
    install_requires = [line.strip() for line in f] + \
        ["trustworthyai==%s" % version]

setuptools.setup(
    name="affectlog_widgets",
    version=version,
    author="AL360°",
    author_email="developer@affectlog.com",
    description="Interactive visualizations to assess fairness, explain "
                "models, generate counterfactual examples, analyze "
                "causal effects and analyze errors in "
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
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ],
    include_package_data=True,
    package_data={
    'affectlog_widgets': [
        'widget/*.html',
        'widget/*.js',
        'widget/*.css',
        'widget/*.png',
        ]
    },

    zip_safe=False,
)
