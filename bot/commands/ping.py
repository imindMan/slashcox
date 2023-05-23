from bot.base import BaseCommand 


class cmd(BaseCommand):
    name = "ping"
    description = "Check the current latency of the bot."

    async def execute(self, interaction):
        await interaction.response.send_message("Im alivetesererete!!")
