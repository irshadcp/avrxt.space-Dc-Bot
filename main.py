import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class AvrxtBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents, help_command=None)

    async def setup_hook(self):
        # Automatically load all files in the cogs folder
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f"Loaded Cog: {filename}")
        
        # Sync slash commands with Discord
        await self.tree.sync()

bot = AvrxtBot()

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user} (ID: {bot.user.id})')
    await bot.change_presence(activity=discord.Game(name="AVRXT'S SPACE"))

bot.run(TOKEN)
