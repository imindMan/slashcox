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

### CONFIG DEFINITION ###
class Config:
    token: str = os.getenv("DISCOX_TOKEN")  # bot token
    report_channel_id: int = int(
        os.getenv("DISCOX_REPORT_ID", 1064539181193375784)
    )  # mod role id
    mod_role_id: List[int] = [
        int(x) for x in os.getenv("DISCOX_MOD_ROLE_ID", "0").split(",")
    ]  # mod role id
    temp_channel: int = int(os.getenv("DISCOX_TEMP_CHANNEL", "0"))  # temp channel id
    channel_id: str = os.getenv(
        "DISCOX_CHANNEL_ID", "UCCFVFyadjMuaR5O89yRToew"
    )  # channel id
    role_channel: int = int(os.getenv("DISCOX_ROLE_CHANNEL", "0"))  # role channel
    youtube_announcement_id: int = int(
        os.getenv("DISCOX_YOUTUBE_ANNOUNCEMENT_ID", 1056990617357521009)
    )  # youtube announcement id
    mysql_host: str = os.getenv("DISCOX_MYSQL_HOST", "localhost")
    mysql_port: int = int(os.getenv("DISCOX_MYSQL_PORT", 3306))
    mysql_user: str = os.getenv("DISCOX_MYSQL_USER", "root")
    mysql_password: str = os.getenv("DISCOX_MYSQL_PASSWORD", "")  # recommendaton :tf:
    mysql_database: str = os.getenv(
        "DISCOX_MYSQL_DATABASE", "discox"
    )  
    starboard_channel: int = int(
        os.getenv("DISCOX_STARBOARD_CHANNEL", "0")
    )  # starboard channel
    server_id: int = int(os.getenv("DISCOX_SERVER_ID", "1032277950416035930")) # imindworld server id

