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

import logging
import sys
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from os import environ

from sqlalchemy_utils import database_exists

from aurori.config import configure_app, config_manager
from aurori.version import version
from aurori.logs import log_manager
from aurori.features import feature_manager
from aurori.users import userManager, userbase
from aurori.features.permission import Permission
from aurori.runners import runner_manager
from aurori.database import db, SQLModelBase
from aurori.utils import unicode_string_to_bytes
from aurori.pages import menu_builder

__version__ = version


def create_app(config, fastapi_config=None, minimal=False, api_prefix="", title="Aurori App", version="0.1.0"):
    config_manager.init_manager(config, fastapi_config)
    app = FastAPI(title=title, version=version)

    origins = [
        "*"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    db.init_app(config)



    from aurori import app_router
    app.include_router(app_router, tags=["core"])

    from aurori.runners import jobs_router
    app.include_router(jobs_router,prefix=api_prefix, tags=["jobs"])

    from aurori.users import user_router, core_router  # noqa: F401, F811
    app.include_router(core_router, tags=["core"])
    app.include_router(user_router, prefix=api_prefix + "/user", tags=["app.user"])

    if not minimal:
        runner_manager.init_manager(config_manager.config)
        menu_builder.init_builder(app, db, userManager, feature_manager)

    feature_manager.init_app(app, config_manager.config, minimal=minimal,api_prefix=api_prefix)
    if not minimal:
        userManager.init_manager(app, db, feature_manager, config_manager.config)


    database_is_new = not database_exists(db.url)
    if database_is_new == True:
        log_manager.warning("No database found at", db.url)
        log_manager.warning("Creating new empty database")
        SQLModelBase.metadata.create_all(bind=db.engine)

    return app


# declare app routes
app_router = APIRouter()
from aurori import routes
