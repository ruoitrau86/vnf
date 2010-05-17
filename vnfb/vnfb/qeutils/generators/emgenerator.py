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

from vnfb.qeutils.qeparser.namelist import Namelist
from vnfb.qeutils.qeparser.card import Card

# Default Control params
CALCULATION     = "'cp'"
RESTART_MODE    = "'from_scratch'"
TSTRESS         = ".true."
TPRNFOR         = ".true."
NDR             = "51"
NDW             = "51"
IPRINT          = "10"
ISAVE           = "100"
ETOT_CONV_THR   = "1.d-4"
EKIN_CONV_THR   = "1.d-6"


# Default System params
CELLDM          = "10.2"

# Default Electron params
EMASS_CUTOFF            = "2.5"
ORTHOGONALIZATION       = "'ortho'"
ELECTRON_DYNAMICS       = "'sd'"
ELECTRON_TEMPERATURE    = "'not_controlled'"

# Default Ion params
ION_DYNAMICS        = "'none'"
ION_TEMPERATURE     = "'not_controlled'"

# Default Cell params
CELL_DYNAMICS       = "'none'"

# XXX: Critical: celldm(1) is created incorrectly from atomic structure
#   Quick fix: set fixed value!
class EMGenerator(object):
    "Generator for CP Electronic Minimization task"
    
    def __init__(self, director, inventory, input = None):
        self._director  = director
        self._inv       = inventory
        self._input     = input


    def setControl(self):
        "CONTROL namelist"
        control = Namelist("control")
        self._input.addNamelist(control)
        control.add("calculation",  CALCULATION)
        control.add("restart_mode", RESTART_MODE)
        control.add("ndr",          NDR)
        control.add("ndw",          NDW)
        control.add("nstep",        self._inv.nstep)
        control.add("iprint",       IPRINT)
        control.add("isave",        ISAVE)
        control.add("tstress",      TSTRESS)
        control.add("tprnfor",      TPRNFOR)
        control.add("dt",           self._inv.dt)
        control.add("etot_conv_thr", ETOT_CONV_THR)
        control.add("ekin_conv_thr", EKIN_CONV_THR)


    def setSystem(self):
        "SYSTEM namelist"
        system  = self._input.namelist("system")  # System namelist already exists
        system.add("ecutwfc", self._inv.ecutwfc)
        system.set("celldm(1)", CELLDM) # XXX: Hack


    def setElectrons(self):         # TODO: Suitable for phonon calculations?
        "ELECTRONS namelist"
        electrons   = Namelist("electrons")
        self._input.addNamelist(electrons)
        electrons.add("emass",                  self._inv.emass)
        electrons.add("emass_cutoff",           EMASS_CUTOFF)
        electrons.add("orthogonalization",      ORTHOGONALIZATION)
        electrons.add("electron_dynamics",      ELECTRON_DYNAMICS)
        electrons.add("electron_temperature",   ELECTRON_TEMPERATURE)


    def setIons(self):
        ions        = Namelist("ions")
        self._input.addNamelist(ions)
        ions.add("ion_dynamics",        ION_DYNAMICS)
        ions.add("ion_temperature",     ION_TEMPERATURE)


    def setCell(self):
        cell    = Namelist("cell")
        self._input.addNamelist(cell)
        cell.add("cell_dynamics",   CELL_DYNAMICS)


    def toString(self):
        return self._input.toString()


    
__date__ = "$May 16, 2010 10:01:22 AM$"

