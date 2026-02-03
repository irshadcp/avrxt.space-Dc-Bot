import discord
from discord import app_commands
from discord.ext import commands

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.blurple, custom_id="ticket_btn")
    async def ticket_btn(self, itxn: discord.Interaction, button: discord.ui.Button):
        guild = itxn.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            itxn.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True)
        }
        ch = await guild.create_text_channel(f"ticket-{itxn.user.name}", overwrites=overwrites)
        await itxn.response.send_message(f"Ticket opened at {ch.mention}", ephemeral=True)
        await ch.send(f"Welcome {itxn.user.mention}. Staff will be with you shortly.")

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ticket_setup", description="Post ticket embed")
    async def ticket_setup(self, itxn: discord.Interaction):
        embed = discord.Embed(title="Support", description="Click below to open a ticket")
        await itxn.channel.send(embed=embed, view=TicketView())
        await itxn.response.send_message("Setup done.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Tickets(bot))
