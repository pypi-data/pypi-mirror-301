"""
Copyright 2024 Amazon.com, Inc. and its affiliates. All Rights Reserved.

Licensed under the Amazon Software License (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at

  https://aws.amazon.com/asl/

or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.
"""

from setuptools import setup, find_packages

extras_require = {
    "run-agent": [
        "fastapi~=0.112.0",
        "uvicorn~=0.30.5",
    ],
    "evaluate": [
        "nltk~=3.9.1",
        "scikit-learn~=1.5.1",
    ],
    "interactive": [
        "pandas~=2.2.2",
        "colorama~=0.4.6",
        "jsonpickle~=3.2.2",
        "requests~=2.32.3",
        "itables~=2.1.4",
        "tabulate~=0.9.0",
    ],
    "dev": ["boto3-stubs[bedrock-runtime,dynamodb]~=1.35.2"],
}

setup(
    name="genai-toolkit",
    description=open("README.md").read(),
    author="Amazon Web Services",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["boto3~=1.34.140"],
    extras_require={
        **extras_require,
        "all": list(set([v for e in extras_require.values() for v in e])),
    },
    python_requires=">=3.12",
)
