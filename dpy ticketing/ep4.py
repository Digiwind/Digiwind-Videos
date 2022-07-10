#code added in https://youtu.be/SHuGkt_Z4bA
#button:
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

#slash command:
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

#client:
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
            #await tree.sync(guild = discord.Object(id=guild_id)) #guild specific: leave blank if global (global registration can take 1-24 hours)
            self.synced = True
        if not self.added:
            self.add_view(ticket_launcher())
            self.add_view(main())
            self.added = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)
