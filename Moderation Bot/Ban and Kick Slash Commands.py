#by Digiwind
#from https://youtu.be/Fa7Jtfv2wgI
#uses Pycord, a fork of Discord.py

import discord
from discord import Option
from discord.ext import commands
from discord.ext.commands import MissingPermissions

bot = discord.Bot() 

servers = [] #server ids

@bot.event
async def on_ready():
    print("We have logged in!")

@bot.slash_command(guild_ids = servers, name = "ban", description = "Bans a member")
@commands.has_permissions(ban_members = True, administrator = True)
async def ban(ctx, member: Option(discord.Member, description = "Who do you want to ban?"), reason: Option(str, description = "Why?", required = False)):
    if member.id == ctx.author.id: #checks to see if they're the same
        await ctx.respond("BRUH! You can't ban yourself!")
    elif member.guild_permissions.administrator:
        await ctx.respond("Stop trying to ban an admin! :rolling_eyes:")
    else:
        if reason == None:
            reason = f"None provided by {ctx.author}"
        await member.ban(reason = reason)
        await ctx.respond(f"<@{ctx.author.id}>, <@{member.id}> has been banned successfully from this server!\n\nReason: {reason}")
    
@ban.error
async def banerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You need Ban Members and Administrator permissions to do this!")
    else:
        await ctx.respond("Something went wrong...") #most likely due to missing permissions
        raise error

@bot.slash_command(guild_ids = servers, name = "kick", description = "Kicks a member")
@commands.has_permissions(kick_members = True, administrator = True)
async def kick(ctx, member: Option(discord.Member, description = "Who do you want to kick?"), reason: Option(str, description = "Why?", required = False)):
    if member.id == ctx.author.id: #checks to see if they're the same
        await ctx.respond("BRUH! You can't kick yourself!")
    elif member.guild_permissions.administrator:
        await ctx.respond("Stop trying to kick an admin! :rolling_eyes:")
    else:
        if reason == None:
            reason = f"None provided by {ctx.author}"
        await member.kick(reason = reason)
        await ctx.respond(f"<@{ctx.author.id}>, <@{member.id}> has been kicked from this server!\n\nReason: {reason}")

@kick.error
async def kickerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You need Kick Members and Administrator permissions to do this!")
    else:
        await ctx.respond("Something went wrong...") #most likely due to missing permissions 
        raise error

bot.run('token') #token: KEEP THIS SAFE, from your developer portal
