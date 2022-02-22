#uses Pycord
#from https://youtu.be/KS1_3km5vC0

import discord
from datetime import datetime
from discord import Option
from discord.ext import commands
from discord.ext.commands import MissingPermissions

bot = discord.Bot()

servers = []

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}.")
    
@bot.slash_command(guild_ids = servers, name = "bans", description = "Get a list of members who are banned from this server!")
@commands.has_permissions(ban_members = True)
async def bans(ctx):
    await ctx.defer()
    bans = await ctx.guild.bans()
    embed = discord.Embed(title = f"List of Bans in {ctx.guild}", timestamp = datetime.now(), color = discord.Colour.red())
    for entry in bans:
        if len(embed.fields) >= 25:
            break
        if len(embed) > 5900:
            embed.add_field(name = "Too many bans to list")
        else:
            embed.add_field(name = f"Ban", value = f"Username: {entry.user.name}#{entry.user.discriminator}\nReason: {entry.reason}\nUser ID: {entry.user.id}\nIs Bot: {entry.user.bot}", inline = False)
    await ctx.respond(embed = embed)

@bot.slash_command(guild_ids = servers, name = "unban", description = "Unbans a member")
@commands.has_permissions(ban_members = True)
async def unban(ctx, id: Option(discord.Member, description = "The User ID of the person you want to unban.", required = True)):
    await ctx.defer()
    member = await bot.get_or_fetch_user(id)
    await ctx.guild.unban(member)
    await ctx.respond(f"I have unbanned {member.mention}.")

@unban.error
async def unbanerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You need ban members permissions to do this!")
    else: 
        await ctx.respond(f"Something went wrong, I couldn't unban this member or this member isn't banned.")
        raise error

bot.run('token')
