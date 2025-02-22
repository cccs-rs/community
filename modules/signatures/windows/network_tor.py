# Copyright (C) 2012 Claudio "nex" Guarnieri (@botherder)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from lib.cuckoo.common.abstracts import Signature


class Tor(Signature):
    name = "network_tor"
    description = "Installs Tor on the infected machine"
    severity = 3
    categories = ["network", "stealth"]
    authors = ["nex"]
    minimum = "1.3"
    evented = True
    ttps = ["T1188"]  # MITRE v6
    ttps += ["T1090"]  # MITRE v6,7,8
    ttps += ["T1090.003"]  # MITRE v7,8
    ttps += ["U0903"]  # Unprotect

    filter_apinames = set(["CreateServiceA", "CreateServiceW"])

    def on_call(self, call, process):
        if self.check_argument_call(call, pattern="Tor Win32 Service", ignorecase=True):
            return True

    def on_complete(self):
        indicators = (
            r".*\\tor\\cached-certs$",
            r".*\\tor\\cached-consensus$",
            r".*\\tor\\cached-descriptors$",
            r".*\\tor\\geoip$",
            r".*\\tor\\lock$",
            r".*\\tor\\state$",
            r".*\\tor\\torrc$",
        )

        for indicator in indicators:
            if self.check_file(pattern=indicator, regex=True):
                if self.pid:
                    self.mark_call()
                return True
