# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# base class for visual factory root
# it contains various factories for building visuals
# those factories may still have sub-factories


from BeamProfileStartPanel import Factory as StartPanel
from BeamProfileResultsView import Factory as ResultsView
from BeamProfileTableView import Factory as TableView

from FactoryRoot import FactoryRoot as base
class BeamProfile(base):

    sub_factory_constructors = {
        'start_panel': StartPanel,
        'results_view': ResultsView,
        'table_view': TableView,
        }


# version
__id__ = "$Id$"

# End of file 
