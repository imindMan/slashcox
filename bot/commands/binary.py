# Replies with the given message in binary.

from bot.base import BaseCommand
from bot.config import Embed


class cmd(BaseCommand):
    # Our 'binary' command.
    name = "binary"
    description = "Rewrites the given message in binary."

    def decode_binary(self, string) -> str:
        # Take each byte, (8 bits, that's why there are multiple eights in this
        # code) convert them to a character, and join them together.
        # This thing is absolutely unreadable, but here you go:
        try:
            return "".join(
                chr(int(string[i * 8 : i * 8 + 8], 2)) for i in range(len(string) // 8)
            )
        except Exception:
            raise RuntimeError(
                "An error occured decoding the binary sequence - might not be a valid one."
            )

    async def execute(self, interaction, option: str, message: str) -> None:
        # Get the option - either "encode" or "decode".
        if option not in ("encode", "decode"):
            raise KeyError(
                f"Invalid option: {option} - valid options are 'encode' and 'decode'."
            )

        # If encode is True, we will encode the given message. Else, we decode a binary sequence.
        encode = option == "encode"

        translated = None

        if encode:
            # Take every char from full_message, translate it into binary,
            # and join them.
            translated = " ".join(format(ord(i), "b").zfill(8) for i in message)
        else:
            # We have to decode full_message.
            # Replacing spaces with empty strings, because it will fail if the
            # user inputs something like 00110100 10101101 if we don't do that.
            translated = str(self.decode_binary(message.replace(" ", "")))

        # Now make our embed
        embed = Embed(
            title="Binary",
            description=f"""
            The binary sequence for '{message}' is:
            ```{translated}```
            """,
        )

        embed.set_color("green")

        await interaction.response.send_message(embed=embed)
