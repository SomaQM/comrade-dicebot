import os

import dotenv

from dicebot.bot import bot
from dicebot.db import SQLiteDB
from dicebot.logsetup import setup_logging
from dicebot.stat_tracker import stat_tracker
from dicebot.varenv import var_env_provider

config = dotenv.dotenv_values(os.environ.get("COMRADE_DICEBOT_CONFIG_FILE", "/etc/data/env"))

setup_logging()

token = config["FLUXER_TOKEN"]
db = SQLiteDB(config["SQLITE_PATH"])
var_env_provider.set_db(db)
stat_tracker.set_db(db)

bot.run(token)
db.close()
