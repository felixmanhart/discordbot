import asyncio
import os
import discord
from discord import app_commands
from discord.ext import commands


from dotenv import load_dotenv

load_dotenv()

class Client(commands.Bot):

    def __init__(self, command_prefix, application_id, initial_extensions):
        super().__init__(
            command_prefix=command_prefix,
            application_id=application_id,
            intents=discord.Intents.all()
        )

        self.initial_extensions = initial_extensions

    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        await bot.tree.sync(guild=discord.Object(id=938105317781307392))

    async def on_ready(self):
        print(f"Bot is online")


if __name__ == "__main__":
    initial_extensions = [
        "cogs.ticket",
        "cogs.utility"
    ]

    bot = Client(command_prefix="$", application_id=1035657488533573652, initial_extensions=initial_extensions)

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename.find("__") == -1:
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    await load()
    await bot.start(os.getenv("TOKEN"))



asyncio.run(main())
