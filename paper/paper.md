---
title: 'NanoparticleAtomCounter: A Python/Web-based package to convert nanoparticle geometry from Transmission Electron Microscopy into atom counts'
tags:
    - Python
    - Transmission Electron Microscopy
    - active sites
    - catalysts
    - nanoparticles
authors:
    - name: Gbolagade Olajide
      orcid: 0000-0003-0992-670X
      equal_contrib: true
      affiliation: '1'
    - name: Tibor Szilvasi
      corresponding: true
      orcid: 0000-0002-4218-1570
      affiliation: '1'
affiliations:
    - index: 1
      name: Department of Chemical and Biological Engineering, The University of Alabama, Tuscaloosa, AL, 35405, United States
date: 13 August 2025
bibliography: paper.bib
---

# Summary
`NanoparticleAtomCounter` converts transmission electron microscopy (TEM) derived geometry into atom counts for supported nanoparticles. Using the radius and contact angle of a nanoparticle, `NanoparticleAtomCounter` models nanoparticles as spherical caps and analytically estimates the total, surface, interfacial, and perimeter atoms without any atomistic modelling, allowing the conversion of hundreds of thousands of geometries into atom counts in minutes.

# Statement of need
Supported nanoparticles are important catalysts, and central to their reactivity is the binding site, the local environment where reactants adsorb. Quantifying how many binding sites exist and where they sit is essential for understanding catalyst performance. While imaging techniques such as TEM give precise shapes and sizes, they do not directly yield atomic-level counts across different regions of the nanoparticle. Converting the size and shape descriptors into atom counts is critical, as atoms located at interfaces, perimeters, and outer surfaces often exhibit different reactivity. Existing approaches to determine atom counts include the construction of full atomistic models for each particle geometry, an approach that scales poorly and is impractical for high-throughput TEM image screening.
Our package, `NanoparticleAtomCounter`, addresses the challenge of estimating atom counts in nanoparticles by using only two inputs, radius and contact angle, both of which can be obtained from TEM imaging. `NanoparticleAtomCounter` approximates nanoparticle morphology as a spherical cap and uses analytical geometry to estimate the atom counts in the interface, perimeter, and outer surface without requiring atomic-resolution modeling. Hundreds of thousands of calculations can be completed in minutes. Thus, researchers can translate TEM-derived geometry into quantitative binding site populations, enabling turnover frequencies to be reported on a per-site basis, rather than per-mass/area.

# Overview of NanoparticleAtomCounter
Below, we describe the methods used to calculate the number of total, interfacial, perimeter, and surface atoms of supported nanoparticles. We assume a monometallic nanoparticle shaped as a spherical cap of footprint radius $r$, radius of curvature $R$, and contact angle $\theta$. (Figure 1) Users should be aware that the spherical cap model is unreliable for very small nanoparticles (often around $r$ < 1-2 nm). Here, we illustrate only a case with $\theta > 90$; similar equations (with slight modifications) apply when $\theta \le 90$.


![Spherical cap model of a supported nanoparticle with *θ* > 90. \label{fig:figure1}](paper/Fig1_v3.png)

## Interfacial count
We first consider the entire interfacial region (i.e. interface + perimeter) of thickness $z$ (exaggerated in Figure 1), which is equal to the planar spacing at the nanoparticle-support interface. We calculate the planar spacing using the atomic simulation environment (ASE) [@Larsen:2017] for all facets from {0,0,1} till {3,3,3}. The volume for the entire interfacial region is given by the formula for the volume of a spherical segment:

\begin{equation}\label{eq:ventire}
V_{\text{entire interface}} = \frac{\pi z}{6}\left(3x^2 + 3r^2 + z^2\right)
\end{equation}

where $x$ is the footprint radius at height $z$ above the nanoparticle-support interface. The only unknown term is $x$, which is expressed by Pythagoras’ theorem:

\begin{equation}\label{eq:pythag-offset}
x^2 = R^2 - h^2
\end{equation}


where $R$ is given as:

\begin{equation}\label{eq:R-from-r-theta}
R = \frac{r}{\sin\theta}
\end{equation}

and $h$ is obtained from $R$ by Pythagoras’ theorem:

\begin{equation}\label{eq:R2-r2-hz2}
R^2 = r^2 + (h+z)^2
\end{equation}


Thus, $x$ is given as:

\begin{equation}\label{eq:x2-r2-hz2-h2}
x^2 = r^2 + (h+z)^2 - h^2
\end{equation}


We can then convert the entire interfacial volume $V_{\text{entire interface}}$ to the number of interfacial + perimeter atoms $N_{\text{entire interface}}$:

\begin{equation}\label{eq:N-entire-interface}
N_{\text{entire interface}}=\frac{V_{\text{entire interface}}}{V_M}\,N_A
\end{equation}

where $N_A$ is Avogadro’s number and $V_M$ is the molar volume, calculated with ASE.

A faster method, which does not consider $\theta$ and hence assumes a negligible thickness of the interfacial region, calculates the number of interfacial atoms thus:

\begin{equation}\label{eq:N-entire-from-sigmaA}
N_{\text{entire interface}}=\sigma_{\text{interface}}\times A_{\text{entire interface}}
\end{equation}

where $\sigma_{\text{interface}}$ is the *atomic surface density (atoms per unit area) at the interface and $A_{\text{entire interface}}$ is the area of the entire interface. $A_{\text{entire interface}}$ *is calculated by:

\begin{equation}\label{eq:A-entire-interface}
A_{\text{entire interface}}=\pi r^2
\end{equation}

and $\sigma_{\text{interface}}$, thus:

\begin{equation}\label{eq:sigma-interface}
\sigma_{\text{interface}}=\frac{z\,N_A}{V_M}
\end{equation}


Lastly, as what we have called the “entire interface” is comprised of the interface and the perimeter, we have the number of interfacial atoms, $N_{\text{interface}}$ as:

\begin{equation}\label{eq:N-interface-diff}
N_{\text{interface}} = N_{\text{entire interface}} - N_{\text{perimeter}}
\end{equation}

The procedure for estimating $N_{\text{perimeter}}$ is described below.

## Perimeter count
We assume that the entire interface is an annular ring of thickness $D$, which is the diameter of an atom of the nanoparticle and therefore the thickness of the perimeter. Thus, the radius of the interface is $r-D$. The volume of the interface $V_{\text{interface}}$ is therefore calculated with \autoref{eq:ventire}, where $r-D$ is substituted for $r$. Note that before applying \autoref{eq:ventire}, $x$ is also recalculated using \autoref{eq:x2-r2-hz2-h2}, with $r-D$ substituted for $r$.
The perimeter’s volume $V_{\text{perimeter}}$ is:

\begin{equation}\label{eq:V-perimeter-diff}
V_{\text{perimeter}}=V_{\text{entire interface}}-V_{\text{interface}}
\end{equation}

$N_{\text{perimeter}}$ is then calculated using \autoref{eq:N-entire-interface}, with $V_{\text{perimeter}}$ *substituted for $V_{\text{entire interface}}$.
Using the area-based method, we can calculate $N_{\text{perimeter}}$ using \autoref{eq:N-entire-from-sigmaA}, \autoref{eq:A-entire-interface}, and \autoref{eq:sigma-interface}, but with \autoref{eq:A-entire-interface} modified to:

\begin{equation}\label{eq:A-perimeter-annulus}
A_{\text{perimeter}}=\pi r^2-\pi(r-D)^2
\end{equation}


## Total count
The total volume $V_{\text{total}}$ of the nanoparticle uses the formula:

\begin{equation}\label{eq:V-total-alpha-beta}
V_{\text{total}}=\frac{\pi r^3\,\alpha(\theta)\,\beta(\theta)}{3}
\end{equation}

where:

\begin{equation}\label{eq:alpha-theta}
\alpha(\theta)=\frac{1}{1+\cos\theta}
\end{equation}

and:

\begin{equation}\label{eq:beta-theta}
\beta(\theta)=\frac{(2+\cos\theta)(1-\cos\theta)}{\sin\theta}
\end{equation}


The total number of atoms $N_{\text{total}}$ is then calculated using \autoref{eq:N-entire-interface}, with $N_{\text{total}}$ substituted for $N_{\text{entire interface}}$

## Surface count
From \autoref{fig:figure1}, it can be seen that:

\begin{equation}\label{eq:cos-180-theta}
\cos(180^\circ-\theta)=-\cos\theta=\frac{h+z}{R}
\end{equation}

Which gives:

\begin{equation}\label{eq:h-plus-z}
h+z=-R\cos\theta
\end{equation}

Similarly:

\begin{equation}\label{eq:cos-180-theta-prime}
\cos(180^\circ-\theta')=-\cos\theta'=\frac{h}{R}
\end{equation}

Which gives:

\begin{equation}\label{eq:h-theta-prime}
h=-R\cos\theta'
\end{equation}


Therefore:

\begin{equation}\label{eq:h-equivalence}
h \equiv \left(h+z\right) - z = -R\cos\theta - z = -R\cos\theta'
\end{equation}

Dividing through by $-R$ gives:

\begin{equation}\label{eq:cos-theta-prime}
\cos(\theta')=-\frac{h}{R}=\frac{z}{R}+\cos\theta
\end{equation}

Which gives us the contact angle at height $z$ (i.e. $\theta'$). The surface area of the region of the nanoparticle above $z$ (i.e. the surface area excluding the area of the perimeter) is calculated with the formula for the curved surface area of a spherical cap:

\begin{equation}\label{eq:A-curved-surface}
A_{\text{curved surface}} = 2\pi r^2\,\alpha(\theta')
\end{equation}

The atomic density at the surface is calculated similarly to \autoref{eq:sigma-interface}:

\begin{equation}\label{eq:sigma-surface}
\sigma_{\text{surface}}=\frac{z_{\text{surface}}\,N_A}{V_M}
\end{equation}

where $z_{\text{surface}}$ is the planar spacing at the nanoparticle’s outer surface.
Finally, the number of surface atoms (excluding the perimeter atoms) is calculated with \autoref{eq:N-entire-from-sigmaA}, substituting $A_{\text{curved surface}}$ for $A_{\text{entire interface}}$ and $\sigma_{\text{surface}}$ for $\sigma_{\text{interface}}$.


# Availability
Version 0.1.4 of `NanoparticleAtomCounter` is freely available under the MIT License. The source code, tests, examples, and documentation are hosted at https://github.com/szilvasi-group/NanoparticleAtomCounter. The web version is hosted at https://nanoparticle-atom-counting.streamlit.app/.

# Acknowledgements
This work is funded by the National Science Foundation (NSF) under grant number 2245120. G.O. would like to acknowledge financial support from the University of Alabama Graduate School as a Graduate Council Fellow. The authors also thank Tristan Maxson for useful comments and his contributions to an earlier version of the code.

# References


