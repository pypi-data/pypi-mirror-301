import uvicorn

from aurori import create_app
from aurori.config import Config
from aurori.database import db

from aurori.types.objDict import ObjDict

from seed import seed_environment

config = Config(config_path="config.ini")

app = create_app(config)

with db.get_session() as db_session:
    seed_environment(db_session)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8100)
