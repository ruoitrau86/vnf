# -*- Python -*-
# auto-generated by mcstas-component-to-dom
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
from MonitorBase import MonitorBase as base
class PSDMonitor(base):

    abstract = False
    nx = 90.0
    ny = 90.0
    x_min = 0.0
    x_max = 0.0
    y_min = 0.0
    y_max = 0.0
    x_width = 0.0
    y_height = 0.0
    def customizeLubanObjectDrawer(self, drawer):
        drawer.mold.sequence = ['componentname', 'short_description', 'referencename', 'position', 'orientation', 'nx', 'ny', 'x_min', 'x_max', 'y_min', 'y_max', 'x_width', 'y_height']
InvBase=base.Inventory
class Inventory(InvBase):
    nx = InvBase.d.float(name='nx', default=90.0)
    nx.help = 'Number of pixel columns (1)'
    ny = InvBase.d.float(name='ny', default=90.0)
    ny.help = 'Number of pixel rows (1)'
    x_min = InvBase.d.float(name='x_min', default=0.0)
    x_min.help = 'Lower x bound of detector opening (m)'
    x_max = InvBase.d.float(name='x_max', default=0.0)
    x_max.help = 'Upper x bound of detector opening (m)'
    y_min = InvBase.d.float(name='y_min', default=0.0)
    y_min.help = 'Lower y bound of detector opening (m)'
    y_max = InvBase.d.float(name='y_max', default=0.0)
    y_max.help = 'Upper y bound of detector opening (m)'
    x_width = InvBase.d.float(name='x_width', default=0.0)
    x_width.help = 'Width/diameter of detector (x). Overrides x_min,x_max. (m)'
    y_height = InvBase.d.float(name='y_height', default=0.0)
    y_height.help = 'Height of detector (y). Overrides y_min,y_max. (m)'
    dbtablename = 'psdmonitors'
PSDMonitor.Inventory = Inventory
del Inventory
from _ import o2t, MonitorTableBase
PSDMonitorTable = o2t(PSDMonitor, {'subclassFrom': MonitorTableBase})
# version
__id__ = "$Id$"

# End of file 