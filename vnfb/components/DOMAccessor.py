# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2007-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.components.Component import Component as base


# domaccessor facilitates association of db with the application.
# the application must has facility to
#  1. create a unique ID
#  2. know who is the current user
#
class DOMAccessor( base ):


    db = None
    director = None
    

    def __init__(self, name, facility = 'dom-accessor'):
        super(DOMAccessor, self).__init__(name, facility)
        return


    # initialization methods
    def setApplicationDirector(self, director):
        self.director = director
        return


    def setDB(self, db):
        self.db = db
        return


    def set(self, db=None, director=None):
        if db: self.setDB(db)
        if director: self.setApplicationDirector(director)
        return


    # transient objects
    def isTransient(self, record):
        from vnf.dom.TransientObject import TransientObject
        q = self.db.query(TransientObject).filter_by(
            target = record.globalpointer.id)
        r = q.all()
        return bool(len(r))


    def setTransient(self, record):
        from vnf.dom.TransientObject import TransientObject
        row = TransientObject()
        row.target = record
        self.db.insertRow(row)
        return


    def removeTransient(self, record):
        from vnf.dom.TransientObject import TransientObject
        q = self.db.query(TransientObject).filter_by(
            target = record.globalpointer.id)
        rs = q.all()
        if len(rs)==0: return
        for r in rs:
            self.db.deleteRow(TransientObject, where="id='%s'" % r.id)
            continue
        return
        

    # access to proxy
    def makeProxy(self, record, factory):
        return factory(record, domaccess=self)
    


    # generic accessing methods
    def updateRecordWithID(self, record):
        'update a record. assumes that it has a "id" column'
        return self.db.updateRecord(record)


    def getRecordByID(self, tablename, id):
        from dsaw.db.Table import Table as TableBase
        if isinstance(tablename, basestring):
            Table = self._getTable(tablename)
        elif issubclass(tablename, TableBase):
            Table = tablename
        else:
            raise ValueError, 'tablename must be a string or a table class: %s' % tablename
        return self._getRecordByID(Table, id)
    
    
    def insertNewOwnedRecord(self, table, owner = None):
        '''create a new record for the given table.

        The given table is assumed to have following fields:
          - id
          - creator
          - date
        '''
        if isinstance(table, str): table = self._getTable(table)
        
        director = self.director
        id = director.getGUID()

        record = table()
        record.id = id

        if not owner: 
            owner = director.sentry.username
        record.creator = owner
        
        self.insertNewRecord( record )
        return record


    def insertNewRecordWithID(self, table):
        '''create a new record for the given table and store it in the db.

        The given table is assumed to have following fields:
          - id
        '''
        record = self.createRecordWithID(table)
        return self.insertNewRecord(record)
    
    
    def createRecordWithID(self, table):
        '''create a new record for the given table but do not store it in the db.

        The given table is assumed to have following fields:
          - id
        '''
        record = table()
        
        director = self.director
        id = director.getGUID()
        record.id = id

        return record


    def insertNewRecord(self, record):
        'insert a new record into db'
        try:
            self.db.insertRow( record )
        except:
            columns = record.getColumnNames()
            values = [ record.getColumnValue( column ) for column in columns ]
            s = ','.join(
                [ '%s=%s' % (column, value)
                  for column, value in zip(columns, values)
                  ] )
            self._debug.log( 'failed to insert record: %s' % s)
            raise
        return record


    def deleteRecordWithID(self, record):
        'delete a record. assumes that it has a "id" column'
        self.db.deleteRow(record.__class__, where="id='%s'" % record.id)
        return
    

    def dereference(self, pointer):
        '''dereference a "pointer"'''
        return pointer.dereference(self.db)


    def _getUsername(self):
        return self.director.sentry.username


    def _getTable(self, name):
        return self.db.getTable(name)


    def _getRecordByID(self, table, id ):
        all = self.db.fetchall( table, where = "id='%s'" % id )
        if len(all) == 1:
            return all[0]
        raise RuntimeError, "Cannot find record of id=%s in table %s" % (
            id, table.__name__)

    def _getAll(self, table, where = None):
        index = {}
        all = self.db.fetchall(table, where=where)
        return all

    
    """Auxiliary classes"""
    
    def _getClass(self, classname):
        """Get class from classname"""
        maindom = "vnf.dom"
        module  = _import("%s.%s" % (maindom, classname))
        return getattr(module, classname)


    def _getEntry(self, classname, id=None, where=None):
        """Get entry specified by id or where clause"""
        table = self._getClass(classname)
        if id is not None:
            return self._getRecordByID( table, id )

        return self._getAll(table, where)



class Proxy(object):

    
    def __init__(self, record, domaccess=None):
        self.record = record
        self.domaccess = domaccess
        self.db = domaccess.db
        return


    def __getattr__(self, name):
        o = self._getObject()
        if hasattr(o, name): return getattr(o, name)
        return getattr(self.record, name)


    def _getObject(self):
        if not '_object' in self.__dict__:
            try:
                o = self._convertToObject()
            except:
                import traceback
                raise RuntimeError, 'failed to convert record %s:%s to object: %s' % (
                    self.record.__class__.name, self.record.id, traceback.format_exc())
            
            setattr(self, '_object', o)
        return self._object


    def _setObjectObsolete(self):
        if self.__dict__.has_key('_object'):
            del self.__dict__['_object']


    def _convertToObject(self):
        raise NotImplementedError


def _import(package):
    return __import__(package, {}, {}, [''])


# version
__id__ = "$Id$"

#    # Added from old Clerk, same as updateRecordWithID()?
#    def updateRecord(self, record):
#        """Updates row in the database specified by record.id"""
#        id = record.id
#        where = "id='%s'" % id
#
#        assignments = []
#
#        # get the column names and couple them with the new values
#        for column in record.getColumnNames():
#            value = getattr( record, column )
#            assignments.append( (column, value) )
#            continue
#        # update the row, or in other words, record
#        self.db.updateRow(record.__class__, assignments, where)
#        return record



# End of file 
