Nanoparticle Atom Counter
=========================

Treating a supported nanoparticle as a spherical cap, NanoparticleAtomCounter rapidly estimates the number of **Total**, **Surface**, **Perimeter**, and **Interfacial** atoms (see below).
Only two inputs are needed: the radius and contact angle, readily obtainable from Transmission Electron Microscopy (TEM) images.



.. figure:: https://raw.githubusercontent.com/giolajide/nanoparticleatomcounter/main/Nanoparticle_Legend.png
   :width: 450
   :alt: Atom types discriminated
   :align: center



Can be used on the web app_ or on a command line.




Requirements
------------

* numpy>=1.20,<2.3
* pandas>=1.4
* streamlit>=1.4,<2
* openpyxl>=3.1.0
* xlrd>=2.0.1


For testing, these are also required

* pytest>=8,<9
* ase>=3.22.0,<3.25
* tqdm<=4.67.1
* joblib<=1.5.1
* ascii-colors



Installation
------------

First create and activate a new environment::

    mamba create --name env_name "python>=3.10,<3.15"
    mamba activate env_name

To install the latest version::

    pip install NanoparticleAtomCounter
    #pip install NanoparticleAtomCounter[test] to be able to run tests

Alternatively::

    git clone git@github.com:szilvasi-group/NanoparticleAtomCounter.git
    cd NanoparticleAtomCounter/
    pip install -e .
    #pip install -e ".[test]" to be able to run tests



Usage
-------

- **Prepare your input CSV**

  Upload a .csv containing the columns:

  ::

      r (A), R (A), Theta, Element, Interface Facet, Surface Facet

  Notes:

  - Supply either ``r`` or ``R`` (if both are present, ``r`` is used).
  - ``Interface Facet`` and ``Surface Facet`` are optional; leave blank if unknown.
  - See the sidebar on the web app_ for a sample input file.

- **Use the web app**

  Upload your input file and download the output.

* Prepare your input CSV. 
Upload a .csv containing the columns
r (A), R (A), Theta, Element, Interface Facet, Surface Facet.

Supply either r or R (if both are present, r is used).
Interface Facet and Surface Facet are optional; leave blank if unknown.

See the sidebar on the web app_ for a sample input file
* To use on the web app_, upload your input file and download the output
* To use on a command line::

    nanoparticle-atom-counter --input input_file.csv --output output_file.csv



Testing
-------

If you have it installed with the tests, then run the following test and please let me know if there are any errors::

    atom-count-test



Contact
-------

Any problems or questions?

* Email me at giolajide@crimson.ua.edu
* Or raise an issue right here_




.. _app: https://nanoparticle-atom-counting.streamlit.app
.. _here: https://github.com/giolajide/nanoparticleatomcounting/issues
