from bot.base import BaseCommand
from bot.config import Config, Embed


class cmd(BaseCommand):
    """A discord command instance."""

    name = "embeds"
    description = "View all embed colors."

    async def execute(self, interaction) -> None:
        keys = list(Embed().colors.keys())
        embeds = [keys[i : i + 9] for i in range(0, len(keys), 9)]

        for lst in embeds:
            out = []
            for k in lst:
                embed = Embed(description=f"```{k:<20}```")
                embed.set_color(k)
                embed.set_footer(text="", icon_url="")
                embed.timestamp = None
                out.append(embed)

            await interaction.response.send_message(embeds=out)
