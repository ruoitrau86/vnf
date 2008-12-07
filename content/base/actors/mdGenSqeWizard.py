from vnf.components.MaterialSimulationWizard import \
     actionRequireAuthentication, action_link, AuthenticationError, InputProcessingError

from vnf.components.MaterialSimulationWizard import MaterialSimulationWizard as base


class MdGenSqeWizard(base):
    
    
    class Inventory(base.Inventory):
        
        import pyre.inventory
        

    def configureSimulation(self, director, matter=None):
        self.inventory.type = 'gulpsimulations'
        if matter:
            self.inventory.mattertype = matter.__class__.__name__
            self.inventory.matterid = matter.id

        try:
            page = director.retrieveSecurePage( 'materialsimulationwizard' )
        except AuthenticationError, err:
            return err.page
    
    
    def kernel_generator(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main
        document = main.document(title='Kernel Generator' )
        document.byline = '<a href="http://danse.us">DANSE</a>'        
        
        formcomponent = self.retrieveFormToShow( 'inelasticScatteringIntensity')
        formcomponent.director = director
        # build the form form
        form = document.form(name='', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'neutronexperimentwizard', 
            sentry = director.sentry,
            routine = 'submit_experiment',
            label = '',
            id = self.inventory.id,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        next = form.control(name='submit',type="submit", value="next")
#        self._footer( document, director )
        return page  