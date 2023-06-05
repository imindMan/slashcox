import json
import random

import aiohttp

from bot.base import BaseCommand
from bot.config import Embed


class cmd(BaseCommand):
    """A discord command instance."""

    name = "gigachad"
    description = "Gigachad random image"

    async def execute(self, interaction) -> None:
        # Special thanks to the awesome work of justinlime for the collection of gigachads
        # Repo: https://github.com/justinlime/GigaChads

        # Start parsing every available images in the GigaChads repo
        gigaurl = (
            "https://raw.githubusercontent.com/justinlime/GigaChads/main/gigalist.json"
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(gigaurl) as result:
                if result.status != 200:
                    embed = Embed(title="GigaSad :(", description="Could Not Load")
                    embed.set_color("red")
                    await interaction.response.send_message(embed=embed)
                    return
                gigalist = await result.json(content_type=None)
                gigalist = gigalist["gigachads"]

        # randomly
        gigachad = random.choice(gigalist)

        # send the image
        embed = Embed(title="Best GigaChad ever:")
        embed.set_image(
            url=f"https://raw.githubusercontent.com/justinlime/GigaChads/main/gigachads/{gigachad}"
        )
        await interaction.response.send_message(embed=embed)
