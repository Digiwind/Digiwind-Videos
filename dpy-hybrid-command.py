#from: https://youtu.be/CWoXbL3oZFc
#uses discord.py 2.0

import discord
from discord.ext import commands
from discord import app_commands

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix = "?", intents = intents)

    async def setup_hook(self):
        await self.tree.sync(guild = discord.Object(id = guild_id))
        print(f"Synced slash commands for {self.user}.")
    
    async def on_command_error(self, ctx, error):
        await ctx.reply(error, ephemeral = True)

bot = Bot()

@bot.hybrid_command(name = "test", with_app_command = True, description = "Testing")
@app_commands.guilds(discord.Object(id = guild_id))
@commands.has_permissions(administrator = True)
async def test(ctx: commands.Context):
    await ctx.defer(ephemeral = True)
    await ctx.reply("hi!")

bot.run('TOKEN')
