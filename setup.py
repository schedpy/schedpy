import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="schedpy",
    version="v0.1.0",
    author="Abdullah Javed Nesar",
    author_email="abduljaved1994@gmail.com",
    description="A cron or job scheduler in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/schedpy/schedpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
