#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  Any Red Hat
# trademarks that are incorporated in the source code or documentation are not
# subject to the GNU General Public License and may only be used or replicated
# with the express permission of Red Hat, Inc. 
#
import string

from pykickstart.base import *
from pykickstart.options import *

class FC3_IgnoreDisk(KickstartCommand):
    removedKeywords = KickstartCommand.removedKeywords
    removedAttrs = KickstartCommand.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        KickstartCommand.__init__(self, writePriority, *args, **kwargs)
        self.op = self._getParser()

        self.ignoredisk = kwargs.get("ignoredisk", [])

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if len(self.ignoredisk) > 0:
            retval += "ignoredisk --drives=%s\n" % string.join(self.ignoredisk, ",")

        return retval

    def _getParser(self):
        def drive_cb (option, opt_str, value, parser):
            for d in value.split(','):
                parser.values.ensure_value(option.dest, []).append(d)

        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--drives", dest="ignoredisk", action="callback",
                      callback=drive_cb, nargs=1, type="string")
        return op

    def parse(self, args):
        (opts, extra) = self.op.parse_args(args=args)
        self._setToSelf(self.op, opts)
        return self

class F8_IgnoreDisk(FC3_IgnoreDisk):
    removedKeywords = FC3_IgnoreDisk.removedKeywords
    removedAttrs = FC3_IgnoreDisk.removedAttrs

    def __init__(self, writePriority=0, *args, **kwargs):
        FC3_IgnoreDisk.__init__(self, writePriority, *args, **kwargs)

        self.onlyuse = kwargs.get("onlyuse", [])

    def __str__(self):
        retval = KickstartCommand.__str__(self)

        if len(self.ignoredisk) > 0:
            retval += "ignoredisk --drives=%s\n" % string.join(self.ignoredisk, ",")
        elif len(self.onlyuse) > 0:
            retval += "ignoredisk --only-use=%s\n" % string.join(self.onlyuse, ",")

        return retval

    def _getParser(self):
        def drive_cb (option, opt_str, value, parser):
            for d in value.split(','):
                parser.values.ensure_value(option.dest, []).append(d)

        op = FC3_IgnoreDisk._getParser(self)
        op.add_option("--only-use", dest="onlyuse", action="callback",
                      callback=drive_cb, nargs=1, type="string")
        return op