from .config import Embed


class Logger:
    @staticmethod
    def newline():
        print("[#]")

    @staticmethod
    def log(*args):
        print("[#]", *args)

    @staticmethod
    def error(*args):
        print("[!]", *args)

    @staticmethod
    async def send_error(err: str, interaction) -> None:
        embed = Embed(
            title="Oopsie Woopsie!",
            description=f"Looks like an error occured, please contact a system administrator if you believe this to be a mistake.\n```{err}```",
        )
        embed.set_color("red")
        await interaction.response.send_message(embed=embed)
