### CONFIG (embed in the future) ###
#
# Mainly migrating from discox. Config class supports setting inside the .env file (for security & privacy purpose)
#
####################################

### IMPORT SOMETHING ###
from dotenv import load_dotenv

load_dotenv()

import datetime
import os
from typing import List


# os.getenv returns an empty string if the value is empty so it doesn't use the second argument
def getenv(name: str, other: str = None) -> any:
    """Gets an environment variable
    [Args]:
        name (str): The name of the env variable
        other (str): Will return if name is empty or None
    """
    env = os.getenv(name)
    return env if env or other is None else other


### CONFIG DEFINITION ###
class Config:
    token: str = getenv("SLASHCOX_TOKEN")  # bot token
    report_channel_id: int = int(
        getenv("SLASHCOX_REPORT_ID", "1064539181193375784")
    )  # mod role id
    mod_role_id: List[int] = [
        int(x) for x in getenv("SLASHCOX_MOD_ROLE_ID", "0").split(",")
    ]  # mod role id
    temp_channel: int = int(getenv("SLASHCOX_TEMP_CHANNEL", "0"))  # temp channel id
    channel_id: str = getenv(
        "SLASHCOX_CHANNEL_ID", "UCCFVFyadjMuaR5O89yRToew"
    )  # channel id
    role_channel: int = int(getenv("SLASHCOX_ROLE_CHANNEL", "0"))  # role channel
    youtube_announcement_id: int = int(
        getenv("SLASHCOX_YOUTUBE_ANNOUNCEMENT_ID", "1056990617357521009")
    )  # youtube announcement id
    mysql_host: str = getenv("SLASHCOX_MYSQL_HOST", "localhost")
    mysql_port: int = int(getenv("SLASHCOX_MYSQL_PORT", "3306"))
    mysql_user: str = getenv("SLASHCOX_MYSQL_USER", "root")
    mysql_password: str = getenv("SLASHCOX_MYSQL_PASSWORD", "")  # recommendaton :tf:
    mysql_database: str = getenv("SLASHCOX_MYSQL_DATABASE", "discox")
    starboard_channel: int = int(
        getenv("SLASHCOX_STARBOARD_CHANNEL", "0")
    )  # starboard channel
    server_id: int = int(
        getenv("SLASHCOX_SERVER_ID", "1032277950416035930")
    )  # imindworld server id
