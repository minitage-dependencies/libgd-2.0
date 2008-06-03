import os
def pre_configure(options, buildout):
    """Custom pre-make hook for building libgd"""
    #relibtoolize project"
    os.system("""cd %s;
              libtoolize --copy --force""" % (
                  options['compile-directory']
              )
             )

