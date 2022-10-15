import asyncio
import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
    
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
@commands.has_role(1030540753224605716)
@commands.cooldown(1, 60 * 60 * 24 * 2, commands.BucketType.user)
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
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(colour=discord.Colour.red(), description=f"""
        Can\'t mention everyone, pls try again in {:.2}.""")
        await ctx.send(embed=em)


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename.find("__") == -1:
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    await load()
    await bot.start(os.getenv("TOKEN"))



asyncio.run(main())