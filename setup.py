import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="genpot",
    version="1.1.3",
    author="Even Marius Nordhagen",
    author_email="evenmn@fys.uio.no",
    description="Generate potential files used by LAMMPS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/evenmn/generate-potential-files",
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
