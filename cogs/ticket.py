import asyncio
import discord
from discord.ui import Button, View
from discord.ext import commands

class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

        self.GUILD_ID = 938105317781307392
        self.TEAM_ROLE = 1030518060559372318
        self.TICKET_CHANNEL = 1030518079857369190
        self.CATEGORY_ID = 1030518071003201666

        print("Registered ticket Cog")

    @commands.command()
    @commands.is_owner()
    async def setup(self, ctx):
        button1 = Button(label="Hilfe!", style=discord.ButtonStyle.red, custom_id="ticket_button")
        button2 = Button(label="Nitro kaufen!", style=discord.ButtonStyle.red, custom_id="buy_button")
        view = View()
        view.add_item(button1)
        view.add_item(button2)
        emb = discord.Embed(description="Only **create a Ticket** if you want to buy or need help!", title=f"Buy & Support", colour=discord.Colour.blue())
        emb.set_footer(
            icon_url="https://cdn.discordapp.com/attachments/1030518107388788736/1035695718255579208/1.png",
            text="Ticket System | Simple Service")
        channel = self.bot.get_channel(self.TICKET_CHANNEL)
        await channel.send(embed=emb, view=view)
        await ctx.send("✅ Sent!")


    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.channel.id == self.TICKET_CHANNEL:
            if "ticket_button" in str(interaction.data):
                guild = self.bot.get_guild(self.GUILD_ID)
                for ticket in guild.channels:
                    if str(interaction.user.id) in ticket.name:
                        embed2 = discord.Embed(
                            description=f"Du kannst keine Hilfe-Anfragen mehrmals stellen!\nDu hast bereits eine gestellt: {ticket.mention}")
                        await interaction.response.send_message(embed=embed2, ephemeral=True)
                        return

                category = self.bot.get_channel(self.CATEGORY_ID)
                ticket_num = 1 if len(category.channels) == 0 else int(category.channels[-1].name.split("-")[1]) + 1
                ticket_channel = await guild.create_text_channel(f"support-{ticket_num}", category=category,
                                                                 topic=f"Member {interaction.user} \nClient-ID: {interaction.user.id}")

                await ticket_channel.set_permissions(guild.get_role(self.TEAM_ROLE), send_messages=True,
                                                     read_messages=True, add_reactions=False,
                                                     embed_links=True, attach_files=True, read_message_history=True,
                                                     external_emojis=True)
                await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True,
                                                     add_reactions=False,
                                                     embed_links=True, attach_files=True, read_message_history=True,
                                                     external_emojis=True)
                embed3 = discord.Embed(description=f"""
                **Warten auf {self.TEAM_ROLE}...**\n
                *Bitte das Team nicht pingen, wir werden uns bei dir melden.*\n
                Um das Ticket zu schließen, nutzte `!close`.
                """, color=discord.Colour.blue())
                embed3.set_author(name=f'Support-Anfrage!')
                mess_2 = await ticket_channel.send(embed=embed3)
                embed3 = discord.Embed(title="Anfrage gesendet!",
                                      description=f'Hier findest du deine Anfrage!: {ticket_channel.mention}',
                                      color=discord.colour.Color.green())

                await interaction.response.send_message(embed=embed3, ephemeral=True)
                return

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.channel.id == self.TICKET_CHANNEL:
            if "buy_button" in str(interaction.data):
                guild = self.bot.get_guild(self.GUILD_ID)
                for ticket in guild.channels:
                    if str(interaction.user.id) in ticket.name:
                        embed = discord.Embed(
                            description=f"Du kannst keine Kaufanfrage mehrmals senden!\nDu hast bereits eine gestellt: {ticket.mention}")
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        return

                category = self.bot.get_channel(self.CATEGORY_ID)
                ticket_num = 1 if len(category.channels) == 0 else int(category.channels[-1].name.split("-")[1]) + 1
                ticket_channel = await guild.create_text_channel(f"nitro-{ticket_num}", category=category,
                                                                 topic=f"Käufer {interaction.user} \nClient-ID: {interaction.user.id}")

                await ticket_channel.set_permissions(guild.get_role(self.TEAM_ROLE), send_messages=True,
                                                     read_messages=True, add_reactions=False,
                                                     embed_links=True, attach_files=True, read_message_history=True,
                                                     external_emojis=True)
                await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True,
                                                     add_reactions=False,
                                                     embed_links=True, attach_files=True, read_message_history=True,
                                                     external_emojis=True)
                embe = discord.Embed(description=f"""
                **Warten auf {self.TEAM_ROLE}...**\n
                *Bitte das Team nicht pingen, wir werden uns bei dir melden.*\n
                Um das Ticket zu schließen, nutzte `!close`.
                """, color=discord.Colour.blue())
                embe.set_author(name=f'Nitro kaufen!')
                mess_2 = await ticket_channel.send(embed=embe)
                embe = discord.Embed(title="Anfrage gesendet!",
                                      description=f'Hier findest du deine Anfrage!: {ticket_channel.mention}',
                                      color=discord.colour.Color.green())

                await interaction.response.send_message(embed=embe, ephemeral=True)
                return

    @commands.command()
    async def close(self, ctx):
        if "support-" or "nitro-" or "boost-" in ctx.channel.name:
            embed = discord.Embed(
                description=f'**Ticket will be closed in 5 seconds.**',
                color=16711680)
        await ctx.channel.send(embed=embed)
        await asyncio.sleep(5)
        await ctx.channel.delete()

async def setup(bot):
    await bot.add_cog(TicketCog(bot))