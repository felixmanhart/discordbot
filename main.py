import asyncio
import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
    
bot = commands.Bot(command_prefix="s!", intents=discord.Intents.all())
bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('Simple Service | !help'))
    print("Started!")

@bot.command()
async def help(ctx):
    em = discord.Embed(title='Bot Hilfe!', description="""
    **Moderation:**\n
    `ban` bannt einen Nutzer.\n 
    `kick` kick einen Nutzer.\n
    `unban` entbannt einen Nutzer.\n
    `mute` setzt einen Nutzer ins Timeout.\n
    \n
    **Ulity**
    `nuke` löscht bestimmte Anzahl an Nachrichten im Chat\.n
    `mehr kommt später...`  
    """, colour=discord.Colour.red())
    await ctx.send(embed=em)

@bot.command()
@commands.has_role("ping permission")
@commands.cooldown(1, 172800, commands.BucketType.user)
async def ping(ctx: commands.Context):
    await ctx.send(f'{ctx.guild.default_role}', delete_after=172800)
    message: discord.Message = ctx.message

    await message.delete()

@bot.command()
@commands.has_role("Ticket Service")
async def ltc(ctx: commands.Context):
    await ctx.send(f'||ltc1q52zrfd6cernk0325quwmwsd9jkued2w9rswz43||', delete_after=60)
    message: discord.Message = ctx.message

    await message.delete()

@bot.command()
@commands.has_role("Ticket Service")
async def paypal(ctx):
    em = discord.Embed(colour=discord.Colour.blue(), title="Raions Paypal", description="**raionsozials@gmail.com**\n**friends & family**\n**+screenshot**")
    await ctx.send(embed=em)
    message: discord.Message = ctx.message

    await message.delete()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=discord.Color.red())
        embed.add_field(name="Access denied", value='You don\'t have Permissions to do that.')
        await ctx.send(embed= embed)
        await ctx.message.delete()
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"You can only ping every 48 hours!",
                           description=f"Try again in 48h.", colour=discord.Colour.red())
        await ctx.send(embed=em, delete_after=5)
        await ctx.message.delete()



async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename.find("__") == -1:
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    await load()
    await bot.start(os.getenv("TOKEN"))



asyncio.run(main())
