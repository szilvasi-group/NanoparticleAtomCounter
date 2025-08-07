"""
Here, I will compare the results given by the npatomcounter to those
from making an approximate atomistic model for nanoparticles of an FCC
lattice and flat interface
"""

import subprocess
from ase.io import write
import shlex
from os import system
import numpy as np
import pandas as pd
from itertools import product
from ase import Atoms
from nanoparticleatomcounter.tests.compare_to_atomistic.atomistic_utils import scaler, create_unit_support
from tqdm import tqdm
from typing import List, Union, Tuple, Literal
from ase.visualize import view
import warnings
from nanoparticleatomcounter.tests.compare_to_atomistic.create_spherical_caps import create_sphere, cut_particle
from argparse import ArgumentParser

MIN_ANGLE = 60
MAX_ANGLE = 160
MIN_RADIUS = 10 #Ang
MAX_RADIUS = 50 #Ang
N_ANGLES = 5
N_RADII = 5
PROCESSES = -1
OUTPUT_TRAJECTORY = "atoms.traj"
NP_ELEMENTS = ["Ag"]
SUPPORT_ELEMENTS = ["graphene", "au"]


def create_trajectory(
        min_angle: float, max_angle: float, n_angles: int,
        min_radius: float, max_radius: float, n_radii: int,
        output_trajectory: str,
        np_elements: Union[str, List[str]],
        support_element: Union[str, List[str]]
        ) -> Tuple[List[float],List[float],List[str]]:

    """
    Creates the atomistic model

    Requires:

        min_angle:          lowest contact angle desired
        max_angle:          max contact angle desired
        n_angles:           how many contact angles desired
        min_radius:         lowest radius OF CURVATURE (NOT footprint radius) desired
        max_radius:         work it out
        n_radii:            work it out
        output_trajectory:  name of file in which to write the models
        np_elements:        the type of atom of which the nanoparticle is composed,
                            as a list, one for each nanoparticle/support combination
        support_elements:   the type of atom of which the support is composed,
                            as a list, one for each nanoparticle/support combination.
                            Should be 'graphene', 'mgo', or 'au'

    Returns:

        contact_angles:     list of contact angles
        radii_angstrom:     list of curvature radii
        nanoparticles:      list of nanoparticle elements
        supports:           list of support elements
    """

    if max_radius > 40:
        warnings.warn("""This will take some time.
                I hope you can what you are doing!""",
                category = UserWarning
                )

    nanoparticles = [np_elements] if isinstance(np_elements, str) else np_elements
    supports = [support_elements] if isinstance(support_element, str) else support_element

    radii_angstrom = np.linspace(min_radius, max_radius, n_radii)
    contact_angles = np.linspace(min_angle, max_angle, n_angles)

    atoms_list: List[Atoms] = []

    for r in tqdm(radii_angstrom, total = len(radii_angstrom),
            desc = "creating atomistic models of the requested systems"):
        for theta in contact_angles:
            for nanoparticle in nanoparticles:
                for support in supports:
                    atoms = create_sphere(element=nanoparticle,radius=r)
                    atoms = cut_particle(atoms,theta)
                    unit_support = create_unit_support(support)
                    atoms = scaler(image = atoms, unit_support=unit_support)
                    atoms.info["np_element"] = nanoparticle
                    atoms_list.append(atoms)

    write(output_trajectory, atoms_list)
    print("created and written atoms objects")

    return contact_angles, radii_angstrom, nanoparticles, supports


def run_atomistic(
        processes: int,
        trajectory_file: str, radii_angstrom: List[float],
        contact_angles: List[float],
        nanoparticles: List[str], supports: List[str],
        input_to_atomcounter: str,
        atomistic_output: str,
        ):
    """
    Use the atomistic model to get the number of each kind of atom in each nanoparticle

    Requires:

        processes:              number of parallel processes to use.
        trajectory_file:        the file containing the atomistic models
        radii_angstrom:         list of curvature radii
        contact_angles:         list of contact angles
        nanoparticles:          list of nanoparticle elements
        supports:               list of support elements
        input_to_atomcounter:   name of input file this will generate;
                                will contain the curvature radius, element, and contact angle,
                                which the atomcounter will need
        atomistic_output:       name of output file to be generated, containing the number
                                of each kind of atom in each nanoparticle

    """
    print("discriminating...")
    command = shlex.split(f"python tests/discrimination.py -t {trajectory_file} -p {processes} -o {atomistic_output}")

    with open("discrimination.out", "w") as out_f, open("discrimination.err", "w") as err_f:
        subprocess.run(
                command,
                stdout = out_f,
                stderr = err_f,
                check = True
                )

    rows = []
    for R, theta, element, _ in product(radii_angstrom, contact_angles, nanoparticles, supports):
        rows.append({
            "r (A)": 0.0,
            "R (A)": R,
            "Theta": theta,
            "Element": element.capitalize(),
            "Interface Facet": "(1,0,0)",
            "Surface Facet": "(1,1,1)",
        })

    df = pd.DataFrame(rows)
    df.to_csv(input_to_atomcounter, index=False)
    print("Finished the atomistic modelling")


def run_atomcounter(input_file: str, output_file: str):
    """
    Runs the atomcounter to get the number of each kind of atom in each nanoparticle

    Requires:

        input_file:     name of input file, having the element, curvature radius, etc
        output_file:    name of output file to be generated
    """

    print("running npatomcounter...")
    command = shlex.split(f"nanoparticle-atom-count -i {input_file} -o {output_file}")
    with open("atomcounter.out", "w") as out_f, open("atomcounter.err", "w") as err_f:
        subprocess.run(
                command,
                stdout = out_f,
                stderr = err_f,
                check = True
                )

    print("Finished running the atom counter")


def plot_parities(atomistic_output: str,
        atomcounter_output: str):
    """
    Creates parity plots of the results, comparing the atomistic to the atomcounter

    Requires:
        atomistic_output:       name of output file from the atomistic
        atomcounter_output:     name of output file from the atomcounter
    """
    print("plotting parities...")
    command = shlex.split(f"python tests/plot-parity.py {atomistic_output} {atomcounter_output} --show")
    with open("parity.out", "w") as out_f, open("parity.err", "w") as err_f:
        subprocess.run(
                command,
                stdout = out_f,
                stderr = err_f,
                check = True
                )



##here we go
traj_file = OUTPUT_TRAJECTORY
input_to_atomcounter = "input.csv"
atomcounter_output = "counter.csv"
atomistic_output = "atomistic.csv"

contact_angles, radii_angstrom, nanoparticles, supports = create_trajectory(
        min_angle = 69, max_angle = 155, n_angles = 6,
        min_radius = 12, max_radius = 25, n_radii = 6,
        output_trajectory = traj_file, np_elements = ["Pd"],
        support_element = ["graphene"]
        )

print("We might be here a while . . . ")

run_atomistic(
        processes = PROCESSES, trajectory_file = traj_file,
        contact_angles = contact_angles, radii_angstrom = radii_angstrom,
        nanoparticles = nanoparticles, supports = supports,
        input_to_atomcounter = input_to_atomcounter,
        atomistic_output = atomistic_output
        )

run_atomcounter(input_file = input_to_atomcounter, output_file = atomcounter_output)

plot_parities(atomistic_output = atomistic_output, atomcounter_output = atomcounter_output)


