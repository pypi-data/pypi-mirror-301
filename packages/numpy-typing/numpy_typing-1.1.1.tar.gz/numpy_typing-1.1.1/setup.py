from setuptools import setup, find_packages
import os

if (os.path.exists("./dist")):
    os.system("rm -r ./dist/*")

VERSION = "1.1.1"
print(f"VERSION : {VERSION}")
DESCRIPTION = 'Improved numpy typing anotations'

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="numpy_typing",
    version=VERSION,
    author="Pirolley Melvyn",
    author_email="",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=["numpy"],
    package_data={'': ['*.py']},
    keywords=['python', 'numpy', 'typing', 'type hinting'],
    classifiers= [
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: MIT License",
    ]
)