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
from fastapi import APIRouter
from aurori.runners.runner import Runner

from aurori.runners.runnerManager import RunnerManager
from aurori.logs import log_manager
from inspect import isclass

runner_manager = RunnerManager()

jobs_router = APIRouter()

def trigger_runner(job_class, args, user):
    if user is None:
        log_manager.info("Internal job {} triggered".format(job_class))
    else:
        log_manager.info("User {} triggered job {}".format(user.email, job_class))

    job_id = runner_manager.run_job(user,
                                job_class,
                                args,
                                datetime.now(),
                                log_trigger=True)
    return job_id


def add_dated_job(user,
                  job,
                  args,
                  date=None,
                  feature=None,
                  max_instances=10):
    if date is None:
        date = datetime.now()
    key = ""
    if feature is not None:
        if type(feature) == str:
            key += feature + '/'
        elif isclass(feature):
            log_manager.error(
                "Class parameters are not allowed for add_dated_job")
            return
        else:
            key += feature.name + '/'

    if type(job) == str:
        key += job
    elif isclass(feature):
        log_manager.error("Class parameters are not allowed for add_dated_job")
        return
    elif issubclass(type(job), Runner):
        key += job.name
    else:
        log_manager.error("Unknown type of job in add_dated_job")
        return
    runner_manager.run_job(user, key, args, date, max_instances)


def print_job_list():
    print("jobs.print_job_list not implemented yet")


from aurori.runners import routes
