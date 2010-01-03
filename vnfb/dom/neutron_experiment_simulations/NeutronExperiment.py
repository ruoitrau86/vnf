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


from Instrument import Instrument
from SampleAssembly import SampleAssembly
from SampleEnvironment import SampleEnvironment


class NeutronExperiment:

    # instrument
    instrument = None
    instrument_configuration = None

    # sample
    sample = None

    # sample environment
    sampleenvironment = None
    
    ncount = 1e6


from instrument_configuration_types import getTypes
instrument_configuration_types = getTypes()
instrument_configuration_types.append(Instrument)


from samplecomponent_types import getTypes
samplecomponent_types = getTypes()
from SampleEnvironment import SampleEnvironment

from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    dbtablename = 'neutronexperiments'

    instrument = InvBase.d.reference(name = 'instrument', targettype = Instrument, owned=0)
    instrument_configuration = InvBase.d.reference(
        name = 'instrument_configuration',
        targettypes = instrument_configuration_types,
        owned = 1,
        )

    sample = InvBase.d.reference(
        name = 'sample',
        targettype=None,
        targettypes = [SampleAssembly] + samplecomponent_types,
        owned = 0)
    
    sampleenvironment = InvBase.d.reference(
        name = 'sampleenvironment', targettype = SampleEnvironment, owned = 1)

    ncount = InvBase.d.float(name = 'ncount', default = 1e6)

    # constructed = InvBase.d.varchar( name = 'constructed', length = 4, default = '' )

    # status = InvBase.d.varchar( name = 'status', length = 32, default = '' )
    # started: just started to be configured
    # partially configured: configuration not done
    # ready for submission: configuration done and ready for submission, job not created yet
    # constructed: configuration done and job created.
    # deleted: experiment is deleted

    # expected_results = InvBase.d.varcharArray( name = 'expected_results', length = 128 )

NeutronExperiment.Inventory = Inventory
del Inventory


from _ import o2t, AbstractOwnedObjectBase as TableBase
NeutronExperimentTable = o2t(NeutronExperiment, {'subclassFrom': TableBase})
    

# version
__id__ = "$Id$"

# End of file 
