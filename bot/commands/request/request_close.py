from discord import Interaction
from discord.ui import Button, View

from bot.base import BaseCommand
from bot.config import Config, Embed


class cmd(BaseCommand):
    """
    INFO:
    This command is a support command of request, it's used to close the request after reviewing and voting
    Easily by using `v!request_close <number_id>`, which <number_id> is the number_id of the request
    This command only works if the user is an administrator. The bot will detect if you are an administrator by checking your roles. If you have one of the role in the mod_role_id list (assume that you have configured it in the .env file), then you can use this command.

    """

    name = "request_close"
    description = "Close the request. Only mod can deal with it"

    async def execute(self, interaction: Interaction, number_id: int) -> None:
        """
        HOW IT WORKS:
            After entering the command, the bot will check that if the number_id is valid. If that's the case
            then the bot will send a message: Are you sure? and some options (as reactions).
            If the user's reaction is 👍, then the bot will delete the request out of the database (close the request)
            If the user's reaction is 👎, then the bot will ignore your request.
        """

        res = await self.db.raw_exec_select(
            f"SELECT * FROM request WHERE Number_id = ?", (number_id,)
        )

        if not res:
            embed = Embed(title="Invalid record")
            embed.set_color("red")
            await interaction.response.send_message(embed=embed)
            return

        # Send the message to the user
        yes_button = Button(emoji="👍", label="Yes")

        async def yes_button_callback(interaction):
            """
            HOW IT WORKS:
                By default, the request number_id is an attribute with the AUTO_INCREMENT key.
                That's why when deleting a request, we also have to update the number_id and AUTO_INCREMENT key.
                Since we use mysql, we can just ALTER TABLE request AUTO_INCREMENT = (curr_auto_incre - 1)
                For example, assuming we have a database looks like this:
                    1. "Sample request 1" by Foo
                    2. "Sample request 2" by Bar
                    3. "Sample request 3" by Egg

                When we run this command and delete the "Sample request 2" request, the database will look like this:
                Table: request
                    1. "Sample request 1" by Foo
                    3. "Sample request 3" by Egg
                Table: sqlite_sequence
                    name: request, seq: 3

                Since we only have 2 requests left, the sqlite_sequence should be updated like this:
                    name: request, seq: 2 (this way, we can keep track of the number_id correctly in the next time)
                And then, we also need to run a loop, keep track of all the requests and update their number_id.
                So the final result should be:

                Table: request
                    1. "Sample request 1" by Foo
                    2. "Sample request 3" by Egg # the name doesn't matter
                Table: sqlite_sequence
                    name: request, seq: 2
            """
            # Get the current AUTO_INCREMENT value
            res = await self.db.raw_exec_select(
                f"SELECT `AUTO_INCREMENT` FROM  INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'discox' AND   TABLE_NAME   = 'request';"
            )

            # delete the request
            await self.db.raw_exec_commit(
                f"DELETE FROM request WHERE Number_id=?", (number_id,)
            )
            # Update the sqlite_sequence
            await self.db.raw_exec_commit(
                f"ALTER TABLE request AUTO_INCREMENT = ?",
                (res[0][0] - 1,),
            )

            # And then run a loop to update the number_id
            res = await self.db.raw_exec_select(f"SELECT * FROM request")
            for i in range(0, len(res)):
                if i + 1 == int(res[i][0]):
                    continue
                await self.db.raw_exec_commit(
                    "UPDATE request SET Number_id = ? WHERE Number_id = ?",
                    (int(i) + 1, res[i][0]),
                )
            # Send a notification to the user
            embed = Embed(title="The data has successfully been deleted!")
            await interaction.response.send_message(embed=embed)

        yes_button.callback = yes_button_callback

        no_button = Button(emoji="👎", label="No")

        async def no_button_callback(interaction):
            embed = Embed(title="The request has successfully been ignored!")
            await interaction.response.send_message(embed=embed)

        no_button.callback = no_button_callback

        view = View()
        view.add_item(yes_button)
        view.add_item(no_button)

        embed = Embed(
            title="Are you sure?",
            description="React 👍 if you wish to or 👎 if you don't want to. \nEstimate time: 1min",
        )
        embed.set_color("red")
        await interaction.response.send_message(embed=embed, view=view)

    def check_permissions(self, interaction):
        return any([i.id in Config().mod_role_id for i in interaction.user.roles])
