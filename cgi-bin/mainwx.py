
app = 'wxmain.py'

import os

#The "request" object passed from simple http server
#convert it to a query string
try:
    request
    query_string = '&'.join( '%s=%s' % (k, ','.join(v)) for k,v in request.iteritems() )
except NameError:
    import sys
    request = dict([item[2:].split("=") for item in sys.argv[1:]])
    query_string = '&'.join( '%s=%s' % (k,v) for k,v in request.iteritems() )
os.environ['QUERY_STRING'] = query_string


import tempfile
d = tempfile.mkdtemp()
out = os.path.join(d, 'out.html')
err = os.path.join(d, 'err.html')

cmd = "%s >%s  2>%s" % (webapp, out, err)
if os.system( cmd ):
    print open( err ).read()
else:
    lines = open( out ).readlines()
    print ''.join( lines[1:] )

import shutil
shutil.rmtree(d)
