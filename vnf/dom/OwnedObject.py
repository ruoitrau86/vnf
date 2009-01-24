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


from User import User

from DbObject import DbObject
class OwnedObject(DbObject):

    import pyre.db

    creator = pyre.db.varchar(name='creator', length=64)

    date = pyre.db.date( name='date' )
    date.meta['tip'] = 'date of creation'

    pass # end of OwnedObject


# version
__id__ = "$Id$"

# End of file 
