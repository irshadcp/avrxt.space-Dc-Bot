# Save this in cogs/automod.py
import discord
from discord.ext import commands

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bad_words = [] # In a real bot, load this from a database
        self.caps_limit = 70 

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return

        # Bad Word Filter
        if any(word in message.content.lower() for word in self.bad_words):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, that word is not allowed!", delete_after=5)

        # Caps Filter
        if len(message.content) > 10:
            caps_count = sum(1 for c in message.content if c.isupper())
            percent = (caps_count / len(message.content)) * 100
            if percent > self.caps_limit:
                await message.delete()
                await message.channel.send("Too many caps!", delete_after=5)

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
