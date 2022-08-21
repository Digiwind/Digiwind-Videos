#discord.py 2.0
#from: link coming soon...

import discord
from discord.ext import commands
from datetime import timedelta

class Client(discord.Client):
    def __init__(self):
        intents = discord.Intents.default() #antispam doesn't need message content intent
        super().__init__(intents = intents)
        self.anti_spam = commands.CooldownMapping.from_cooldown(5, 15, commands.BucketType.member)
        self.too_many_violations = commands.CooldownMapping.from_cooldown(4, 60, commands.BucketType.member)

    async def on_ready(self):
        print(f'We have logged in as {self.user}.')
    
    async def on_message(self, message):
        if type(message.channel) is not discord.TextChannel or message.author.bot: return
        bucket = self.anti_spam.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, don't spam!", delete_after = 10)
            violations = self.too_many_violations.get_bucket(message)
            check = violations.update_rate_limit()
            if check:
                await message.author.timeout(timedelta(minutes = 10), reason = "Spamming")
                try: await message.author.send("You have been muted for spamming!")
                except: pass

client = Client()

import os
from dotenv import load_dotenv
load_dotenv('token.env')
client.run(os.environ['TOKEN'])
