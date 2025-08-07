Nanoparticle Atom Counter
=============================

Assuming a spherical cap, we estimate the number of Total, Surface, Perimeter, and Interfacial atoms of a supported nanoparticle
from the radius and contact angle, both of which can be easily gotten from TEM images

Web app: https://nanoparticle-atom-counting.streamlit.app/

Requirements
------------
* NumPy>=1.20,<2.3
* pandas>=1.4
* Streamlit>=1.4
* openpyxl>=3.1.0
* xlrd>=2.0.1
* pytest<=8.4.1
* ase<=3.23.0
* tqdm<=4.67.1
* joblib<=1.5.1

Installation
------------
TO install the latest version:
::
    pip install nanoparticleatomcounter

Alternatively:
::
    git clone XXXXX

Testing
-------
Please run the following test and let us know if there are any errors:
::
    XXXXX I need to put this in an automatic way like 'ase test' XXXX

Contact
-------
* Email me at giolajide@crimson.ua.edu
* Or raise an issue right here


Example
-------
1. On the webpage
2. On a command line
   ::
        nanoparticle-atom-counter --input input.csv --output output.csv



:: _webpage: https://nanoparticle-atom-counting.streamlit.app
