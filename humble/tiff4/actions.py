#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    shelltools.export("CFLAGS", "%s -fno-strict-aliasing" % get.CFLAGS())

    autotools.autoreconf("-vfi")
    options = "--disable-static \
               --disable-rpath \
               --without-x \
               --enable-cxx \
               --with-pic"

    if get.buildTYPE() == "emul32":
        options += " --prefix=/emul32 --libdir=/usr/lib32"
        shelltools.export("CC", "%s -m32" % get.CC())
        shelltools.export("CXX", "%s -m32" % get.CXX())

    autotools.configure(options)

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    if get.buildTYPE() == "emul32":
        pisitools.removeDir("/emul32")
        pisitools.remove("/usr/lib32/libtiff.so")
        pisitools.remove("/usr/lib32/libtiffxx.so")
    else:
        pisitools.remove("/usr/lib/libtiff.so")
        pisitools.remove("/usr/lib/libtiffxx.so")

    # pisitools.rename("/%s/tiff-%s" % (get.docDIR(), get.srcVERSION()), get.srcNAME())
