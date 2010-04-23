#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

"""
QEConvergence - base actor class for Quantum Espresso convergence pages
"""

import luban.content as lc
from luban.content import select, load

from luban.components.AuthorizedActor import AuthorizedActor as base

class QEConvergence(base):

    class Inventory(base.Inventory):
        import pyre.inventory
        id          = pyre.inventory.str('id', default='')          # Simulation Id


    def default(self, director):
        # Redirection doesn't pass value to self.id, so I need to do it manually

        return select(id='main-display-area').replaceContent(self.content(director))


    def content(self, director):
        "Contains of two separate splitters: header and results"
        doc         = lc.document(title="Analysis of Simulation Results")
        splitter    = doc.splitter(orientation="vertical")
        sInd        = splitter.section()                        # path indicator
        sAct        = splitter.section(id="qe-section-actions") # actions

        docResults  = lc.document() #id = ID_RESULTS
        doc.add(docResults)

        self._viewIndicator(director, sInd)
        self._showActions(director, sAct)                 # Show actions

        # Main content
        resSplitter = docResults.splitter(orientation="vertical")
        self._mainContent(director, resSplitter)              # Simulation Specific data

        return doc


    def _viewIndicator(self, director, section):
        path = []
        path.append(('Simulations ', load(actor='materialsimulation')))
        path.append(('Quantum Espresso ', load(actor='materialsimulation')))
        path.append(('%s ' % self.id, load(actor    = 'material_simulations/espresso/sim-view',
                                           id       = self.id)))

        path.append('Convergence Tests')
        section.add(director.retrieveVisual('view-indicator', path=path))


    def _showActions(self, director, section):
        self._backAction(section)
        self._refreshAction(section)
        self._newTestAction(section)
        self._pwInputAction(section)

        section.add(lc.document(Class="clear-both"))


    def _backAction(self, section):
        section.add(lc.link(label="Back",
                            Class="qe-action-back",
                            onclick = load(actor      = 'material_simulations/espresso/sim-view',
                                             id         = self.id))
                    )

    def _refreshAction(self, section):
        section.add(lc.link(label="Refresh",
                            Class="qe-action-back",
                            onclick = load(actor      = 'material_simulations/espresso-convergence/view',
                                             id       = self.id))
                    )

    def _newTestAction(self, section):
        section.add(lc.link(label="Create New Test",
                            Class="qe-action-new",
                            onclick = load(actor      = 'material_simulations/espresso-convergence/test-create',
                                             id         = self.id))
                    )

    def _pwInputAction(self, section):
        "Shows PW input action button"
        section.add(lc.link(label="Create PW Input",
                            Class="qe-action-new",  # qe-action-default
                            onclick = load(actor      = 'material_simulations/espresso/sim-view',
                                             id         = self.id))
                    )


    def _mainContent(self, director, splitter):
        "Main content. Should be overwritten by subclass"


    def _configure(self):
        super(QEConvergence, self)._configure()
        self.id             = self.inventory.id


    def _init(self):
        super(QEConvergence, self)._init()


    def __init__(self, name):
        super(QEConvergence, self).__init__(name=name)


__date__ = "$Apr 22, 2010 5:29:03 PM$"

