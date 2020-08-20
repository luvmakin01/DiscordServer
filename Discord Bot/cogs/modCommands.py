import discord, json
from typing import Optional
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, Greedy

class mainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(title = "Bot Latency", description = f'{round(self.bot.latency * 1000)}ms', color = discord.Color(0xff0000))
        embed.set_footer(text = 'Created by OR Dev Team.')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_any_role('Admin', 'Moderator')
    async def purge(self, ctx, limit=1):
        await ctx.message.channel.purge(limit=int(limit) + 1)

    @commands.command()
    @commands.has_any_role('Admin', 'Moderator')
    async def kick(self, ctx, targets: Greedy[discord.Member], *, reason: Optional[str] = "No reason provided!"):
        if not len(targets):
            await ctx.send('Please enter a valid username!')
        else:
            for target in targets:
                await target.kick(reason=reason)
                embed = discord.Embed(title = "Kicked Member", description = 'Command used by {}'.format(ctx.author) + '!\nKicked {}'.format(target) + '!', color = discord.Color(0xff0000))
                embed.set_footer(text = 'Developed by OR Dev Team.')
                file = open('./json/channels.json', 'r')
                data = json.load(file)
                channel = data["logs"]
                await self.bot.get_channel(channel).send(embed=embed)            

    @commands.command()
    @commands.has_any_role('Admin', 'Moderator')
    async def set(self, ctx, *, channel_id):
        file = open('./json/channels.json', 'r')
        data = json.load(file)
        channels = str(channel_id)
        channels = channels.replace('<','').replace('#','').replace('>','')
        data["logs"] = int(channels)
        with open('./json/channels.json', 'w') as tf:
            json.dump(data, tf)
        await ctx.send('Channel set successfully!')

def setup(bot):
    bot.add_cog(mainCog(bot))
