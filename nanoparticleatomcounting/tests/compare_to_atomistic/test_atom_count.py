import subprocess
from ase.io import write
import shlex
from os import system
import numpy as np
import pandas as pd
from itertools import product
from ase import Atoms
#from nanoparticleatomcounting.tests.ase_utils import scaler, create_unit_support
from nanoparticleatomcounting.ase_utils import scaler, create_unit_support
from tqdm import tqdm
from typing import List
from ase.visualize import view
import warnings
#from nanoparticleatomcounting.tests.create_spherical_caps import create_sphere, cut_particle
from nanoparticleatomcounting.create_spherical_caps import create_sphere, cut_particle

min_angle, max_angle = 75, 155
min_radius = 20 #Ang
max_radius = 200 #Ang
if max_radius > 50:
    warnings.warn("""This will take some time!
            If you're not patient, reduce the max radius""",
            category = UserWarning
            )
#let's create some Ag/graphene
processes = -1
trajectory = "atoms.traj"
radii_angstrom = np.linspace(min_radius, max_radius, 20)
contact_angles = np.linspace(min_angle, max_angle, 3)
nanoparticles = ["ag"]
supports = ["c"]
atoms_list: List[Atoms] = []

for r in tqdm(radii_angstrom):
    for theta in contact_angles:
        for nanoparticle in nanoparticles:
            for support in supports:
                atoms = create_sphere(element=nanoparticle,radius=r)
                atoms=cut_particle(atoms,theta)
                unit_support = create_unit_support(support)
                atoms = scaler(image = atoms, unit_support=unit_support)
                atoms.info["np_element"] = nanoparticle
                atoms.info["interfacial_facet"] = (1,0,0)
                atoms_list.append(atoms)


print("created atoms objects")
write(trajectory, atoms_list)
#view(atoms_list)

print("discriminating...")
#system("python discrimination.py -t atoms.traj -p -1")
command = shlex.split(f"python discrimination.py -t {trajectory} -p {processes}")

with open("discrimination.out", "w") as out_f, open("discrimination.err", "w") as err_f:
    subprocess.run(
            command,
            stdout = out_f,
            stderr = err_f,
            check = True
            )

rows = []
for R, theta, elem in product(radii_angstrom, contact_angles, nanoparticles):
    rows.append({
        "r (A)":     0.0,
        "R (A)":     R,
        "Theta":     theta,
        "Element":   elem.capitalize(),
        "Facet":     "(1,0,0)",
    })


df = pd.DataFrame(rows)
input_file = "input.csv"
df.to_csv(input_file, index=False)

print("running npatomcounter...")
command = shlex.split(f"python ../nanoparticleatomcounting/atom_count.py -i {input_file}")
with open("atomcounter.out", "w") as out_f, open("atomcounter.err", "w") as err_f:
    subprocess.run(
            command,
            stdout = out_f,
            stderr = err_f,
            check = True
            )

print("plotting parities...")
command = shlex.split(f"python plot-parity.py output_atomistic.csv output_atomcounts.csv  --show")
with open("parity.out", "w") as out_f, open("parity.err", "w") as err_f:
    subprocess.run(
            command,
            stdout = out_f,
            stderr = err_f,
            check = True
            )
print("Done!")

