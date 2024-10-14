from setuptools import setup, find_packages

setup(
    name="ntwrk",
    version="1.0.0",
    author="khiat Mohammed Abderrezzak",
    author_email="khiat.dev@gmail.com",
    license="MIT",
    description="Sophisticate Graph",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/ntwrk/",
    packages=find_packages(),
    install_requires=[
        "tabulate>=0.9.0",
        "hashtbl>=1.0.4",
    ],
    keywords=[
        "graph",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
