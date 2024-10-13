try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

import pycdlib

iso = pycdlib.PyCdlib()
iso.new()

foostr = b'foo\n'
iso.add_fp(BytesIO(foostr), len(foostr), '/FOO.;1')

iso.add_directory('/DIR1')

iso.write('new.iso')
iso.close()
