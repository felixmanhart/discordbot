import discord
import interactions
import discord.ui
from discord.ui import Button
from discord.ext import commands


class BotButton(Button):
    def __init__(self):
        super().__init__(
            label="Bot Info!",
            style=discord.enums.ButtonStyle.grey,
            custom_id="interaction:BotButton",
        )

    async def callback(self, interaction: discord.Interaction):
        helpinfo = discord.Embed(title="Bot Hilfe für Administratoren.", description=
        """**Folgende Infos sind nur für die Commands!**
        `/help` Öffnet dieses Hilfezentrum.
        `/close` Schließt das Ticket.
        `/nuke` Löscht sämtliche Nachrichten in einem Channel.
        `/hello` Grüßt den Bot.
        **Dieser Bot wird nur für Ulity und Tickets benutzt.**""", colour=discord.Colour.greyple())
        await interaction.response.send_message(embed=helpinfo, ephemeral=True)

class ServerButton(Button):
    def __init__(self):
        super().__init__(
            label="Server Info!",
            style=discord.enums.ButtonStyle.grey,
            custom_id="interaction:ServerButton",
        )

    async def callback(self, interaction: discord.Interaction):
        serverinfo = discord.Embed(title="Server Informationen", description="""
        **Hier findest du einige Infos über unseren Service:**

        Wir sind der beste Nitro Seller Deutschlands und bieten dir hier günstig Discord Nitro an.
        Falls du also Nitro suchst, bist du genau richtig. Unser Team bietet einen tollen Eindruck auf den Server und ist 24/7 für Support da.
        Außerdem gibt es bei uns auch, immer mal wieder, einige Giveaways, wo du etwas gewinnen kannst!

        Um die Preise zu sehen, kannst du dir einfach unserer Channel anschauen.
        **Öffne ein Ticket um Nitro noch heute *simple* und günstig zu kaufen!**""",
                                   colour=discord.Colour.greyple())
        await interaction.response.send_message(embed=serverinfo, ephemeral=True)
