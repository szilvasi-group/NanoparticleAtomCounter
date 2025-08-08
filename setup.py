##I generated this setup.py using setup-py-cli
##from https://pypi.org/project/setup-py-cli/

from setuptools import setup, find_packages
import io
import os
from nanoparticleatomcounter import __version__

here = os.path.abspath(os.path.dirname(__file__))

# read the contents of your README.md
with io.open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="nanoparticleatomcounter",
    version=__version__,
    author="Gbolagade Olajide, Tibor Szilvasi",
    author_email="giolajide@crimson.ua.edu, tszilvasi@crimson.ua.edu",
    description="Estimate atom counts in monometallic nanoparticles"
    " given radius and contact angle",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/giolajide/nanoparticleatomcounter",
    packages=find_packages(where="."),

    # specify your dependencies here
    install_requires=[
        "numpy>=1.20,<2.3",
        "pandas>=1.4",
        "streamlit>=1.4,<2.0",
        "openpyxl>=3.1.0",
        "xlrd>=2.0.1",
        "pytest<=8.4.1",
        "ase<=3.23.0",
        "tqdm<=4.67.1",
        "joblib<=1.5.1"
    ],

    # enable the CLI: `nanoparticle-atom-count`
    entry_points={
        "console_scripts": [
            "nanoparticle-atom-count="
            "nanoparticleatomcounter.cli.atom_count:main", #main script

            "atom-count-test="
            "nanoparticleatomcounter.tests.run_tests:main" #tests script
        ],
    },

    classifiers=[
        ##https://pypi.org/classifiers/
        # Project maturity
        "Development Status :: 4 - Beta",
        # Audience & topic
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry",
        # License
        "License :: OSI Approved :: MIT License",
        # Supported Python versions
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],

    keywords=[
        "nanoparticle",
        "tem",
        "electron microscopy",
        "active site",
        "catalyst"
        ],

    license="MIT",
    python_requires=">=3.8",
    include_package_data=True,
    project_urls={
        "Bug Tracker": "https://github.com/giolajide/nanoparticleatomcounter/issues",
        "Documentation": "https://github.com/giolajide/nanoparticleatomcounter#readme",
    },
)

