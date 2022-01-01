import discord, asyncio
from datetime import datetime
from discord.utils import find

bot = discord.Bot(activity=discord.Activity(type=discord.ActivityType.watching, name="the New Year, 2022!"), status = discord.Status.online)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

testingservers = []

@bot.slash_command(guild_ids = testingservers, name = "notify", description = "Sends a DM when it is the new year")
async def notify(ctx):
    member = ctx.author.id
    server = ctx.guild.id
    line_number = None
    file = open("newyear.txt", "r")
    for number, line in enumerate(file):
            if str(member) in line:
                line_number = number
                break
    file.close()
    if line_number == None:
        file = open("newyear.txt", "a")
        file.writelines(f"{member} {server}")
        try:
            await ctx.author.send(f"Hello <@{ctx.author.id}>!")
            await ctx.respond(f"Hi <@{member}>, I have sent you a DM!")
        except:
            await ctx.respond(f"Uh oh, <@{member}>, your DMs were closed.")
    else:
        try:
            await ctx.author.send(f"Hello <@{ctx.author.id}>!")
            await ctx.respond(f"Hi <@{member}>, I have sent you a DM!")
        except:
            await ctx.respond(f"Uh oh, <@{member}>, your DMs were closed.")

@bot.slash_command(guild_ids = testingservers, name = "pinging", description = "")
async def pinging(ctx):
    await ctx.channel.trigger_typing()
    dt = datetime.now()
    seconds = ((24 - dt.hour - 1) * 60 * 60) + ((60 - dt.minute - 1) * 60) + (60 - dt.second)
    await asyncio.sleep(1)
    with open('newyear.txt') as file:
        for line in file:
            id = int(line[0:18])
            guild = int(line[-18:])
            member = await bot.get_or_fetch_user(id)
            try:
                await member.send(f"Happy New Year <@{member.id}>! I wish you a happy 2022!")
                await member.send("https://media.giphy.com/media/Q5gYwgsTe2ixRthGO9/giphy.gif")
            except:
                general = find(lambda x: x.name == 'general', guild.text_channels)
                await general.send(f"Happy New Year <@{member.id}>! I wish you a happy 2022!")
    await ctx.send("I have wished everyone a happy new year!")

@bot.slash_command(guild_ids = testingservers, name="time-until-2022", description = "Calculates the time until 2022!")
async def until(ctx):
    await ctx.channel.trigger_typing()
    dt = datetime.now()
    hours = 23 - dt.hour
    minutes = 59 - dt.minute
    seconds = 59 - dt.second
    await ctx.respond(f"{hours} hours, {minutes} minutes, and {seconds} seconds")

@bot.slash_command(guild_ids = testingservers, name = "gifs", description = "sends a variety of new year gifs")
async def gifs(ctx):
    await ctx.channel.trigger_typing()
    await ctx.respond("https://media.giphy.com/media/ZW3LXgQSm3BoauaLRP/giphy.gif\nhttps://media.giphy.com/media/eSxLsgvwmczOEg4MBR/giphy-downsized-large.gif\nhttps://media.giphy.com/media/MOBbiDj5FeoZr2wjzu/giphy.gif\nhttps://media.giphy.com/media/3gncMZgcxrBfzivjND/giphy.gif")

bot.run('token')
