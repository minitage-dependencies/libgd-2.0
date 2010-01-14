import os
import re
import sys
def pre_configure(options, buildout):
    """Custom pre-make hook for building libgd"""
    # fix shared build
    libpng = [i 
              for i in os.listdir(os.path.join(buildout['buildout']['directory'], '..')) 
              if 'libpng' in i][-1]
    libpng_path = os.path.abspath(
                    os.path.join(buildout['buildout']['directory'], '..', libpng, 'parts', 'part')
                    )
    print "Using %s" % libpng_path
    if 'cygwin' in sys.platform:
        d = os.path.join(options['compile-directory'], 'configure.ac')
        c = open(d).read()
        flags = "-no-undefined -L%s/lib -L%s/bin" % (libpng_path, libpng_path)
        flags = "-L%s/lib -L%s/bin" % (libpng_path, libpng_path)
        print "patching configure.ac"
        c = c.replace('-lpng12', "%s -lpng" % flags)
        c = c.replace('-lpng ', '%s -lpng '% flags)
        c = c.replace('AC_CHECK_LIB(png,', 'AC_CHECK_LIB(png,')
        c = c.replace('AC_CHECK_LIB(png12,', 'AC_CHECK_LIB(png,')
        c = c.replace('LIBS="-lz', 'LIBS="-lz %s' % flags)
        c = re.sub('libpng_LDFLAGS=".*"', 'libpng_LDFLAGS="%s -lpng"'%flags, c, re.S|re.M|re.U|re.X)
        c = re.sub('libpng_LDFLAGS=`.*`', 'libpng_LDFLAGS="%s -lpng"'%flags, c, re.S|re.M|re.U|re.X)
        open(d, 'w').write(c)

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
             
    # fix static build
    if 'cygwin' in sys.platform:
        for f in ['configure', 'autom4te.cache/output.0', 'autom4te.cache/output.1' , 'config/libtool.m4', 'libtool', 'libtool.m4']:
            d = os.path.join(options['compile-directory'], f)
            if os.path.exists(d):
                print 'patching %s' % f
                c = open(d).read()
                open(d, 'w').write(c.replace('compiler_flags -o', 'compiler_flags -lpng -o'))


# vim:set et ts=4 sts=4:
