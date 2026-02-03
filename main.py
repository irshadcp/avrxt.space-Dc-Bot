import discord
from discord.ext import commands
import os

intents = discord.Intents.all()

class AvrxtBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!", 
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        # Load extensions (Cogs)
        extensions = ['cogs.moderation', 'cogs.automod', 'cogs.tickets', 'cogs.utility']
        for ext in extensions:
            await self.load_extension(ext)
        
        # Syncing slash commands
        await self.tree.sync()
        print(f"Synced slash commands for {self.user}")

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        await self.change_presence(activity=discord.Game(name="AVRXT'S SPACE"))

bot = AvrxtBot()

# Replace with your actual token
bot.run('YOUR_BOT_TOKEN_HERE')
