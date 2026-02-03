import discord
from discord import app_commands
from discord.ext import commands

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # Persistent

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.primary, custom_id="create_ticket")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        
        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            overwrites=overwrites,
            category=None # You can specify a category ID here
        )
        
        await interaction.response.send_message(f"Ticket created: {channel.mention}", ephemeral=True)
        
        embed = discord.Embed(title="Support Ticket", description="Staff will be with you shortly.", color=discord.Color.green())
        await channel.send(embed=embed, view=TicketControls())

class TicketControls(discord.ui.View):
    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.delete()

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ticket_setup")
    async def ticket_setup(self, interaction: discord.Interaction):
        embed = discord.Embed(title="AVRXT'S SPACE Support", description="Click the button below to open a ticket.")
        await interaction.channel.send(embed=embed, view=TicketView())
        await interaction.response.send_message("Setup complete.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Tickets(bot))
