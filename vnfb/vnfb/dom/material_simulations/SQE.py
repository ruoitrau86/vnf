# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# data object
class SQE(object):

    matter = None


# orm
from vnfb.dom.AtomicStructure import Structure

from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    matter = InvBase.d.reference(
        name='matter', targettype=None, targettypes=[Structure], owned=0)

    dbtablename = 'sqes'

SQE.Inventory = Inventory


# db table
from ComputationResult import ComputationResult
from _ import o2t
SQETable = o2t(SQE, {'subclassFrom': ComputationResult})
SQETable.histogramh5 = 'sqe.h5'
SQETable.datafiles = [
    SQETable.histogramh5
    ]


# version
__id__ = "$Id$"

# End of file 