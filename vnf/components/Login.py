#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Actor import Actor


class Login(Actor):

    class Inventory(Actor.Inventory):

        import pyre.inventory



    def default(self, director):
        page = director.retrievePage( 'login' )

        main = page._body._content._main

        # populate the main column
        document = main.document( title = 'login' )
        document.description = ('You have successfully logged out.')
        
        # build the login form
        login = document.form(
            name='login', legend='Account details', action=director.cgihome)
        
        actor = login.hidden(name='actor', value='greet')
        attempts = login.hidden(name='sentry.attempts', value=str(director.sentry.attempts))
        
        username = login.text(id='username', name='sentry.username', label='Username')
        username.help = 'Usernames are case sensitive; make sure your caps lock key is not enabled.'
        
        password = login.password(id='password', name='sentry.passwd', label='Password')
        password.help = (
            'Passwords are also case sensitive. If you have forgotten your password, you may '
            'be able to <a href="%s?actor=retrieve-password">retrieve</a> it.' % director.cgihome)
        
        submit = login.control(name="submit", type="submit", value="login")
        
        p = login.paragraph()
        p.text = [
            'When you are done, please logout or exit your browser'
            ]
        
        return page


    def __init__(self, name=None):
        if name is None:
            name = "login"
        super(Login, self).__init__(name)
        return


    pass # end of Login


# version
__id__ = "$Id$"

# End of file 
