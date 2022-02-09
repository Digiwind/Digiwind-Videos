import discord
from discord.ui import InputText, Modal

bot = discord.Bot()

servers = []

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

class MyModal(Modal):
    def __init__(self) -> None:
        super().__init__("A Modal") #title of the modal up top
        self.add_item(InputText(label="Short Input", placeholder="Placeholder")) 
        self.add_item(
            InputText(
                label= "Long Input", 
                value= "Default", #sort of like a default
                style=discord.InputTextStyle.long, #long/short
            )
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Your Modal Results", color=discord.Color.blurple())
        embed.add_field(name="First Input", value=self.children[0].value, inline=False)
        embed.add_field(name="Second Input", value=self.children[1].value, inline=False)
        await interaction.response.send_message(embeds=[embed])

@bot.slash_command(guild_ids = servers, name= "modal")
async def test(ctx):
    modal = MyModal()
    await ctx.interaction.response.send_modal(modal)

bot.run("token")
