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


from OwnedObject import OwnedObject as base1
from ComputationResult import ComputationResult as base2
class PhononDispersion(base1, base2):

    name = 'phonondispersions'

    datafiles = [
        'DOS',
        'Omega2',
        'Polarizations',
        'Qgridinfo',
        ]
    
    pass # end of Dispersion


def inittable(db):
    def new(id):
        r = PhononDispersion()
        r.id = id
        return r

    records = [
        new('phonon-dispersion-fccNi-0'),
        ]

    for r in records: db.insertRow(r)
    return


# version
__id__ = "$Id$"

# End of file 
