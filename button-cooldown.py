#uses discord.py 2.0
#from: link coming soon...

import discord
from discord import app_commands
from discord.ext import commands

class button_view(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)
    
    @discord.ui.button(label = "hello", style = discord.ButtonStyle.blurple, custom_id = "button_with_cooldown")
    async def hello_button(self, interaction, button):
        interaction.message.author = interaction.user
        bucket = self.cooldown.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
            return await interaction.response.send_message(f"Slow down! Try again in {round(retry, 1)} seconds.", ephemeral = True)
        await interaction.response.send_message("hi", ephemeral = True)

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False #we use this so the bot doesn't sync commands more than once
        self.added = False #was written, incorrectly, as True

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #check if slash commands have been synced 
            await tree.sync(guild = discord.Object(id=guild_id)) #guild specific: leave blank if global (global registration can take 1-24 hours)
            self.synced = True
        if not self.added:
            self.add_view(button_view())
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

@tree.command(guild = discord.Object(id=guild_id), name = 'button', description='Launches a button!') #guild specific slash command
async def launch_button(interaction: discord.Interaction):
    await interaction.response.send_message(view = button_view())

client.run('TOKEN')
