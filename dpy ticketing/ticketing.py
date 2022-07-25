import discord, os
from datetime import datetime
from discord import app_commands, utils
from discord.ext import commands

class ticket_launcher(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 600, commands.BucketType.member)
    
    @discord.ui.button(label = "Create a Ticket", style = discord.ButtonStyle.blurple, custom_id = "ticket_button")
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        interaction.message.author = interaction.user
        retry = self.cooldown.get_bucket(interaction.message).update_rate_limit()
        if retry: return await interaction.response.send_message(f"Slow down! Try again in {round(retry, 1)} seconds!", ephemeral = True)
        ticket = utils.get(interaction.guild.text_channels, name = f"ticket-for-{interaction.user.name.lower().replace(' ', '-')}-{interaction.user.discriminator}")
        if ticket is not None: await interaction.response.send_message(f"You already have a ticket open at {ticket.mention}!", ephemeral = True)
        else:
            if type(client.ticket_mod) is not discord.Role: 
                client.ticket_mod = interaction.guild.get_role(role_id)
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                interaction.user: discord.PermissionOverwrite(view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True), 
                client.ticket_mod: discord.PermissionOverwrite(view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True),
            }
            try: channel = await interaction.guild.create_text_channel(name = f"ticket-for-{interaction.user.name}-{interaction.user.discriminator}", overwrites = overwrites, reason = f"Ticket for {interaction.user}")
            except: return await interaction.response.send_message("Ticket creation failed! Make sure I have `manage_channels` permissions!", ephemeral = True)
            await channel.send(f"{client.ticket_mod.mention}, {interaction.user.mention} created a ticket!", view = main())
            await interaction.response.send_message(f"I've opened a ticket for you at {channel.mention}!", ephemeral = True)

class confirm(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)
        
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.red, custom_id = "confirm")
    async def confirm_button(self, interaction, button):
        try: await interaction.channel.delete()
        except: await interaction.response.send_message("Channel deletion failed! Make sure I have `manage_channels` permissions!", ephemeral = True)

class main(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)
    
    @discord.ui.button(label = "Close Ticket", style = discord.ButtonStyle.red, custom_id = "close")
    async def close(self, interaction, button):
        embed = discord.Embed(title = "Are you sure you want to close this ticket?", color = discord.Colour.blurple())
        await interaction.response.send_message(embed = embed, view = confirm(), ephemeral = True)

    @discord.ui.button(label = "Transcript", style = discord.ButtonStyle.blurple, custom_id = "transcript")
    async def transcript(self, interaction, button):
        await interaction.response.defer()
        if os.path.exists(f"{interaction.channel.id}.md"):
            return await interaction.followup.send(f"A transcript is already being generated!", ephemeral = True)
        with open(f"{interaction.channel.id}.md", 'a') as f:
            f.write(f"# Transcript of {interaction.channel.name}:\n\n")
            async for message in interaction.channel.history(limit = None, oldest_first = True):
                created = datetime.strftime(message.created_at, "%m/%d/%Y at %H:%M:%S")
                if message.edited_at:
                    edited = datetime.strftime(message.edited_at, "%m/%d/%Y at %H:%M:%S")
                    f.write(f"{message.author} on {created}: {message.clean_content} (Edited at {edited})\n")
                else:
                    f.write(f"{message.author} on {created}: {message.clean_content}\n")
            generated = datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
            f.write(f"\n*Generated at {generated} by {client.user}*\n*Date Formatting: MM/DD/YY*\n*Time Zone: UTC*")
        with open(f"{interaction.channel.id}.md", 'rb') as f:
            await interaction.followup.send(file = discord.File(f, f"{interaction.channel.name}.md"))
        os.remove(f"{interaction.channel.id}.md")
    
class aclient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents = intents)
        self.synced = False #we use this so the bot doesn't sync commands more than once
        self.added = False
        self.ticket_mod = role_id

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #check if slash commands have been synced 
            await tree.sync(guild = discord.Object(id=guild_id)) #guild specific: leave blank if global (global registration can take 1-24 hours)
            self.synced = True
        if not self.added:
            self.add_view(ticket_launcher())
            self.add_view(main())
            self.added = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

@tree.command(guild = discord.Object(id=guild_id), name = 'ticket', description='Launches the ticketing system') #guild specific slash command
@app_commands.default_permissions(manage_guild = True)
@app_commands.checks.cooldown(3, 60, key = lambda i: (i.guild_id))
@app_commands.checks.bot_has_permissions(manage_channels = True)
async def ticketing(interaction: discord.Interaction):
    embed = discord.Embed(title = "If you need support, click the button below and create a ticket!", color = discord.Colour.blue())
    await interaction.channel.send(embed = embed, view = ticket_launcher())
    await interaction.response.send_message("Ticketing system launched!", ephemeral = True)

@tree.command(guild = discord.Object(id=guild_id), name = 'close', description='Closes the ticket') #guild specific slash command
@app_commands.checks.bot_has_permissions(manage_channels = True)
async def close(interaction: discord.Interaction):
    if "ticket-for-" in interaction.channel.name:
        embed = discord.Embed(title = "Are you sure you want to close this ticket?", color = discord.Colour.blurple())
        await interaction.response.send_message(embed = embed, view = confirm(), ephemeral = True)
    else: await interaction.response.send_message("This isn't a ticket!", ephemeral = True)

@tree.command(guild = discord.Object(id=guild_id), name = 'add', description='Adds a user to the ticket') #guild specific slash command
@app_commands.describe(user = "The user you want to add to the ticket")
@app_commands.default_permissions(manage_channels = True)
@app_commands.checks.cooldown(3, 20, key = lambda i: (i.guild_id, i.user.id))
@app_commands.checks.bot_has_permissions(manage_channels = True)
async def add(interaction: discord.Interaction, user: discord.Member):
    if "ticket-for-" in interaction.channel.name:
        await interaction.channel.set_permissions(user, view_channel = True, send_messages = True, attach_files = True, embed_links = True)
        await interaction.response.send_message(f"{user.mention} has been added to the ticket by {interaction.user.mention}!")
    else: await interaction.response.send_message("This isn't a ticket!", ephemeral = True)

@tree.command(guild = discord.Object(id=guild_id), name = 'remove', description='Removes a user from the ticket') #guild specific slash command
@app_commands.describe(user = "The user you want to remove from the ticket")
@app_commands.default_permissions(manage_channels = True)
@app_commands.checks.cooldown(3, 20, key = lambda i: (i.guild_id, i.user.id))
@app_commands.checks.bot_has_permissions(manage_channels = True)
async def remove(interaction: discord.Interaction, user: discord.Member):
    if "ticket-for-" in interaction.channel.name:
        if type(client.ticket_mod) is not discord.Role: client.ticket_mod = interaction.guild.get_role(role_id)
        if client.ticket_mod not in interaction.user.roles:
            return await interaction.response.send_message("You aren't authorized to do this!", ephemeral = True)
        if client.ticket_mod not in user.roles:
            await interaction.channel.set_permissions(user, overwrite = None)
            await interaction.response.send_message(f"{user.mention} has been removed from the ticket by {interaction.user.mention}!", ephemeral = True)
        else: await interaction.response.send_message(f"{user.mention} is a moderator!", ephemeral = True)
    else: await interaction.response.send_message("This isn't a ticket!", ephemeral = True)

@tree.command(guild = discord.Object(id=guild_id), name = 'transcript', description='Generates a transcript for a ticket') #guild specific slash command
async def transcript(interaction: discord.Interaction): 
    if "ticket-for-" in interaction.channel.name:
        await interaction.response.defer()
        if os.path.exists(f"{interaction.channel.id}.md"):
            return await interaction.followup.send(f"A transcript is already being generated!", ephemeral = True)
        with open(f"{interaction.channel.id}.md", 'a') as f:
            f.write(f"# Transcript of {interaction.channel.name}:\n\n")
            async for message in interaction.channel.history(limit = None, oldest_first = True):
                created = datetime.strftime(message.created_at, "%m/%d/%Y at %H:%M:%S")
                if message.edited_at:
                    edited = datetime.strftime(message.edited_at, "%m/%d/%Y at %H:%M:%S")
                    f.write(f"{message.author} on {created}: {message.clean_content} (Edited at {edited})\n")
                else:
                    f.write(f"{message.author} on {created}: {message.clean_content}\n")
            generated = datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
            f.write(f"\n*Generated at {generated} by {client.user}*\n*Date Formatting: MM/DD/YY*\n*Time Zone: UTC*")
        with open(f"{interaction.channel.id}.md", 'rb') as f:
            await interaction.followup.send(file = discord.File(f, f"{interaction.channel.name}.md"))
        os.remove(f"{interaction.channel.id}.md")
    else: await interaction.response.send_message("This isn't a ticket!", ephemeral = True)

@tree.context_menu(name = "Open a Ticket", guild = discord.Object(id=guild_id))
@app_commands.default_permissions(manage_guild = True)
@app_commands.checks.cooldown(3, 20, key = lambda i: (i.guild_id, i.user.id))
@app_commands.checks.bot_has_permissions(manage_channels = True)
async def open_ticket_context_menu(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer(ephemeral = True)
    ticket = utils.get(interaction.guild.text_channels, name = f"ticket-for-{user.name.lower().replace(' ', '-')}-{user.discriminator}")
    if ticket is not None: await interaction.followup.send(f"{user.mention} already has a ticket open at {ticket.mention}!", ephemeral = True)
    else:
        if type(client.ticket_mod) is not discord.Role: 
            client.ticket_mod = interaction.guild.get_role(role_id)
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
            user: discord.PermissionOverwrite(view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True),
            interaction.guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True), 
            client.ticket_mod: discord.PermissionOverwrite(view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True),
        }
        try: channel = await interaction.guild.create_text_channel(name = f"ticket-for-{user.name}-{user.discriminator}", overwrites = overwrites, reason = f"Ticket for {user}, generated by {interaction.user}")
        except: return await interaction.followup.send("Ticket creation failed! Make sure I have `manage_channels` permissions!", ephemeral = True)
        await channel.send(f"{interaction.user.mention} created a ticket for {user.mention}!", view = main())   
        await interaction.followup.send(f"I've opened a ticket for {user.mention} at {channel.mention}!", ephemeral = True)

@tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        return await interaction.response.send_message(error, ephemeral = True)
    elif isinstance(error, app_commands.BotMissingPermissions):
        return await interaction.response.send_message(error, ephemeral = True)
    else:
        await interaction.response.send_message("An error occurred!", ephemeral = True)
        raise error

import os
from dotenv import load_dotenv
load_dotenv('token.env')
client.run(os.environ['TOKEN'])
