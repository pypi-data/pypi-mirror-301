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

import os
import pathlib
import pkgutil
import inspect
from aurori.features.feature import Feature
from aurori.logs import log_manager
import sys
import traceback
import sqlalchemy as sa


class FeatureManager(object):
    """The FeaturesManager holds all available features and load them while creation."""

    def __init__(self, feature_source_path):
        self.feature_source_path = feature_source_path
        self.app = None
        self.db = None
        self.config = None
        self.features = None
        self.user_class = None
        self.api_prefix = None

    def init_app(self, app, config, minimal=False, api_prefix="api/v1"):
        self.app = app
        self.config = config
        self.features = []
        self.seen_paths = []
        self.api_prefix = api_prefix
        log_manager.info("")
        log_manager.info(f"Discover features in path : {self.feature_source_path}")
        self.discover_features(self.feature_source_path)
        self.discover_database()
        if minimal is False:
            self.discover_permissions()
            self.create_permissions()
            self.discover_runners()
            self.discover_pages()
            self.discover_apis()

        log_manager.info("")
        log_manager.info("Features and their components initialized")

    def get_feature(self, name):
        for w in self.features:
            if w.name is name:
                return w
        return None

    def reload_features(self):
        """Reset the list of all plugins and initiate the walk over the main
        provided plugin package to load all available plugins
        """
        self.features = []
        self.seen_paths = []
        log_manager.info("")
        log_manager.info(f"Discover features in path : {self.feature_source_path}")
        self.discover_features(self.feature_source_path)

    def discover_permissions(self):

        log_manager.info("")
        log_manager.info("Discover permissions:")

        for f in self.features:
            log_manager.info(f'  For feature: "{f.name}"')

            # try to register permissions
            try:
                f.discover_permissions(self.feature_source_path)
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                log_manager.error(
                    f'  Feature "{f.uri}" unable to discover permissions  ({str(type(e).__name__)}:{e})'
                )

    def discover_pages(self):
        log_manager.info("")
        log_manager.info("Discover pages:")

        for w in self.features:
            log_manager.info(f'  For feature: "{w.name}"')
            feature_config_section_name = pathlib.Path(w.path).resolve().name.upper()
            # try to register permissions

            try:
                w.discover_pages(self.feature_source_path)
            except Exception as exception:
                traceback.print_exc(file=sys.stdout)
                log_manager.error(
                    f'  Feature "{w.name}" unable to discover pages  ({str(type(exception).__name__)}:{exception})'
                )

    def discover_runners(self):
        log_manager.info("")
        log_manager.info("Discover runners:")

        for w in self.features:
            log_manager.info(f'  For feature: "{w.name}"')
            feature_config_section_name = pathlib.Path(w.path).resolve().name.upper()

            if (
                feature_config_section_name in self.config
                and "disable_runners" in self.config[feature_config_section_name]
                and self.config[feature_config_section_name]["disable_runners"]
            ):
                log_manager.info(f'    Runners for "{w.name}" are disabled by config')
            else:
                # try to register jobs
                try:
                    w.discover_runners(self.feature_source_path)
                except Exception as e:
                    traceback.print_exc(file=sys.stdout)
                    log_manager.error(
                        f'    Feature "{w.name}" unable to discover jobs  ({str(type(e).__name__)}:{e})'
                    )

    def discover_apis(self):
        log_manager.info("")
        log_manager.info("Discover api modules:")

        for w in self.features:
            log_manager.info(f'  For feature : "{w.name}"')
            feature_config_section_name = pathlib.Path(w.path).resolve().name.upper()

            try:
                w.discover_apis(self.feature_source_path)
            except Exception as exception:
                traceback.print_exc(file=sys.stdout)
                log_manager.error(
                    f'  Feature "{w.name}" unable to apis pages  ({str(type(exception).__name__)}:{exception})'
                )

    def discover_database(self):
        log_manager.info("")
        log_manager.info("Discover database modules:")

        source = self.feature_source_path
        try:
            imported_source = __import__(source, fromlist=["blah"])
        except Exception as exception:
            log_manager.error(f"  Unable to locate features {str(exception)}")
            return
        all_current_paths = []

        # all_current_paths.append(imported_source.__path__._path)

        if isinstance(imported_source.__path__, str):
            all_current_paths.append(imported_source.__path__)
        else:
            all_current_paths.extend([x for x in imported_source.__path__])

        from aurori.users.userbase import UserBase

        # remove duplicates
        all_current_paths = list(set(all_current_paths))

        for pkg_path in all_current_paths:
            # Walk through all sub directories
            child_pkgs = [
                p
                for p in os.listdir(pkg_path)
                if os.path.isdir(os.path.join(pkg_path, p))
            ]

            for child_pkg in child_pkgs:
                log_manager.info(f'  For feature : "{child_pkg}"')
                try:
                    # fixme: this was assigned to a later unused variable?
                    # imported_package = __import__(source + '.' + child_pkg + '.database', fromlist=['blah'])
                    imported_package = __import__(
                        source + "." + child_pkg + ".database", fromlist=["blah"]
                    )
                    for _, modelpackagename, ispkg in pkgutil.iter_modules(
                        imported_package.__path__, imported_package.__name__ + "."
                    ):

                        feature_module = __import__(modelpackagename, fromlist=["blah"])
                        log_manager.info(
                            f'    Discovered database module "{modelpackagename}"'
                        )

                        clsmembers = inspect.getmembers(feature_module, inspect.isclass)

                        for _, c in clsmembers:
                            if issubclass(c, UserBase) & (c is not UserBase):
                                if self.user_class is not None and self.user_class != c:
                                    raise Exception(
                                        "Multiple User models found. For a aurori app only one is allowed."
                                    )
                                self.user_class = c
                except ModuleNotFoundError:
                    modelmodule = source + "." + child_pkg + ".database"
                    log_manager.info(f"    No database models found")

        if self.user_class is None:
            log_manager.warning(
                f"No User model derived from aurori.users.basemodels.UserBase found."
            )
            log_manager.warning(f"A aurori app needs a user model to work properly.")
            log_manager.warning(
                f'Please define a derived model named "User" in your features, if needed.'
            )
            log_manager.warning(
                f"The default model will be used, please reference: aurori.users.defaultmodels.User "
            )
            from aurori.users.defaultuser import User

    def discover_features(self, source):
        """Recursively walk the supplied package to retrieve all plugins (features)"""

        try:
            imported_source = __import__(source, fromlist=["blah"])
        except Exception as e:
            log_manager.error(f"Unable to locate features {str(e)}")
            return

        all_current_paths = []

        # all_current_paths.append(imported_source.__path__._path)

        if isinstance(imported_source.__path__, str):
            all_current_paths.append(imported_source.__path__)
        else:
            all_current_paths.extend([x for x in imported_source.__path__])

        # remove duplicates
        all_current_paths = list(set(all_current_paths))

        for pkg_path in all_current_paths:
            # Walk through all sub directories
            child_pkgs = [
                p
                for p in os.listdir(pkg_path)
                if os.path.isdir(os.path.join(pkg_path, p))
            ]

            # Every sub directory contains one feature
            for child_pkg in child_pkgs:
                imported_package = __import__(
                    source + "." + child_pkg, fromlist=["blah"]
                )

                clsmembers = inspect.getmembers(imported_package)

                uri = ""
                if hasattr(imported_package, "uri"):
                    uri = imported_package.uri
                else:
                    uri = str(child_pkg).lower()

                logger = None
                if hasattr(imported_package, "logger"):
                    logger = imported_package.logger

                featureInstance = Feature(self.app, self.db, str(child_pkg), uri)

                if hasattr(imported_package, "description"):
                    featureInstance.description = imported_package.description

                if hasattr(imported_package, "disabled"):
                    featureInstance.disabled = imported_package.disabled

                featureInstance.path = os.path.dirname(imported_package.__file__)
                feature_config_section_name = (
                    pathlib.Path(imported_package.__file__)
                    .parent.resolve()
                    .name.upper()
                )
                log_manager.info(
                    f'  Discovered feature "{featureInstance.name}" as "{featureInstance.uri}" from "{source + "." + child_pkg}"'
                )

                if (
                    (feature_config_section_name in self.config)
                    and ("disabled" in self.config[feature_config_section_name])
                    and (self.config[feature_config_section_name]["disabled"])
                ):
                    log_manager.info(
                        "  The feature is disabled by config and wont show up"
                    )
                else:
                    if featureInstance.disabled is True:
                        log_manager.info(
                            "  The feature is disabled by module definition and wont show up"
                        )
                    else:
                        log_manager.register_logger(logger, featureInstance.name)
                        self.features.append(featureInstance)

    def create_permissions(self):
        """Run createPermissions for all features and store permissions"""
        all_permissions = {}
        for ws in self.features:

            feature_permissions = ws.permissions
            if feature_permissions is not None:
                all_permissions = {**all_permissions, **feature_permissions}

        # delete orphaned permissions for security reasons
        from .database import Permission
        from aurori import db

        engine = db.engine
        table_exists = sa.inspect(engine).has_table(Permission.__tablename__)
        if table_exists:
            with db.get_session() as db_session:
                db_permissions = db_session.query(Permission).all()
                for permission in db_permissions:
                    if permission.name not in all_permissions:
                        log_manager.warning(f"  Delete orphaned {permission}")
                        db_session.delete(permission)
                        db_session.commit()
