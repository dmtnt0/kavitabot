"""
Appl Name: KavitaBot
Version: v0.1.1
Status: Development
Description: A Discord bot that uses Kavita API to allow for self generated email invites.
License: MIT License
Created: 02 March 2025
Copyright: Copyright (c) 2025
"""

import os
import re
import discord
from discord.ext import commands
from discord import app_commands
import discord.ext
import discord.ext.commands
from kavita import KavitaAPI

# Environment Variables
if os.environ.get("DISCORD_ROLE_ID"):
    role_id = os.environ.get("DISCORD_ROLE_ID")
else:
    role_id = 0
if os.environ.get("DISCORD_CHAN_ID"):
    chan_id = os.environ.get("DISCORD_CHAN_ID")
else:
    chan_id = 0

# Discord - KavitaBot - "Intents" Variables
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

bot = discord.ext.commands.Bot(command_prefix="!", intents=intents)
discord.ext.commands.Bot
# Discord - KavitaBot - Initialize Variables
GUILD_ID = discord.Object(id=os.environ.get("DISCORD_SVR_ID"))


@bot.event
async def on_ready():
    print(f'KavitaBot: Logged on as {bot.user}!')
    try:
        guild = discord.Object(id=os.environ.get("DISCORD_SVR_ID"))
        synced = await bot.tree.sync(guild=guild)
        print(f'KavitaBot: Synced {len(synced)} commands to guild {guild.id}')
        
    except Exception as e:
        print(f'Error syncing commands: {e}')


# Discord - KavitaBot - Initialize Items For Slash Commands
@bot.tree.command(name="invite", description='Invitation email to the eBook server', guild=GUILD_ID)
async def invite(ctx: discord.Interaction, email: str):
    
    # Perform check for required user role
    if role_id == 0:
            has_role = True
    else:
        for role in ctx.user.roles:
            if role_id:
                if role.id == int(role_id):
                    has_role = True
                else:
                    has_role = False
            else:
                has_role = False

    if has_role or role_id == 0:

        if ctx.channel_id == int(chan_id) or chan_id == 0:
            
            if re.match(r"^\w+\@\w+\..*", email):

                invite_url = KavitaAPI.invite(os.environ.get("KAVITA_OPDS_URL"),email)

                try:
                    # Send the DM
                    await ctx.user.send("Invitation email sent to: " + email + "\n\n**Registration URL: **" + invite_url)
                    await ctx.response.send_message("ok", ephemeral=True, silent=True, delete_after=0)

                except (IndexError, ValueError):
                    await ctx.response.send_message("Invalid user ID format. Use !dm <user_id>", ephemeral=True)
                except discord.NotFound:
                    await ctx.response.send_message("User not found.", ephemeral=True)
                except discord.Forbidden:
                    await ctx.response.send_message("Bot cannot DM this user.", ephemeral=True)
                except Exception as e:
                    await ctx.response.send_message(f"An error occurred: {e}", ephemeral=True)

            else:
                await ctx.response.send_message("**[ERROR]** Invalid email address!\n**[INFO]** Please check your email and try again.", ephemeral=True)
        else:
            await ctx.response.send_message("**[ERROR]** This bot only accepts commands in a specific channel.", ephemeral=True)
    else:
        await ctx.response.send_message("**[ERROR]** You do not have the required role.", ephemeral=True)


# Discord - KavitaBot - Run command
bot.run(os.environ.get("DISCORD_BOT_TKN"))

