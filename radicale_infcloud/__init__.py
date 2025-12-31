# RadicaleWeb web interface for Radicale.
# Copyright © 2017-2018, 2020, 2022 Unrud <unrud@outlook.com>
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

from http import client
from radicale import httputils
from radicale.web import internal
from importlib.metadata import version

PLUGIN_CONFIG_SCHEMA = {"web": {
    "infcloud_config": {
        "value": "",
        "type": str}}}


class Web(internal.Web):

    def __init__(self, configuration):
        super().__init__(configuration.copy(PLUGIN_CONFIG_SCHEMA))

    def get(self, environ, base_prefix, path, user):
        extra = ()
        if path == "/.web/infcloud/" or path.startswith("/.web/infcloud"):
            response = httputils.serve_resource(
                "radicale_infcloud", "web", base_prefix, path,
                "/.web/infcloud")
        else:
            response = super().get(environ, base_prefix, path, user)

        status = response[0]
        headers = response[1]
        answer = response[2]
        extra = response[3:]

        if status == client.OK and path in ("/.web/", "/.web/index.html"):
            if version("radicale") >= "3.2.0":
                answer = answer.replace(b"""title="Refresh">Refresh</a>""",
                                        b"""title="Refresh">Refresh</a>
      <a class="blue" data-name="infcloud" title="InfCloud" style="float: left;left: 40px;" href="infcloud">InfCloud</a>""")
            else:
                answer = answer.replace(b"""\
<nav>
    <ul>""", b"""\
<nav>
    <ul>
        <li><a href="infcloud">InfCloud</a></li>""")
        
        if status == client.OK and path == "/.web/infcloud/config.js":
            answer += self.configuration.get("web", "infcloud_config").encode()
            
        if version("radicale").startswith("3") and not extra:
            extra = (None,)

        return (status, headers, answer) + extra
