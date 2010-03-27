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

from vnfb.qeutils.results.q2rresult import Q2RResult
from vnfb.qeutils.qeconst import MATDYN_METHOD_LIST
from vnfb.qeutils.qeparser.namelist import Namelist
from vnfb.qeutils.results.pwresult import PWResult
from vnfb.qeutils.generators.phgenerator import PHGenerator

from qecalc.qetask.qeparser.matdyninput import MatdynInput
from vnfb.qeutils.qecalcutils import kmesh

DOS     = ".true."

class MATDYNGenerator(object):

    def __init__(self, director, inventory):
        self._director  = director
        self._inv       = inventory
        self._subtype   = None      # 'dos' or 'dispersion'
        self._input     = None

        self._init()


    def _init(self):
        "Additional init"
        method  = int(self._inv.method) # 0, 1
        if not method in range(len(MATDYN_METHOD_LIST)):  # if out of range
            return

        self._subtype   = MATDYN_METHOD_LIST[method]


    # XXX: nk points still should be present in the input file
    def setInput(self):
        "Populate 'input' namelist"
        q2rresult       = Q2RResult(self._director, self._inv.id)
        phgen           = PHGenerator(self._director, self._inv)
        self._input     = MatdynInput()
        nl              = Namelist("input") # Create namelist
        self._input.addNamelist(nl)

        nl.add("asr",   q2rresult.zasr())   # from Q2R result
        nl.add("flfrc", q2rresult.flfrc())  # from Q2R result
        nl.add("dos",   DOS)
        nl.add("nk1",   self._inv.nk1)
        nl.add("nk2",   self._inv.nk2)
        nl.add("nk3",   self._inv.nk3)

        # Add amasses
        masses    = phgen.amasses() # from PH generator

        if not masses:  # In case if not masses are found in PW input
            nl.add("amass", "ERROR: masses not defined in PW input file!")
            return

        for m in masses:
            nl.add(m[0], m[1])

        if not self._subtype:   # No subtype, no additional parameters
            return  

        # Generate k-points
        if self._subtype == "dispersion":
            self._input.qpoints.set(self._qpoints())
            # Force adding nk1, nk2, nk3 to input
            # This will later be used for exporting dispersion to atomic structure
            nl  = self._input.namelist("input")
            nl.add("nk1",   self._inv.nk1)
            nl.add("nk2",   self._inv.nk2)
            nl.add("nk3",   self._inv.nk3)


    def subtype(self):
        "Return subtype"
        if not self._subtype:
            return ""

        return self._subtype


    def toString(self):
        return self._input.toString()


    def _qpoints(self):
        "Returns qpoints"
        pwresult    = PWResult(self._director, self._inv.id)
        kp          = pwresult.kPoints(formatted=False)
        if not kp:      # No k-points, no q-points
            return

        nqGrid      = [kp[0], kp[1], kp[2]]
        pwinput     = pwresult.input()
        return kmesh.kMeshCart(nqGrid, pwinput.structure.lattice.reciprocalBase())


__date__ = "$Mar 24, 2010 9:59:39 AM$"