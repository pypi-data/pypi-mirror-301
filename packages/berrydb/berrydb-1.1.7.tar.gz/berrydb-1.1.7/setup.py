from setuptools import setup, find_packages

VERSION = "1.1.7"

DESCRIPTION = "The database for unstructured data and AI apps"
AUTHOR = "BerryDB"
URL = "https://berrydb.io"

setup(
    name="berrydb",
    version=VERSION,
    description=DESCRIPTION,
    url=URL,
    author=AUTHOR,
    license="Proprietary",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "requests",
        "openai",
        "langchain",
        "langchain_community",
        "langchain_openai",
        "tiktoken",
        "faiss-cpu",
        "jq",
        "unstructured[pdf]",
        "label-studio-sdk==1.0.5",
    ],
    classifiers=[
        "License :: Other/Proprietary License",
    ],
    py_modules=[
        "database",
        "BerryDB",
        "utils",
        "loaders",
        "embeddings",
    ],
    packages=find_packages(),
)
