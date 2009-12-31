# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


#from Monitor import Monitor as base
from AbstractNeutronComponent import AbstractNeutronComponent as base
class NeutronRecorder(base):

    packetsize = 10000
    
    pass


InvBase=base.Inventory
class Inventory(InvBase):

    packetsize = InvBase.d.int(name='packetsize', default=10000, validator=InvBase.v.positive)

    dbtablename = 'neutronrecorders'



NeutronRecorder.Inventory = Inventory
del Inventory


from _ import o2t, AbstractOwnedObjectBase
NeutronRecorderTable = o2t(NeutronRecorder, {'subclassFrom':AbstractOwnedObjectBase})


# version
__id__ = "$Id$"

# End of file 