import asyncio
import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot

bot = Bot(command_prefix = "!", intents=discord.Intents.default())

@bot.event
async def on_ready():
    print("bot is on")

@bot.command()
@commands.has_role("ping permission")
@commands.cooldown(1, 172800, commands.BucketType.user)
async def ping(ctx):
    ctx.send(ctx.message.guild.default_role)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Error", description="You can only ping every 48h!", colour=discord.Colour.red())
        await ctx.send(embed=embed)


bot.run("MTAyMzYyNDU1OTkzODc3NzE2OQ.GbWcde.aK9epNRBLanTd0h4cDtJTeOri0CD3E7IXcxIm4")
