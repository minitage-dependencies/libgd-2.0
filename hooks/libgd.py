import logging
import os

import zc.buildout

log = logging.getLogger('libgd hook')

def pre_configure(options, buildout):
    """Custom pre-make hook for building libgd"""
    #relibtoolize project"
    os.system("libtoolize --copy --force")



