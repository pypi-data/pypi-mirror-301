from setuptools import setup, find_packages
from setuptools.dist import Distribution

class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True

    def is_pure(self):
        return False

import os
so_files = [f for f in os.listdir('pp_recordio') if f.endswith('.so')]

setup(
    name="pp_recordio",
    version="0.1.3",
		description="Post Perception's RecordIO facimile.",
    long_description="""PostPerception's facimile of Google's RecordIO library (no direct relation
    other than name). This is a binary format for storing sequences of arbitrary
    binary data, usually protocol buffers. It tolerates corruption of the
    underlying data and uses a CRC32 checksum to detect data corruptions.
    Supports Linux x86, Linux aarch64, Darwin x86, and Apple Silicon (Darwin
                                                                      amd64).""",
    long_description_content_type="text/markdown",
    author="Sam Liu",
    author_email="sam@postperception.com",
    url="https://github.com/postperception/pp_recordio",
    license="MIT",
    py_modules=["pp_recordio"],
    packages=find_packages(),
    package_data={
        "pp_recordio": so_files,
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    distclass=BinaryDistribution,
    options={
      'bdist_wheel': {
        'plat_name': 'macosx_11_0_arm64',  # Apple silicon.
        }
      },
)
