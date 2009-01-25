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


from Actor import Actor, action_link, action, actionRequireAuthentication
from vnf.weaver import action_href

class Sample2(Actor):

    class Inventory(Actor.Inventory):

        import time
        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier for a given search"
        
        page = pyre.inventory.str('page', default='empty')

    def default(self, director):
        return self.listall( director )

    def listall(self, director):
        page = director.retrievePage( 'sample' )
        
        main = page._body._content._main
        
        # populate the main column
        document = main.document(title='List of samples')
        document.description = ''
        document.byline = 'byline'

        # retrieve id:record dictionary from db
        clerk = director.clerk
        samples = clerk.indexSamples().values()
        #samples = clerk.indexScatterers().values()
        from vnf.utils.uniquelist import uniquelist
        from vnf.dom.hash import hash
        samples = uniquelist(samples, idfun=lambda sample: hash(sample, clerk.db))
            
        document.contents.append(sampletable(samples, director))
        
        p = document.paragraph()
        p.text = [
            action_link(
                actionRequireAuthentication(
                    'sampleInput', 
                    director.sentry,
                    label = 'Add a new sample',
                    routine = 'default'            
                    ),
                director.cgihome,
                ),
            ]

        return page  


    def __init__(self, name=None):
        if name is None:
            name = "sample"
        super(Sample2, self).__init__(name)
        return


        columnTitles = [
            'Sample description','Chemical formula', 'Cartesian lattice', 
            'Atom positions', 'Shape']


def sampletable(samples, director):
    from vnf.content.table import Model, View, Table
    class model(Model):
        
        description = Model.Measure(name='description', type='text')
        chemical_formula = Model.Measure(name='chemical_formula', type='text')
        cartesian_lattice = Model.Measure(name='cartesian_lattice', type='text')
        atom_positions = Model.Measure(name='atom_positions', type='text')
        shape = Model.Measure(name='shape', type='text')

    class D: pass
    import operator
    generators = {
        'description': operator.attrgetter( 'short_description' ),
        'chemical_formula': lambda s: format_chemical_formula(s.matter, director),
        'cartesian_lattice': lambda s: format_lattice_parameters(s.matter, director),
        'atom_positions': lambda s: format_atoms(s.matter, director),
        'shape': lambda s: format_shape(s.shape, director),
        }
    def d(s):
        r = D()
        for attr, g in generators.iteritems():
            value = g(s)
            setattr(r, attr, value)
            continue
        return r
    data = [d(s) for s in samples]

    class view(View):
        
        columns = [
            View.Column(id='col1',label='Sample description', measure='description'),
            View.Column(id='col2',label='Chemical formula', measure='chemical_formula'),
            View.Column(id='col3',label='Cartesian Lattice', measure='cartesian_lattice'),
            View.Column(id='col4',label='Atom positions', measure='atom_positions'),
            View.Column(id='col5',label='Shape', measure='shape'),
            ]

        editable = False

    table = Table(model, data, view)
    return table


def format_chemical_formula( matter,director ):
    if nullpointer(matter): return "undefined"
    matter = director.clerk.dereference(matter)
    return matter.chemical_formula


def format_lattice_parameters(matter, director):
    if nullpointer(matter): return "undefined"
    matter = director.clerk.dereference(matter)
    
    lattice = matter.cartesian_lattice
    import numpy
    lattice = numpy.array(lattice)
    lattice.shape = -1,3
    return '\n'.join( [ format_vector( vec ) for vec in lattice ] )


def format_atoms(matter, director):
    if nullpointer(matter): return "undefined"
    matter = director.clerk.dereference(matter)

    coords = matter.fractional_coordinates
    import numpy
    coords = numpy.array(coords)
    coords.shape = -1,3
    atom_symbols = matter.atom_symbols
    return '\n'.join(
        [ '%s: %s' % (symbol, format_vector(coord) )
          for symbol, coord in zip(atom_symbols, coords) ]
        )


def format_vector( v ):
    x,y,z = v
    return '%.5f, %.5f, %.5f' % (x,y,z)


class ShapeFormatter:

    def __call__(self, shape):
        handler = 'on%s' % shape.__class__.__name__
        handler = getattr( self, handler )
        return handler( shape )


    def onBlock(self, block):
        texts = [
            'Plate',
            'thickness=%.3fcm' % (block.thickness * 100),
            'height=%.3fcm' % (block.height * 100),
            'width=%.3fcm' % (block.width * 100),
            ]
        return '\n'.join( texts )
    
    def onCylinder(self, cylinder):
        texts = [
            'Cylinder',
            'height=%.3fcm' % (cylinder.height * 100),
            'inner radius=%.3fcm' % (cylinder.innerradius * 100),
            'outer radius=%.3fcm' % (cylinder.outerradius * 100),
            ]
        return '\n'.join( texts )

def format_shape( shape, director ):
    if nullpointer(shape): return "undefined"
    shape = director.clerk.dereference(shape)
    return ShapeFormatter()( shape )


from misc import nullpointer

# version
__id__ = "$Id$"

# End of file 
