import discord
from discord import app_commands
from discord.ext import commands
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Bans a user")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, user: discord.User, reason: str = "No reason provided"):
        await interaction.guild.ban(user, reason=reason)
        embed = discord.Embed(title="User Banned", color=discord.Color.red())
        embed.add_field(name="User", value=user.mention)
        embed.add_field(name="Reason", value=reason)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="nuke", description="Deletes and recreates the channel (Requires Confirmation)")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def nuke(self, interaction: discord.Interaction):
        # Confirmation View
        class ConfirmNuke(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=15)
            
            @discord.ui.button(label="Confirm Nuke", style=discord.ButtonStyle.danger)
            async def confirm(self, inter: discord.Interaction, button: discord.ui.Button):
                pos = interaction.channel.position
                new_channel = await interaction.channel.clone(reason="Channel Nuked")
                await interaction.channel.delete()
                await new_channel.edit(position=pos)
                await new_channel.send(f"**Channel Nuked by {inter.user.mention}**", delete_after=10)

        await interaction.response.send_message("⚠️ Are you sure? This will delete all messages.", view=ConfirmNuke(), ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
