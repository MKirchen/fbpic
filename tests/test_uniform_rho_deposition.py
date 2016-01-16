"""
This test file is part of FB-PIC (Fourier-Bessel Particle-In-Cell).

It verifies the validity of the charge density deposition by:
- Initializing a uniform electron plasma and verifying
  that the deposited density is uniform
  (i.e. this confirms that no Verboncoeur-type correction is needed)
- Shifting this plasma by a small amount in r, and still verifying
  that the deposited density is uniform

Usage :
from the top-level directory of FBPIC run
$ python tests/test_uniform_rho_deposition.py
"""
from scipy.constants import c, e
from fbpic.main import Simulation
import matplotlib.pyplot as plt
import numpy as np

# Parameters
# ----------
show = True     # Whether to show the results to the user, or to
                # automatically determine if they are correct.

# Dimensions of the box
Nz = 250
zmax = 20.e-6
Nr = 50
rmax= 20.e-6
Nm = 2
# Particles
p_nr = 3
p_nz = 2
p_nt = 4
p_rmax = 10.e-6
n = 9.e24
# Shift of the electrons, as a fraction of dr
frac_shift = 0.01

# -------------
# Test function
# -------------

def test_uniform_electron_plasma(show=False):
    "Function that is run by py.test, when doing `python setup.py test`"

    # Initialize the different structures
    sim = Simulation( Nz, zmax, Nr, rmax, Nm, zmax/Nz/c,
        0, zmax, 0, p_rmax, p_nz, p_nr, p_nt, n,
        initialize_ions=False )

    # Deposit the charge
    sim.fld.erase('rho')
    for species in sim.ptcl :
        species.deposit( sim.fld, 'rho')
    sim.fld.divide_by_volume('rho')

    # Check that the density has the correct value
    if show is False:
        # Integer index at which the plasma stops
        Nrmax = int( Nr * p_rmax * 1./rmax  )
        # Check that the density is correct in mode 0, below this index
        assert np.allclose( -n*e,
            sim.fld.interp[0].rho[:,:Nrmax-2], 1.e-10 )
        # Check that the density is correct in mode 0, above this index
        assert np.allclose( 0,
            sim.fld.interp[0].rho[:,Nrmax+2:], 1.e-10 )
        # Check the density in the mode 1
        assert np.allclose( 0,
            sim.fld.interp[1].rho[:,:], 1.e-10 )

    # Show the results
    else:
        plt.title('Uniform plasma, mode 0')
        sim.fld.interp[0].show('rho')
        plt.show()
        plt.title('Uniform plasma, mode 1')
        sim.fld.interp[1].show('rho')
        plt.show()

def test_neutral_plasma_shifted(show=False):
    "Function that is run by py.test, when doing `python setup.py test`"

    # Initialize the different structures
    sim = Simulation( Nz, zmax, Nr, rmax, Nm, zmax/Nz/c,
        0, zmax, 0, p_rmax, p_nz, p_nr, p_nt, n,
        initialize_ions=True )

    # Shift the electrons
    dr = rmax/Nr
    sim.ptcl[0].x += frac_shift * dr

    # Deposit the charge
    sim.fld.erase('rho')
    for species in sim.ptcl :
        species.deposit( sim.fld, 'rho')
    sim.fld.divide_by_volume('rho')

    # Check that the density has the correct value
    if show is False:
        # Integer index at which the plasma stops
        Nrmax = int( Nr * p_rmax * 1./rmax  )
        # Check that the density is correct in mode 0, below this index
        assert np.allclose( 0,
            sim.fld.interp[0].rho[:,:Nrmax-2], atol=n*e*1.e-6 )
        assert np.allclose( 0,
            sim.fld.interp[1].rho[:,:Nrmax-2], atol=n*e*1.e-3 )
        # Check that the density is correct in mode 0, above this index
        assert np.allclose( 0,
            sim.fld.interp[0].rho[:,Nrmax+2:], 1.e-10 )
        # Check the density in the mode 1
        assert np.allclose( 0,
            sim.fld.interp[1].rho[:,Nrmax+2:], atol=n*e*1.e-3 )

    # Show the results
    else:
        plt.title('Shifted plasma, mode 0')
        sim.fld.interp[0].show('rho')
        plt.show()
        plt.title('Shifted plasma, mode 1')
        sim.fld.interp[1].show('rho')
        plt.show()

if __name__ == '__main__' :

    test_uniform_electron_plasma(show)
    test_neutral_plasma_shifted(show)
