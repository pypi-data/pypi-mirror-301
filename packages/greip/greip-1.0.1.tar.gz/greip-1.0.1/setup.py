from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="greip",
    version="1.0.1",
    description="Python wrapper for Greip API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Greip",
    author_email="info@greip.io",
    url="https://github.com/Greipio/python",
    keywords="geolocation, geoip, fraud-prevention, profanity-detection, fraud-detection, asn-lookup, bin-lookup",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Development Status :: 3 - Production/Stable",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Security",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    python_requires='>=3.6',
    project_urls={
        "Bug Reports": "https://github.com/Greipio/python/issues",
        "Source": "https://github.com/Greipio/python",
    },
)
