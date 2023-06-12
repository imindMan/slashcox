from bot.base import BaseCommand
from bot.config import Config, Embed
from discord.ui import TextInput, Modal

import discord

class RequestModal(Modal, title="Slashcox request input prompt"):
    title_of_the_request = TextInput(
            style = discord.TextStyle.short,
                            label="Title",
                            required=True,
                            placeholder="Good title"
        )
    description_of_the_request = TextInput(
                        style = discord.TextStyle.long,
                        label ="Description",
                        required=True,
                        max_length=1000,
                        placeholder="This is a sample description"
            
                )
    def init_db(self, db):
        self.db = db
    async def on_submit(self, interaction) -> None:
        
        member_id = interaction.user.__repr__()
        # MAIN EXECUTION: after getting all the information, the bot will add all of the information to the database
        split_member_id = member_id.split(" ")
        member_name = split_member_id[2].replace("'", "")[5:]
        member_discriminator = split_member_id[3].replace("'", "")[14:]
        member_id = member_name + "#" + member_discriminator

        await self.db.raw_exec_commit(
            "INSERT INTO request(Member_id, Title, Description, Upvote, Downvote, Pending_close) VALUES(?, ?, ?, ?, ?, ?)",
            (member_id, self.title_of_the_request.value, self.description_of_the_request.value, 0, 0, 0),
        )
        # Notify the user that the bot has added the request to the database.

        # Notify the administrators to review the request
        ping_roles = ""
        for i in Config.mod_role_id:
            ping_roles += "<@&" + str(i) + ">"

        embed = Embed(title=f"{interaction.user.mention}{ping_roles} A request has been added! Please consider to review it and start voting")
        await interaction.response.send_message(ping_roles, embed=embed)
    
class cmd(BaseCommand):
    """
    INFO: this is a request command. It's used for requesting the server to do something.
    When you request something to the server, maybe the administrators don't get that.The request command will ping to all the administrators to notice your request, so they can review it immediately or start voting for your request!
    Support multiple commands to deal with it, too: request_book, request_close, request_start_vote, request_end_vote and request_status.
    """

    name = "request"
    description = (
        "Add some recommendation to the server. Support multiple commands to deal with."
    )

    async def execute(self, interaction) -> None:
        """
        HOW DOES IT WORK?
        Well, when you type 'v!req request', it will automatically start an interactive chat to you. It will ask you some information about the request, and then once you fill all of them, the command will add it to the database and ping every moderators and administrators to review it.

        INFORMATION ABOUT THE REQUEST:
            - Title of the request: (the title variable)
            - Description of the request: (the description variable)
            - Your id: (the member_id variable) so we will know who made the request
        """

        modal = RequestModal()
        modal.init_db(self.db)
        await interaction.response.send_modal(modal)
        
        
