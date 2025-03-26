"""
MIT License

Copyright (c) 2025 DMTNT.CO

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

App Name: KavitaBot
Version: v0.2.0
Status: Development
Description: A Discord bot that uses Kavita API to allow for self generated email invites.
Created: 02 March 2025
Updated: 26 March 2025
"""
import os
import re
import discord
from discord.ext import commands
from discord import app_commands
import discord.ext
import discord.ext.commands
from urllib.parse import urlparse
from kavita import KavitaAPI

# Environment Variables
if os.environ.get("DISCORD_ROLE_ID"):
    role_id = os.environ.get("DISCORD_ROLE_ID")
else:
    role_id = False

if os.environ.get("DISCORD_CHAN_ID"):
    chan_id = os.environ.get("DISCORD_CHAN_ID")
else:
    chan_id = False

try:
    opds_url = os.environ.get("KAVITA_OPDS_URL")
except Exception as e:
    print(f'Error saving OPDS URL to variable: {e}')

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
    if role_id == False:
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

    if has_role:
        if chan_id == False:
            in_chan = True
        else:
            if chan_id:
                if ctx.channel_id == int(chan_id):
                    in_chan = True
                else:
                    in_chan = False
            else:
                in_chan = False

        if in_chan:
            if re.match(r"^\w+\@\w+\..*", email):

                user_list = KavitaAPI.users(opds_url)
                for obj in user_list:
                    if email == obj['email']:
                        user_exists = True
                        user_pending = obj['isPending']
                        parsed_url = urlparse(opds_url)
                        url = f"{parsed_url.scheme}://{parsed_url.netloc}"

                if user_exists and user_pending:
                    await ctx.response.send_message(f"Your account exists and is pending activation. Please check your DMs or email for the activation link.", ephemeral=True)
                elif user_exists and not user_pending:
                    await ctx.response.send_message(f"Your account exists and is activate.\nTo access navigate to: {url}\nThis message will self destruct in 5 minutes.", ephemeral=True)
                else:
                    invite_url = KavitaAPI.invite(opds_url,email)

                    try:
                        # Send the DM
                        await ctx.user.send(f"Invitation email sent to: " + email + "\n\n**Registration URL: **" + invite_url)
                        await ctx.response.send_message(f"Invite link sent via DM.\nThis message will autodelete in 30 seconds.", ephemeral=True, delete_after=30)

                    except (IndexError, ValueError):
                        await ctx.response.send_message(f"Invalid user ID format. Use !dm <user_id>", ephemeral=True)
                    except discord.NotFound:
                        await ctx.response.send_message(f"User not found.", ephemeral=True)
                    except discord.Forbidden:
                        await ctx.response.send_message(f"Bot cannot DM this user.", ephemeral=True)
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

