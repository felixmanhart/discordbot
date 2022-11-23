import discord
import interactions
from discord.ext import commands
from discord import app_commands
from discord.ui import View
from lib.buttons import BotButton, ServerButton



class Utility(commands.Cog):
    def __int__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="Information über den Bot/ über den Server.")
    async def help(self, interation: interactions.Interaction):
        helpembed = discord.Embed(title="Informationen!",
                                  description=f"**Um eine Information zu sehen, musst du einen der unteren Knöpfe drücken!**\nWenn du Kontakt zum Team brauchst, dann öffne ein Ticket!",
                                  colour=discord.Colour.red())
        view = View()
        view.add_item(BotButton())
        view.add_item(ServerButton())

        await interation.response.send_message(embed=helpembed, view=view, ephemeral=True)

    @app_commands.command(name="nuke", description="Säubert den Channel.")
    @app_commands.default_permissions(manage_channels=True)
    async def nuke(self, interaction: discord.Interaction):
        await interaction.channel.purge()
        await interaction.response.send_message(f"Nuked by `{interaction.user}`!")

    @app_commands.command(name="hello", description="Sag Hallo zu dem Bot.")
    async def hello(self, interation: interactions.Interaction):
        await interation.response.send_message(f"Hallo {interation.user.mention}, ich hoffe dir geht es gut!")


async def setup(bot: commands.Bot):
    await bot.add_cog(
        Utility(bot),
        guilds=[discord.Object(id=938105317781307392)]
    )
