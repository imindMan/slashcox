from bot.base import BaseCommand
from bot.config import Config, Embed

# Just a simple about project command, tells info about the project
# first contribution from me
# originally made by ahz


class cmd(BaseCommand):
    """A discord command instance."""

    name = "about"
    description = "Explains about the project."

    async def execute(self, interaction) -> None:
        embed = Embed(
            title="About me",
            description="Hi, I'm slashcox. Basically I'm a clone of my father, discox, but support slash commands. Hope you enjoy me!",
            color=0x00FF00,
        )
        embed.add_field(name="Github:", value="https://github.com/imindMan/slashcox")
        embed.add_field(name="Original project:", value="https://github.com/v1rbox/discox")
        embed.add_field(name="Virbox Channel:", value="https://www.youtube.com/@Virbox")

        await interaction.response.send_message(embed=embed)
