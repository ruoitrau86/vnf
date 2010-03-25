#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

"""
PWGenerator - generates parameters for pw configuration input. 

Notes:
    - Input object is passed from loaded atomic structure
    - ATOMIC_SPECIES card is generated by QECalc

"""

from vnfb.qeutils.qeparser.namelist import Namelist
from vnfb.qeutils.qeparser.card import Card
from vnfb.qeutils.qeconst import SMEARING, MATTER_TYPE, SIMTYPE, RELAXLIST

# Default Control params
CALCULATION     = "'scf'"
RESTART_MODE    = "'from_scratch'"
TPRNFOR         = ".true."

# Default System params
OCCUP_METAL     = "'smearing'"
OCCUP_ISO       = "'fixed'"

# Default Electron params
CONV_THR        = "1.0d-8"
MIXING_BETA     = "0.7"

# Geometry: control
FORC_CONV_THR   = "0.001"
ETOT_CONV_THR   = "0.0001"

# Geometry: ions
ION_DYNAMICS        = "'bfgs'"
POT_EXTRAPOLATION   = "'atomic'"
WFC_EXTRAPOLATION   = "'none'"
UPSCALE             = "10.0"
BFGS_NDIM           = "1"
TRUST_RADIUS_MAX    = "0.8"
TRUST_RADIUS_MIN    = "0.001"
CELL_DYNAMICS       = "'bfgs'"


class PWGenerator(object):

    def __init__(self, inventory, input):
        self._inv       = inventory
        self._input     = input
        self._simtype   = inventory.simtype     # Special case


    def setControl(self):
        "CONTROL namelist"
        control = Namelist("control")
        self._input.addNamelist(control)
        self._addCalculation(control)
        control.add("restart_mode", RESTART_MODE)
        control.add("tprnfor",      TPRNFOR)
        self._addConvParams(control)
        #control.add("prefix", "???")   # Remove 'prefix'


    def setSystem(self):
        "SYSTEM namelist"
        system  = self._input.namelist("system")  # System namelist already exists
        self._addSmearing(system)
        system.add("ecutwfc", self._inv.ecutwfc)
        system.add("ecutrho", self._inv.ecutrho)
        #system.add("nspin", "2")
        #system.add("starting_magnetization(1)", "0.5")

    
    def setElectrons(self):         # TODO: Suitable for phonon calculations?
        "ELECTRONS namelist"
        electrons   = Namelist("electrons")
        electrons.add("conv_thr",       CONV_THR)
        electrons.add("mixing_beta",    MIXING_BETA)
        self._input.addNamelist(electrons)


    def setIons(self):
        if not self._isGeometry():
            return
        
        ions        = Namelist("ions")
        self._input.addNamelist(ions)
        ions.add("ion_dynamics",        ION_DYNAMICS)
        ions.add("pot_extrapolation",   POT_EXTRAPOLATION)
        ions.add("wfc_extrapolation",   WFC_EXTRAPOLATION)
        ions.add("upscale",             UPSCALE)
        ions.add("bfgs_ndim",           BFGS_NDIM )
        ions.add("trust_radius_max",    TRUST_RADIUS_MAX)
        ions.add("trust_radius_min",    TRUST_RADIUS_MIN)


    def setCell(self):
        if not self._isGeometry():
            return

        if self._relax() != "vc-relax":
            return

        # Add cell param for vc-relax only
        nls     = self._input.namelists
        if nls.has_key("cell"):         # Addressing issues in outdated parser in QECalc
            cell    = self._input.namelist("cell")
        else:
            cell    = Namelist("cell")
            self._input.addNamelist(cell)

        cell.add("cell_dynamics", CELL_DYNAMICS)
        

    def setKPoints(self):
        "K_POINTS card"
        k_points   = Card("k_points")
        k_points.setArg("automatic")
        k_points.addLine("%s %s %s 0 0 0" % (self._inv.nk1, self._inv.nk2, self._inv.nk3))
        self._input.addCard(k_points)


    def toString(self):
        return self._input.structure.toString()


    def _addSmearing(self, system):
        types = MATTER_TYPE.keys()

        if types[int(self._inv.mattertype)] == "metal":      # Metal case
            system.add("degauss", self._inv.degauss)
            system.add("smearing", self._smearing())
            system.add("occupations", OCCUP_METAL)

        elif types[int(self._inv.mattertype)] == "insulator": # Insulator
            system.add("occupations", OCCUP_ISO)


    def _smearing(self):
        "Returns smearing parameter for PW config input"
        keys    = SMEARING.keys()
        name    = keys[int(self._inv.smearing)]

        return SMEARING[name]


    def _addCalculation(self, control):
        "Add calculation parameter to control namelist"
        # Geometry optimization specific
        if self._isGeometry() and self._isRelax():
            control.add("calculation", "'%s'" % self._relax()) # Oh, these weird apostrophes
            return

        control.add("calculation", CALCULATION) # Default


    def _addConvParams(self, control):
        if self._isGeometry():  # Geometry optimization specific
            control.add("forc_conv_thr", FORC_CONV_THR)
            control.add("etot_conv_thr", ETOT_CONV_THR)


    def _isGeometry(self):
        "Checks if simulation type is geometry"
        return self._simtype == SIMTYPE["geometry"]


    def _isRelax(self):
        "Checks if relaxation parameter is in range"
        # Example: self._inv.relax == 1 for 'vc-relax'
        return int(self._inv.relax) in range(len(RELAXLIST))


    def _relax(self):
        if self._isRelax():
            return RELAXLIST[int(self._inv.relax)]

        return None

__date__ = "$Mar 21, 2010 8:03:26 AM$"


