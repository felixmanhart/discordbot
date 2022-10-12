import asyncio
import json
import os

import discord
from discord.ext import commands


with open("config.json", "r") as f:
    config = json.load(f)
    
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('Rude Alts | !help'))
    print("Started!")

@bot.command()
async def help(ctx):
    em = discord.Embed(title='Rude Alts Help', description="""
    `!ping` This pings @everyone. You only can use it in your own Marketplace.\n
    `!ban` Bans an specified user.\n
    `!unban` Unbans an specified user.\n
    `!kick` Kicks specified user.\n
    `!mute` Timeouts a specified user\n
    `!close` Can only used in a ticket. Closes the ticket.
    """, colour=discord.Colour.red())
    await ctx.send(embed=em)

@bot.command()
@commands.has_permissions(mention_everyone=True)
async def ping(ctx: commands.Context):
    await ctx.send(f'{ctx.guild.default_role}')
    message: discord.Message = ctx.message

    await message.delete()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color= discord.Color.red())
        embed.add_field(name="Access denied", value='You don\'t have Permissions to do that.')
        await ctx.send(embed= embed)
        await ctx.message.delete()


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename.find("__") == -1:
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    await load()
    await bot.start("MTAyMzYyNDU1OTkzODc3NzE2OQ.G3LKl5.Nb6pZkmdO6ku5LDY_fE1WuRqIwsG1pO_XpZgfo")



asyncio.run(main())
