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

from datetime import datetime
from aurori.logs import log_manager
from aurori.config import config_manager
from aurori.database import db
import logging
import traceback


class Runner(object):
    """Base class that each job inherit from.
       The class define methods that all jobs have to implement
    """
    description = "Not available"  # description of the job
    disable = False  # disable the job
    local = True  # only runnable by the same feature
    strict = True  # strict argument parsing
    requireAdmin = False  # admin is required to view the page
    requirePermission = None  # a permission is required in the meaning of one of the following

    # Repetetive members
    cron = False
    day = None
    week = None
    day_of_week = None
    hour = None
    minute = None
    second = None

    def __init__(self, name=None, uri=None):
        if name is None:
            self.name = type(self).__name__
        else:
            self.name = name
        self.job_key = self.name
        self.feature = ""
        self.parameters = None
        self.define_arguments()

    def start_runner(self, **kwargs):
        from aurori.runners.database import RunnerExecute

        self.debug_info = {}
        triggered = datetime.now()
        current_time = triggered.strftime("%H:%M:%S")

        log_manager.info("Run " + self.name + " " + current_time)

        je = None

        with db.get_session() as db_session:
            if 'job_execution_id' in kwargs:
                je = db_session.query(RunnerExecute).filter_by(
                    id=kwargs['job_execution_id']).first()

            if je is None:
                je = RunnerExecute()
                je.feature = self.feature
                je.triggered_by = "Cron"
                je.triggered_on = triggered
                je.name = self.job_key
                db_session.add(je)
                db_session.commit()

            try:
                self.run(**kwargs)
                je.state = "SUCCEED"
                # je.results = {"hjsadhj": "jklsajdklas"}
            except Exception as e:
                je.state = "FAILED"
                je.results = {
                    "error": str(type(e)),
                    "traceback": str(traceback.format_exc()),
                    "debug": self.debug_info
                }
                print(je.results)

            after = datetime.now()
            delta = after - triggered
            je.lifetime = delta.total_seconds()
            db_session.commit()


    def add_argument(self,
                    name,
                    typestring,
                    label="",
                    description="",
                    optional=False,
                    group=None):
        p = {
            'name': name,
            'type': typestring,
            'label': label,
            'optional': optional,
            'group': group
        }
        if self.parameters is None:
            self.parameters = [p]
        else:
            self.parameters.append(p)

    def add_dict_argument(self,
                        name,
                        label="",
                        description="",
                        optional=False,
                        group=None):
        log_manager.info("Add dict type argument to job {}".format(self.name))
        self.add_argument(name, 'dict', label, description, optional, group)

    def add_list_argument(self,
                        name,
                        label="",
                        description="",
                        optional=False,
                        group=None):
        log_manager.info("Add list type argument to job {}".format(self.name))
        self.add_argument(name, 'list', label, description, optional, group)

    def add_string_argument(self,
                          name,
                          label="",
                          description="",
                          optional=False,
                          group=None):
        log_manager.info("Add string type argument to job {}: {} - {}".format(
            self.name, name, label))
        self.add_argument(name, 'string', label, description, optional, group)

    def add_double_argument(self,
                          name,
                          label="",
                          description="",
                          optional=False,
                          group=None):
        log_manager.info("Add double type argument to job {}".format(self.name))
        self.add_argument(name, 'double', label, description, optional, group)

    def add_integer_argument(self,
                           name,
                           label="",
                           description="",
                           optional=False,
                           group=None):
        log_manager.info("Add integer type argument for job {}".format(
            self.name))
        self.add_argument(name, 'integer', label, description, optional, group)

    def add_datetime_argument(self,
                            name,
                            label="",
                            description="",
                            optional=False,
                            group=None):
        log_manager.info("Add datetime type argument for job {}".format(
            self.name))
        self.add_argument(name, 'datetime', label, description, optional, group)

    def add_time_argument(self,
                        name,
                        label="",
                        description="",
                        optional=False,
                        group=None):
        log_manager.info("Add time type argument for job {}".format(self.name))
        self.add_argument(name, 'time', label, description, optional, group)

    def add_date_argument(self,
                        name,
                        label="",
                        description="",
                        optional=False,
                        group=None):
        log_manager.info("Add date tyme argument for job {}".format(self.name))
        self.add_argument(name, 'date', label, description, optional, group)

    def add_boolean_argument(self,
                           name,
                           label="",
                           description="",
                           optional=False,
                           group=None):
        log_manager.info("Add boolean type argument for job {}".format(
            self.name))
        self.add_argument(name, 'boolean', label, description, optional, group)

    def define_arguments(self):
        pass

    def run(self, *args, **kwargs):
        raise NotImplementedError
