Nanoparticle Atom Counter
=========================

Assuming a spherical cap, we estimate the number of Total, Surface, Perimeter, and Interfacial atoms (illustrated below)
of a supported nanoparticle from the radius and contact angle, both of which can be easily gotten from TEM images


.. figure:: Nanoparticle_Legend.png
   :width: 300
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
* ase>=3.22,<3.27
* tqdm>=4.66,<5
* joblib>=1.5,<2

For testing, pytest>=8,<9 is also required



Installation
------------

First create and activate a new environment::

    conda create --name env_name python>=3.9
    conda activate env_name

To install the latest version::

    pip install nanoparticleatomcounter

Alternatively::

    git clone git@github.com:giolajide/nanoparticleatomcounter.git
    cd nanoparticleatomcounter
    pip install -e .


To also be able to run tests, install as::

    pip install nanoparticleatomcounter[test]



Testing
-------

If you have it installed with the tests, then please run the following test and let me know if there are any errors::

    atom-count-test



Contact
-------

Any problems or questions?

* Email me at giolajide@crimson.ua.edu
* Or raise an issue right here_



Example
-------

* To use on the web app_, upload your input file and download the output
* To use on a command line::

    nanoparticle-atom-counter --input input.csv --output output.csv



.. _app: https://nanoparticle-atom-counting.streamlit.app
.. _here: https://github.com/giolajide/nanoparticleatomcounting/issues
