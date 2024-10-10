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
__license__ = "AGPLv3"

from aurori.runners.runner import Runner
from aurori.logs import log_manager
from datetime import datetime, timedelta
from aurori.database import db

class CleanupRunnerHistory(Runner):

    cron = True
    second = "5"
    disable = False
    description = "Cleanup runners history"

    def run(self, **kwargs):
        from aurori.runners.database import RunnerExecute
        now = datetime.utcnow()
        datetime_threshold = now.replace(minute=0, second=0,
                                         microsecond=0) - timedelta(days=14)
        with db.get_session() as db_session:
            job_execcute_items_older_7days = db_session.query(RunnerExecute).filter(
                RunnerExecute.triggered_on < datetime_threshold).all()
            for j in job_execcute_items_older_7days:
                db_session.delete(j)
        log_manager.info("CleanupRunnerHistory done")
