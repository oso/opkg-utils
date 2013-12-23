#!/usr/bin/env python
#
# vim:sw=4:ts=4:expandtab
#
# Note: We could have use the list() method of tarfile to get the file content
#  but it does not set the first bit of the ls output...

import datetime
import opkg
import os
import sys
import stat
import md5
import sha

def opkg_data_hash(pkg, hfn):
    tarinfos = pkg.get_data_members()
    for tarinfo in tarinfos:
        if tarinfo.isfile() is False:
            continue

        f = pkg.extractfile(tarinfo)
        h = hfn.new()
        while True:
            buf = f.read()
            if len(buf) == 0:
                break

            h.update(buf)

        f.close()

        print("%s\t%s" % (h.hexdigest(), tarinfo.name))

def opkg_hash(package, hfn = md5, header = False):
    if not os.path.isfile(package):
        sys.stderr.write("%s: %s doesn't exist\n" % (sys.argv[0], package))
        return 1

    pkg = opkg.Package(package)
    tarinfos = pkg.get_data_members()

    if header is True:
        print("%s:" % package)

    opkg_data_hash(pkg, hfn)
