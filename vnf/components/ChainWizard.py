'''
This actor gives the user a menu for performing analysis of his 
simulations/models and several follow-up forms for configuring those analyses.
'''

from vnf.components.SimulationWizard import SimulationWizard
from vnf.components.Actor import actionRequireAuthentication, action, action_link, \
actionRequireAuthentication, action_link, AuthenticationError
from vnf.components.FormActor import InputProcessingError


class ChainWizard(SimulationWizard):
    
    class Inventory(SimulationWizard.Inventory):

        import pyre.inventory
        
        previousSimulationId = pyre.inventory.str("previousSimulationId", default='')
        previousSimulationId.meta['tip'] = "the unique identifier of the previous simulation"

    def default(self, director):
        return self.chainMenu( director )


    def chainMenu(self, director):
        try:
            page = director.retrieveSecurePage( 'generic' )
        except AuthenticationError, err:
            return err.page

        main = page._body._content._main
        document = main.document(title='Material Analysis')
        
        formcomponent = self.retrieveFormToShow( 'selectAnalysisEngine')
        formcomponent.director = director
        #build the form 
        form = document.form(name='', action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(          
            actor = 'chainwizard', 
            sentry = director.sentry,
            routine = 'verifySimulationTypeSelection',
            analysisType = self.inventory.simType,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        next = form.control(name='submit',type="submit", value="next")
        return page 
        
        
    def verifySimulationTypeSelection(self, director):
        '''send to the right method, or form, based on what analytic method is chosen'''
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        self.inventory.simType = simType = self.processFormInputs(director)
        # create a new simulation
        simulation = self._createSimulation(director)
        if simType in ['vacfcomputations']:
            wizard = 'mdanalysiswizard'
        else:
            wizard = 'phononsfromabinitio' # this is not yet done correctly
        #wizard = self._wizardname(type, director)
        routine = 'configureSimulation'
        return director.redirect(wizard, routine, simId = simulation.id, simType=simulation.name)
    
    
    def saveSimulation(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        #nothing need to be done.
        #just go to the simulation list
        actor = 'chainwizard'; routine = 'listall'
        return director.redirect(actor=actor, routine=routine)


    def cancel(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page 

        simulation = self._getSimulation(director)
        # remove this simulation
        if simulation: director.clerk.deleteRecord(simulation)
        
        # redirect
        actor = 'chainwizard'; routine = 'listall'
        return director.redirect(actor=actor, routine=routine)


    def __init__(self, name=None):
        if name is None:
            name = "chainwizard"
        super(ChainWizard, self).__init__(name)
        return


    def _retrievePage(self, director):
        return director.retrieveSecurePage('generic')
    