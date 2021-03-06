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
from AbstractNeutronComponent import AbstractNeutronComponent as base
class DiskChopper(base):
    theta_0 = 0
    R = 0
    h = 0.0
    omega = 0
    n = 3.0
    j = 0.0
    theta_1 = 0.0
    t_0 = 0.0
    IsFirst = 0.0
    n_pulse = 1.0
    abs_out = 1.0
    phi_0 = 0.0
    w = 0.0
    wc = 0.0
    compat = 0.0
    def customizeLubanObjectDrawer(self, drawer):
        drawer.mold.sequence = ['componentname', 'short_description', 'referencename', 'position', 'orientation', 'theta_0', 'R', 'h', 'omega', 'n', 'j', 'theta_1', 't_0', 'IsFirst', 'n_pulse', 'abs_out', 'phi_0', 'w', 'wc', 'compat']
InvBase=base.Inventory
class Inventory(InvBase):
    theta_0 = InvBase.d.float(name='theta_0', default=0)
    theta_0.help = '(deg)    Angular width of the slits.'
    R = InvBase.d.float(name='R', default=0)
    R.help = '(m)      Radius of the disc'
    h = InvBase.d.float(name='h', default=0.0)
    h.help = '(m)      Slit height (if = 0, equal to R). Auto centering of beam at h/2.'
    omega = InvBase.d.float(name='omega', default=0)
    omega.help = '(rad/s)  Angular frequency of the Chopper'
    n = InvBase.d.float(name='n', default=3.0)
    n.help = '(1)      Number of slits'
    j = InvBase.d.float(name='j', default=0.0)
    j.help = ''
    theta_1 = InvBase.d.float(name='theta_1', default=0.0)
    theta_1.help = '(deg)    Angular width of optional beamstop in chopper windows'
    t_0 = InvBase.d.float(name='t_0', default=0.0)
    t_0.help = "(s)      Time 'delay'."
    IsFirst = InvBase.d.float(name='IsFirst', default=0.0)
    IsFirst.help = '(0/1)    Set it to 1 for the first chopper position in a cw source'
    n_pulse = InvBase.d.float(name='n_pulse', default=1.0)
    n_pulse.help = '(1)      Number of pulses (Only if IsFirst)'
    abs_out = InvBase.d.float(name='abs_out', default=1.0)
    abs_out.help = '(0/1)    Absorb neutrons hitting outside of chopper radius?'
    phi_0 = InvBase.d.float(name='phi_0', default=0.0)
    phi_0.help = "(deg)    Angular 'delay' (suppresses t_0)"
    w = InvBase.d.float(name='w', default=0.0)
    w.help = "(m)      'width' of slits for compatibility with Chopper.comp"
    wc = InvBase.d.float(name='wc', default=0.0)
    wc.help = "(m)      'width' of beamstops for compatibility with Chopper.comp"
    compat = InvBase.d.float(name='compat', default=0.0)
    compat.help = '(1)      Chopper placement compatible with original Chopper.comp'
    dbtablename = 'diskchoppers'
DiskChopper.Inventory = Inventory
del Inventory
from _ import o2t, NeutronComponentTableBase
DiskChopperTable = o2t(DiskChopper, {'subclassFrom': NeutronComponentTableBase})
# version
__id__ = "$Id$"

# End of file 
