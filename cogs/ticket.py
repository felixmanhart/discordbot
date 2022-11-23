import discord
import asyncio
import interactions
from discord.ui import View, Button
from discord.ext import commands
from discord import app_commands


class Ticket(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.TICKET_CHANNEL = 1030518079857369190
        self.GUILD_ID = 938105317781307392
        self.CATEGORY_ID = 1030518071003201666
        self.TEAM_ROLE = 1030518060559372318

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        ticketview = View()
        ticketview.add_item(SupportButton(self.bot))
        ticketview.add_item(BuyButton(self.bot))
        setupembed = discord.Embed(title="Tickets", description=
        """Wenn du Hilfe brauchst, oder etwas kaufen möchtest, musst du nur die **unteren Knöpfe drücken.**
        **Ping das Team aber nicht! Wir werden uns bei dir melden.**"""
                                   )
        channel = self.bot.get_channel(self.TICKET_CHANNEL)
        await channel.send(embed=setupembed, view=ticketview)
        await ctx.send("gesendet")

    @app_commands.command(name="close", description="Schließt das Ticket!")
    async def close(self, ctx: interactions.CommandContext) -> None:
        if ctx.channel.name.__contains__("support-") or ctx.channel.name.__contains__("nitro-"):
            embed = discord.Embed(
                description=f'Ticket schließt in 5 Sekunden automatisch!',
                colour=discord.Colour.red())
            await ctx.response.send_message(embed=embed)
            await asyncio.sleep(5)
            await ctx.channel.delete()
        else:
            embederror = discord.Embed(description="Kann nur in Tickets verwendet werden.", colour=discord.Colour.red())
            await ctx.response.send_message(embed=embederror)


async def setup(bot: commands.Bot):
    await bot.add_cog(
        Ticket(bot),
        guilds=[discord.Object(id=938105317781307392)]
    )

class BuyButton(Button):
    def __init__(self, bot):
        super().__init__(
            label="Kaufen!",
            style=discord.enums.ButtonStyle.grey,
            custom_id="interaction:BuyButton",
        )

        self.TICKET_CHANNEL = 1030518079857369190
        self.GUILD_ID = 938105317781307392
        self.CATEGORY_ID = 1030518071003201666
        self.TEAM_ROLE = 1030518060559372318

        self.bot = bot

    async def callback(self, interaction: interactions.Interaction):
        guild = self.bot.get_guild(self.GUILD_ID)
        category = self.bot.get_channel(self.CATEGORY_ID)
        ticket_num = 1 if len(category.channels) == 0 else int(category.channels[-1].name.split("-")[1]) + 1
        ticket_channel = await guild.create_text_channel(f"nitro-{ticket_num}", category=category,
                                                         topic=f"Kaufanfrage von {interaction.user} \nClient-ID: {interaction.user.id}")

        await ticket_channel.set_permissions(guild.get_role(self.TEAM_ROLE), send_messages=True, read_messages=True,
                                             add_reactions=False,
                                             embed_links=True, attach_files=True, read_message_history=True,
                                             external_emojis=True)
        await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True,
                                             add_reactions=False,
                                             embed_links=True, attach_files=True, read_message_history=True,
                                             external_emojis=True)
        inticketembed = discord.Embed(title=f"Welcome {interaction.user}", description=
        f"""Willkommen im Ticket {interaction.user.mention}! 
                                         **Das Team wird sich melden! <@&1030518060559372318>** 
                                         Ticket mit `/close` schließen!"""
                                      )
        inticketembed.set_author(name=f'Anfrage gesendet!')
        mess_2 = await ticket_channel.send(embed=inticketembed)
        successembed = discord.Embed(title="Anfrage erfolgreich gestellt!",
                                     description=f"Deine Anfrage wurde gestellt! {ticket_channel.mention}",
                                     color=discord.colour.Color.green()
                                     )
        await interaction.response.send_message(embed=successembed, ephemeral=True)
        return


class SupportButton(Button):
    def __init__(self, bot):
        super().__init__(
            label="Support!",
            style=discord.enums.ButtonStyle.grey,
            custom_id="interaction:SupportButton",
        )

        self.TICKET_CHANNEL = 1030518079857369190
        self.GUILD_ID = 938105317781307392
        self.CATEGORY_ID = 1030518071003201666
        self.TEAM_ROLE = 1030518060559372318

        self.bot = bot

    async def callback(self, interaction: interactions.Interaction):
        guild = self.bot.get_guild(self.GUILD_ID)
        category = self.bot.get_channel(self.CATEGORY_ID)
        ticket_num = 1 if len(category.channels) == 0 else int(category.channels[-1].name.split("-")[1]) + 1
        ticket_channel = await guild.create_text_channel(f"support-{ticket_num}", category=category,
                                                         topic=f"Supportanfrage von {interaction.user} \nClient-ID: {interaction.user.id}")

        await ticket_channel.set_permissions(guild.get_role(self.TEAM_ROLE), send_messages=True, read_messages=True,
                                             add_reactions=False,
                                             embed_links=True, attach_files=True, read_message_history=True,
                                             external_emojis=True)
        await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True,
                                             add_reactions=False,
                                             embed_links=True, attach_files=True, read_message_history=True,
                                             external_emojis=True)

        inticketembed = discord.Embed(title=f"Welcome {interaction.user}", description=
        f"""Willkommen im Ticket {interaction.user.mention}! 
                                         **Das Team wird sich melden! <@&1030518060559372318>** 
                                         Ticket mit `/close` schließen!"""
                                      )
        mess_2 = await ticket_channel.send(embed=inticketembed)
        successembed = discord.Embed(title="Anfrage erfolgreich gestellt!",
                                     description=f"Deine Anfrage wurde gestellt! {ticket_channel.mention}",
                                     color=discord.colour.Color.green()
                                     )
        await interaction.response.send_message(embed=successembed, ephemeral=True)
        return
