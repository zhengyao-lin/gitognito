from setuptools import setup, find_packages

setup(
    name="gitognito",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "GitPython==3.1.44",
    ],
    entry_points={
        "console_scripts": [
            "gitognito=gitognito.main:main",
        ],
    },
    author="zhengyal",
    author_email="",
    description="Anonymize a Git repo for paper submission purposes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zhengyao-lin/gitognito",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
