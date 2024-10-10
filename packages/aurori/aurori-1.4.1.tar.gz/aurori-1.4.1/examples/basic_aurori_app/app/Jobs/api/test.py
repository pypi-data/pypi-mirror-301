from fastapi import APIRouter

from aurori.api import UserDep
from aurori.runners import trigger_runner

from app.Jobs.runners.testJob import TestJob
api_router = APIRouter()

# index route
@api_router.post('/v1/trigger')
def job_trigger():
    return trigger_runner(TestJob, {"test": "test2"}, None)
