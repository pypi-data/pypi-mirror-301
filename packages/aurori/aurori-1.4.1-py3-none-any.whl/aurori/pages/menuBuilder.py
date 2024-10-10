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


class MenuBuilder(object):
    """ The MenuBuilder ...
    """
    def __init__(self, ):
        # preparation to instanciate
        self.actionsMap = {}

    def init_builder(self, app, db, userManager, feature_manager):
        self.app = app
        self.db = db
        self.feature_manager = feature_manager
        self.userManager = userManager

    def make_menu_header(self, name):
        header = {}
        header['header'] = name
        return header

    def make_menu_group(self, name):
        group = {}
        group['title'] = name
        group['entries'] = []
        group['active'] = False
        group['disabled'] = False  # whether group can be collapsed
        return group

    def make_menu_divider(self, ):
        divider = {}
        divider['divider'] = True
        return divider

    def make_menu_entry(self, title, group, name, icon, path, external=False):
        entry = {}
        entry['title'] = title
        entry['group'] = group
        entry['name'] = name
        entry['icon'] = icon
        entry['href'] = path
        entry['external'] = external
        return entry

    def check_users_permissions(self, user, requirement, feature):
        key = feature.name + '.' + requirement.name
        for g in user.permission_groups:
            for p in g.permissions:
                if key == p.name:
                    return True
        return False

    def has_permission(self, user, page, feature):
        if user is None:
            if page.requireLogin is False:
                return True
        else:
            if user.admin is True:
                return True
            if page.requireAdmin is False:
                if hasattr(page, 'requirePermission'):
                    if page.requirePermission is None:
                        return True
                    else:
                        return self.check_users_permissions(
                            user, page.requirePermission, feature)
        return False

    def build_menu(self, user):
        menu_groups = {}
        for w in self.feature_manager.features:
            for key, p in w.pages.items():
                # is pages in a group
                if p.group is not None:
                    if str(p.group) in menu_groups:
                        rankSum, pageList = menu_groups[str(p.group)]

                        if self.has_permission(user, p, w):
                            pageList.append(p)

                        pageList.sort(key=lambda x: x.rank, reverse=True)
                        menu_groups[str(p.group)] = rankSum + p.rank, pageList
                    else:
                        if self.has_permission(user, p, w):
                            menu_groups[str(p.group)] = p.rank, [p]
                        else:
                            menu_groups[str(p.group)] = p.rank, []
                else:
                    if self.has_permission(user, p, w):
                        menu_groups['_' + str(p.name)] = p.rank, [p]

        sorted_menu_groups = sorted(menu_groups.items(),
                                    key=lambda x: x[1][0],
                                    reverse=True)

        menu = []
        for key, element in enumerate(sorted_menu_groups):
            group, (rank, pagelist) = element
            if len(pagelist) > 0:
                entry = self.make_menu_group(str(group))
                for p in pagelist:
                    entry['entries'].append(
                        self.make_menu_entry(title=p.title,
                                       group=p.group,
                                       name=p.name,
                                       icon=p.icon,
                                       path=p.route))
                menu.append(entry)

        return menu


'''
EXAMPLE of menu structure
[
  {header: 'aurori'},
  {
    title: 'Home',
    group: 'apps',
    icon: 'dashboard',
    name: 'Dashboard',
    href: 'dashboard'
  },
  {divider: true},
  {header: 'Templates&Links'},
  {
    title: 'Vue Material Admin',
    group: 'links',
    icon: 'touch_app',
    external: true,
    href: 'https://github.com/tookit/vue-material-admin'
  },
  {
    title: 'Vue Material Admin Demo',
    group: 'links',
    icon: 'touch_app',
    external: true,
    href: 'http://vma.isocked.com/#/dashboard'
  },
  {
    title: 'Vuetify',
    group: 'links',
    icon: 'touch_app',
    external: true,
    href: 'https://vuetifyjs.com/en/getting-started/quick-start'
  },
];

'''
