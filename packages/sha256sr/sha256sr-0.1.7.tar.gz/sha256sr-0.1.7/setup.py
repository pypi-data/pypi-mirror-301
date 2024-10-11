import os
from setuptools import setup, find_packages, Extension

NAME = "sha256sr"
DESCRIPTION = "the secure random generator based on SHA256"
URL = "https://github.com/capricornsky0119/sha256sr.git"
EMAIL = "zhangdaode0119@gmail.com"
AUTHOR = "zhangdaode"

root_dir = os.path.split(os.path.realpath(__file__))[0]
requires_list = open(os.path.join(root_dir, "requirements.txt"), "r").readlines()
requires_list = [i.strip() for i in requires_list]

with open(os.path.join(root_dir, "README.md"), "r") as fh:
    long_description = fh.read()


example_module = Extension(
    "_secure_random",
    sources=[
        "sha256sr/secure_random.cpp",
        "sha256sr/sha256.cpp",
        "sha256sr/swig_wrap.cxx",
    ],
    include_dirs=[os.path.join(root_dir, "sha256sr")],
    extra_compile_args=['-std=c++11'],
)

setup(
    name=NAME,
    version="0.1.7",
    metadata_version='2.1',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    packages=find_packages(),
    install_requires=requires_list,
    include_package_data=True,
    package_data={
        'sha256sr': [
            os.path.join(root_dir, 'sha256sr', 'secure_random.h'),
            os.path.join(root_dir, 'sha256sr', 'sha256.h'),
            os.path.join(root_dir, 'requirements.txt'),
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    zip_safe=False,
    ext_modules=[example_module]
)
