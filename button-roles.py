#discord.py v2.0
#from https://youtu.be/-oY0k0jU1IE

import discord
from discord import app_commands

class button_view(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    
    @discord.ui.button(label = "verify", style = discord.ButtonStyle.green, custom_id = "role_button")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        if type(client.role) is not discord.Role: client.role = interaction.guild.get_role(role_id)
        if client.role not in interaction.user.roles:
            await interaction.user.add_roles(client.role)
            await interaction.response.send_message(f"I have given you {client.role.mention}!", ephemeral = True)
        else: await interaction.response.send_message(f"You already have {client.role.mention}!", ephemeral = True)

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False #we use this so the bot doesn't sync commands more than once
        self.added = False
        self.role = role_id

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #check if slash commands have been synced 
            await tree.sync(guild = discord.Object(id=guild_id)) #guild specific: leave blank if global (global registration can take 1-24 hours) - sync only when you have to
            self.synced = True
        if not self.added:
            self.add_view(button_view())
            self.added = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

@tree.command(guild = discord.Object(id=guild_id), name = 'button', description='Launches a button!') #guild specific slash command
async def launch_button(interaction: discord.Interaction): 
    await interaction.response.send_message(view = button_view())

client.run('token')
