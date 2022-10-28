import asyncio
import discord
from discord.ui import Button, View
from discord.ext import commands

class BoostCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

        self.GUILD_ID = 938105317781307392
        self.TEAM_ROLE = 1030518060559372318
        self.TICKET_CHANNEL = 1035284564354027613
        self.CATEGORY_ID = 1030518071003201666

        print("Registered boost Cog")

    @commands.command()
    @commands.is_owner()
    async def boosts(self, ctx):
        button1 = Button(label=":booster: Buy Boosts!", style=discord.ButtonStyle.grey, custom_id="boost_button")
        view = View()
        view.add_item(button1)
        emb = discord.Embed(description="If you need *cheap* server boosts:", title=f":booster: **Server Boosts**", colour=discord.Colour.purple())
        emb.add_field(name="3 Months", value="**7 Boosts** = $8 :pp:/ $7 :ltc:\n **14 Boosts** $15 :pp:/ $10 :ltc:", inline=False)
        emb.add_field(name=":yes:", value="If you want **buy server boosts** click the button down below!", inline=False)
        channel = self.bot.get_channel(self.TICKET_CHANNEL)
        await channel.send(embed=emb, view=view)
        await ctx.send(":yes: Sent!")

    @commands.command()
    @commands.is_owner()
    async def setup(self, ctx):
        button1 = Button(label="Create Ticket!", style=discord.ButtonStyle.blurple, custom_id="ticket_button")
        button2 = Button(label="Buy!", style=discord.ButtonStyle.green, custom_id="buy_button")
        view = View()
        view.add_item(button1)
        view.add_item(button2)
        emb = discord.Embed(description="Only **create a Ticket** if you want to buy or need help!",
                            title=f"Buy & Support", colour=discord.Colour.blue())
        channel = self.bot.get_channel(self.TICKET_CHANNEL)
        await channel.send(embed=emb, view=view)
        await ctx.send("Sent!")

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.channel.id == self.TICKET_CHANNEL:
            if "buy_button" in str(interaction.data):
                guild = self.bot.get_guild(self.GUILD_ID)
                for ticket in guild.channels:
                    if str(interaction.user.id) in ticket.name:
                        embed = discord.Embed(
                            description=f"You can't open server boost tickets twice.\nYou alredy opend a server boost ticket!: {ticket.mention}")
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        return

                category = self.bot.get_channel(self.CATEGORY_ID)
                ticket_num = 1 if len(category.channels) == 0 else int(category.channels[-1].name.split("-")[1]) + 1
                ticket_channel = await guild.create_text_channel(f"boost-{ticket_num}", category=category,
                                                                 topic=f"Buyer {interaction.user} \nClient-ID: {interaction.user.id}")

                await ticket_channel.set_permissions(guild.get_role(self.TEAM_ROLE), send_messages=True,
                                                     read_messages=True, add_reactions=False,
                                                     embed_links=True, attach_files=True, read_message_history=True,
                                                     external_emojis=True)
                await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True,
                                                     add_reactions=False,
                                                     embed_links=True, attach_files=True, read_message_history=True,
                                                     external_emojis=True)
                embed = discord.Embed(description=f"**Waiting for Boost Service!**\nTo close the ticket use `!close`", color=62719)
                embed.set_author(name=f'Server Boosts!')
                mess_2 = await ticket_channel.send(embed=embed)
                embed = discord.Embed(title="📬 Opend buy request!",
                                      description=f'Your server boost ticket!: {ticket_channel.mention}',
                                      color=discord.colour.Color.green())

                await interaction.response.send_message(f"Welcome {interaction.user.mention}", embed=embed, ephemeral=True)
                return

    @commands.command()
    async def close(self, ctx):
        if "ticket-" or "buy-" in ctx.channel.name:
            embed = discord.Embed(
                description=f'**Ticket will be closed in 5 seconds.**',
                color=16711680)
        await ctx.channel.send(embed = embed)
        await asyncio.sleep(5)
        await ctx.channel.delete()

async def setup(bot):
    await bot.add_cog(BoostCog(bot))