"""
The aurori project

Copyright (C) 2022  Marcus Drobisch,

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__authors__ = ["Marcus Drobisch"]
__contact__ = "aurori@fabba.space"
__credits__ = []
__license__ = "AGPLv3+"
"""Base class to create and handle pages in the features
"""


class Page(object):
    title = 'Missing title'  # Shown label of the page in the menu
    group = None  # groupname multiple pages
    icon = 'warning'  # icon (in typeset of material design icons)
    route = '/error'  # routing
    builder = 'frontend'  # page get build by the client (frontend)
    rank = 0.0  # ranks (double) the page higher values are at the top of the menu
    # groups will be ranked by the sum of the rank-values of their entries
    requireLogin = True  # login is required to view the page
    requireAdmin = True  # admin is required to view the page
    requirePermission = None  # a permission is required in the meaning of one of the following

    disable = False

    def __init__(self):
        if not hasattr(self, 'name'):
            self.name = self.__class__.__name__
