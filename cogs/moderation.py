import discord
from discord import app_commands
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Ban a user")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, itxn: discord.Interaction, member: discord.Member, reason: str = "No reason"):
        await member.ban(reason=reason)
        await itxn.response.send_message(f"✅ Banned {member.name} for: {reason}")

    @app_commands.command(name="nuke", description="Delete and recreate channel")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def nuke(self, itxn: discord.Interaction):
        # Confirmation buttons
        class NukeConfirm(discord.ui.View):
            @discord.ui.button(label="Confirm Nuke", style=discord.ButtonStyle.danger)
            async def confirm(self, i: discord.Interaction, b: discord.ui.Button):
                pos = i.channel.position
                new_ch = await i.channel.clone()
                await i.channel.delete()
                await new_ch.edit(position=pos)
                await new_ch.send("☢️ **Channel Nuked successfully.**")
        
        await itxn.response.send_message("⚠️ This will wipe all messages. Confirm?", view=NukeConfirm(), ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
