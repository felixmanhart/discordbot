import asyncio
import discord
from discord.ui import Button, View
from discord.ext import commands
from discord.utils import get


class BoostsCog(commands.Cog):
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
        emoji = get(ctx.message.server.emojis, name="booster")
        button1 = Button(label=f"{emoji} Buy Boosts!", style=discord.ButtonStyle.grey, custom_id="boost_button")
        view = View()
        view.add_item(button1)
        emoji2 = get(ctx.message.server.emojis, name="pp")
        emoji3 = get(ctx.message.server.emojis, name="yes")
        emoji4 = get(ctx.message.server.emojis, name="ltc")
        emb = discord.Embed(description="If you need *cheap* server boosts:", title=f"{emoji} **Server Boosts**", colour=discord.Colour.purple())
        emb.add_field(name="3 Months", value=f"**7 Boosts** = $8 {emoji2}/ $7 {emoji4}\n **14 Boosts** $15 {emoji2}/ $10 {emoji4}", inline=False)
        emb.add_field(name=f"{emoji3}", value="If you want **buy server boosts** click the button down below!", inline=False)
        channel = self.bot.get_channel(self.TICKET_CHANNEL)
        await channel.send(embed=emb, view=view)
        await ctx.send(f"{emoji3} Sent!")

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.channel.id == self.TICKET_CHANNEL:
            if "boost_button" in str(interaction.data):
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

async def setup(bot):
    await bot.add_cog(BoostsCog(bot))