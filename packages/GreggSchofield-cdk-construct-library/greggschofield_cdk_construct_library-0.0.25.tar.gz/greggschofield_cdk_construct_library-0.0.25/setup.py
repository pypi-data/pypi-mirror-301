import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "GreggSchofield-cdk-construct-library",
    "version": "0.0.25",
    "description": "cdk-construct-library",
    "license": "Apache-2.0",
    "url": "https://github.com/GreggSchofield/cdk-construct-library",
    "long_description_content_type": "text/markdown",
    "author": "Gregg Schofield<schofieldgregg@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/GreggSchofield/cdk-construct-library"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "GreggSchofield_cdk-construct-library",
        "GreggSchofield_cdk-construct-library._jsii"
    ],
    "package_data": {
        "GreggSchofield_cdk-construct-library._jsii": [
            "cdk-construct-library@0.0.25.jsii.tgz"
        ],
        "GreggSchofield_cdk-construct-library": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.1.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.103.1, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<5.0.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
