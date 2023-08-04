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

from discord import Colour
from discord import Embed as DiscordEmbed

DATABASE = "slashcox"

# for sql stuff
CREATE_STATEMENTS = [
    f"""
        CREATE TABLE IF NOT EXISTS {DATABASE}.fetch (
            user VARCHAR(100) NOT NULL,
            image VARCHAR(10000),
            distro VARCHAR(100),
            kernel VARCHAR(100),
            terminal VARCHAR(100), 
            editor VARCHAR(100),
            shell VARCHAR(100),
            de_wm VARCHAR(100),
            bar VARCHAR(100),
            resolution VARCHAR(100),
            display_protocol VARCHAR(100),
            gtk_theme VARCHAR(100),
            gtk_icon_theme VARCHAR(100),
            cpu VARCHAR(100),
            gpu VARCHAR(100),
            description VARCHAR(100),
            dotfiles VARCHAR(100),
            git VARCHAR(100),
            memory VARCHAR(100) 
        );
    """,
    f"""
    CREATE TABLE IF NOT EXISTS {DATABASE}.polls (
        channel_id BIGINT NOT NULL,
        message_id BIGINT NOT NULL PRIMARY KEY,
        type ENUM('single', 'multiple')
    );
    """,
    f"""
        CREATE TABLE IF NOT EXISTS {DATABASE}.levels (
            user_id VARCHAR(100) PRIMARY KEY,
            level INTEGER,
            exp INTEGER,
            font_color VARCHAR(25),
            bg VARCHAR(2048) DEFAULT NULL
        );
    """,
    f"""
        CREATE TABLE IF NOT EXISTS {DATABASE}.latest_video (
	       video_id VARCHAR(50) PRIMARY KEY
        );
    """,
    f"""
        CREATE TABLE IF NOT EXISTS {DATABASE}.request (
            Number_id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
            Member_id VARCHAR(100) NOT NULL,
            Title VARCHAR(255) NOT NULL,
            Description VARCHAR(2048) NOT NULL,
            Upvote INTEGER NOT NULL,
            Downvote INTEGER NOT NULL,
            Pending_close INTEGER NOT NULL
        );
    """,
    f"""
        CREATE TABLE IF NOT EXISTS {DATABASE}.reminders (
            id INTEGER AUTO_INCREMENT PRIMARY KEY,
            User VARCHAR(100),
            Timestamp INTEGER,
            Reminder VARCHAR(2048),
            Channel VARCHAR(100),
            Message VARCHAR(100)
        );
    """,
    f"""
        CREATE TABLE IF NOT EXISTS {DATABASE}.membercount (
            membercount INT PRIMARY KEY
        );
    """,
    f"""
    	CREATE TABLE IF NOT EXISTS {DATABASE}.starboard (
	       message_id VARCHAR(100) PRIMARY KEY,
	       board_message_id VARCHAR(100)
	   );
    """,
    f"""
        CREATE TABLE IF NOT EXISTS {DATABASE}.tags (
            Name VARCHAR(100) UNIQUE PRIMARY KEY,
            Content VARCHAR(2048)
        );
    """,
]


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

    minecraft_url: str = os.getenv("MINECRAFT_URL", "minecraft.virbos.xyz")
    minecraft_port: int = os.getenv("MINECRAFT_PORT", 25565)



## EMBED STUFF ##


class Embed(DiscordEmbed):
    """Custom implementation of a discord embed object."""

    def __init__(self, *args, **kwargs) -> None:
        DiscordEmbed.__init__(self, *args, **kwargs)

        self.colors = {
            "green": Colour(int("38842c", 16)),
            "red": Colour(int("bf3036", 16)),
            "blue": Colour(int("303f9c", 16)),
            "yellow": Colour(int("b0ba2a", 16)),
            "magenta": Colour(int("a829b0", 16)),
            "brown": Colour(int("2b1313", 16)),
            "purple": Colour(int("5300b0", 16)),
            "pink": Colour(int("ff00fc", 16)),
            "black": Colour(int("000000", 16)),
            "white": Colour(int("ffffff", 16)),
            "cyan": Colour(int("00ffff", 16)),
            "grey": Colour(int("696969", 16)),  # yeah the funny number is grey
            "lightgreen": Colour(int("89f292", 16)),
            "lightred": Colour(int("ff7171", 16)),
            "lightblue": Colour(int("807bff", 16)),
            "lightyellow": Colour(int("f7ff80", 16)),
            "lightmagenta": Colour(int("ff8dfc", 16)),
            "lightbrown": Colour(int("956767", 16)),
            "lightpurple": Colour(int("bf67ff", 16)),
            "lightpink": Colour(int("ff88dc", 16)),
            "lightcyan": Colour(int("bcfbff", 16)),
        }
        self.set_footer(
            text="Slashcox - discox alternative",
            icon_url="https://raw.githubusercontent.com/imindMan/slashcox/main/assets/logo_for_embed.png",
        )
        self.timestamp = datetime.datetime.now()

        self.set_color("green")

    def set_color(self, color: str) -> None:
        """Set a color from the default colorlist."""
        self.color = self.colors[color]
