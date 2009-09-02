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


from Monitor import Monitor as base
class DetectorSystem_fromXML(base):

    name = 'detectorsystem_fromxmls'

    import dsaw.db

    tofmin = dsaw.db.real( name = 'tofmin', default = 3000. )
    tofmin.meta['tip'] = 'minimum tof. unit: microsecond'
    
    tofmax = dsaw.db.real( name = 'tofmax', default = 6000. )
    tofmax.meta['tip'] = 'maximum tof. unit: microsecond'

    ntofbins = dsaw.db.integer( name = 'ntofbins', default = 300 )
    ntofbins.meta['tip'] = 'number of tof bins'

    pass # end of DetectorSystem_fromXML


# version
__id__ = "$Id$"

# End of file 
