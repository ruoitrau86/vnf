# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                            Jiao Lin, Alex Dementsov
#                      California Institute of Technology
#                        (C) 2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from vnfb.dom.neutron_experiment_simulations.neutron_components.LMonitor import LMonitor

from luban.components.Actor import Actor
import luban.orm
base = luban.orm.object2actor(LMonitor)
class Actor(base):

    class Inventory(base.Inventory):

        import luban.inventory



def actor():
    return Actor('orm/lmonitors')


__date__ = "$Sep 12, 2010 7:23:01 AM$"


