# __init__.py is the top level file in a Python package.

from quixote.publish import Publisher

# this imports the class RootDirectory from the file 'root.py'
from .root import RootDirectory
from . import html, image

def create_publisher():
     p = Publisher(RootDirectory(), display_exceptions='plain')
     p.is_thread_safe = True
     return p
 
def setup():                            # stuff that should be run once.
    html.init_templates()

    fp = open('imageapp/dice.png', 'rb')
    some_data = fp.read()
    image.add_image('imageapp/dice.pnh', some_data)
    fp.close()

def teardown():                         # stuff that should be run once.
    pass