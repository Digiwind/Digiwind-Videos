import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='^') #prefix

@bot.event 
async def on_ready():
    print('We have logged in as {0.user}'.format(bot)) #tells us that our bot is online 

@bot.event
async def on_message(message):
    message.content = (message.content.lower()) #makes everything lowercase 
    if "troll" in message.content: #bot trigger
        await message.channel.send("") #what you want to send

bot.run('') #put your token here