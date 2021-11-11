import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!') #bot's prefix

@bot.event 
async def on_ready():
    print('We have logged in as {0.user}'.format(bot)) #tells us that our bot is online

@bot.event #responding to messages
async def on_message(message):
    message.content = (message.content.lower()) #makes all messages lowercase, from the bot's perspective
    if message.author == bot.user: #to not respond to bots
        return
    if "hello" in message.content:
        await message.channel.send("Hi!") #response
    if "rickroll" in message.content:
        await message.channel.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    await bot.process_commands(message) #VERY IMPORTANT, if this line is not added, the bot will not respond to commands
    
@bot.command(aliases=['test2', 'testing']) #other names for the command
async def test(ctx): #test is the command name
    await ctx.send("yes, yes, I am working.") #response to the command

@bot.command(aliases = ['8ball'])
async def ball(ctx): #can't really put numbers in the command name so we have 8ball as an alias instead
    import random
    ballresponses = ['Yes', 'No']
    z = random.choice(ballresponses) #choose yes or no, randomly
    await ctx.send(z) #send either yes or no 

bot.run('') #put your token here 
