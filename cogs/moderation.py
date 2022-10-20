import datetime
import discord
from discord.ext import commands



class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        print("Registered Moderation Cog")

        self.PRICE_CHANNEL = 1030518089307132025

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if reason==None:
            reason="no reason provided"
        await ctx.guild.kick(member)
        await ctx.send(f"{member.mention} has been kicked for {reason}.")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, duration, timescale, *, reason=None):
        if reason == None:
            reason = "no reason provided"
        timescale = timescale.lower()
        timescales = {
        's': 'seconds', 'second': 'seconds',
        'm': 'minutes', 'minute': 'minutes',
        'h': 'hours', 'hour': 'hours',
        'd': 'days', 'day': 'days',
        'w': 'weeks', 'week': 'weeks'
        }

        if timescale not in timescales and timescale not in timescales.values():
            await ctx.send(f'"{timescale}" is not a valid Time Scale')
            return
        if member.is_timed_out():
            await ctx.send(f"{member.mention} is already timed out.")
            return

        try:
            timescale = timescales[timescale]
        except KeyError:
            pass

        time_data = {timescale: int(duration)}
        delta = datetime.timedelta(**time_data)
        try:
            await member.timeout(delta, reason=reason)
            await ctx.send(f'Muted {member.mention} for {duration} {timescale} for {reason}.')
        except discord.errors.HTTPException:
            await ctx.send(f"Invalid amount of time to time {member.mention} out for.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if reason==None:
            reason="no reason provided"
        await ctx.guild.ban(member)
        await ctx.send(f"{member.mention} has been banned for {reason}.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member):
        if str(member).find("#") == -1:
            async for e in ctx.guild.bans():
                user = e.user
                if user.id == member:
                    await ctx.guild.unban(user)
                    await ctx.send(f'Unbanned {user.mention}.')
                    return
            await ctx.send(f'The user with id `{member}` is not banned.')
        else:
            member_name, member_discriminator = member.split('#')
            async for e in ctx.guild.bans():
                user = e.user
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f'Unbanned {user.mention}.')
                    return
            await ctx.send(f'The user `{member}` is not banned.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prices(self, ctx):
        emb = discord.Embed(title="Discord Nitro Prices",description="Prices for Discord Nitro!" , color=discord.Colour.purple())
        emb.add_field(name="Monthly", value="Nitro Classic 2.50€\n Nitro Boost 3.50€")
        emb.add_field(name="Yearly", value="Nitro Classic 6€\n Nitro Boost 9€", inline=False)
        await ctx.send(embed=emb)
        await ctx.reply("Send!")
async def setup(bot):
    await bot.add_cog(ModerationCog(bot))