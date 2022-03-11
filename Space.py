#made by Digiwind (works as of 03/10/22)
#from https://youtu.be/6aenC5mHqLA
#uses Pycord

import discord, aiohttp, json
from datetime import datetime
from discord.ext import commands

bot = discord.Bot()

servers = []

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}.")
    
@bot.slash_command(guild_ids = servers, name = "space", description = "Gets random space images")
@commands.cooldown(1, 5, commands.BucketType.user)
async def space(ctx):
    await ctx.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(url = r"https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&count=1") as response:
            raw = await response.text()
            raw = raw.replace(']', '').replace('[', '')
            space = json.loads(raw)
            title = space["title"]
            try: 
                url = space["hdurl"]
            except:
                url = space["url"]
            explanation = space["explanation"]
            date = space["date"]
            embed = discord.Embed(title = title, description = explanation, timestamp = datetime.now(), color = discord.Colour.blurple())
            embed.set_image(url = url)
            embed.set_footer(text = f"From {date}")
    await ctx.respond(embed = embed)
    
@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(error)
    else:
        raise error

bot.run('token')
