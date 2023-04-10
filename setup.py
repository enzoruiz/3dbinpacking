import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='py3dbp',
    version='1.1.2',
    author="Juan Cho",
    author_email="juanperez@gmail.com",
    description="3D Bin Packing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/enzoruiz/3dbinpacking",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
