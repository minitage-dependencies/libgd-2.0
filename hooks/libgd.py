import os
import sys
def pre_configure(options, buildout):
    """Custom pre-make hook for building libgd"""
    #relibtoolize project"
    os.system("""cd %s;
              libtoolize --copy --force""" % (
                  options['compile-directory']
              )
             )
    os.system("""cd %s;
              autoreconf -iv""" % (
                  options['compile-directory']
              )
             ) 
             

    if 'cygwin' in sys.platform:
        d = os.path.join(options['compile-directory'], 'configure')
        c = open(d).read()
        open(d, 'w').write(
        c.replace('-lpng12', '-no-undefined -lpng-3'
        ).replace('LIBS="-lpng-3', 'LIBS="-lpng'
        ).replace('LIBS="-lz', 'LIBS="-lz -lpng'
        )


        )
        for f in ['configure', 'autom4te.cache/output.0', 'autom4te.cache/output.1' , 'config/libtool.m4', 'libtool', 'libtool.m4']:
            d = os.path.join(options['compile-directory'], f)
            if os.path.exists(d):
                print 'patching %s' % f
                c = open(d).read()
                open(d, 'w').write(
                  #c.replace('--enable-auto-image-base -Xlinker --out-implib -Xlinker', '--enable-auto-image-base -Xlinker --out-implib -Xlinker -lpng')
                  c.replace('compiler_flags -o', 'compiler_flags -lpng -o')
                )






