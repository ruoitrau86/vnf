# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from _ import o2t


# data object
from vsat.Trajectory import Trajectory as TrajectoryDO
from vnfb.dom.AtomicStructure import StructureTable

# "Holder" in vnf
from ComputationResult import ComputationResult
Trajectory = o2t(TrajectoryDO, {'subclassFrom': ComputationResult})

#import dsaw.db
#Motion.addColumn(
#    dsaw.db.reference(name='matter', table=StructureTable, backref='motion')
#    )

#PhononDOSTable.datafiles = [
#    'data.idf',
#    ]



# version
__id__ = "$Id$"

# End of file 