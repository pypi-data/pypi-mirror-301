from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wservice-client",
    version="1.1.1",
    author='DEVMNE',
    author_email='mne@yaposarl.ma',
    description="A Python client for web service communication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mnedev-cell/wservice_client.git",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)

