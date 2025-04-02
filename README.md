# **KavitaBot**
## **Repository overview**

Project KavitaBot: This project was born from Kavita not having any type of real SSO option. I needed a way for my Discord users to generate their own invites, and so KavitaBot was created! Currently it only accepts the /invite command, however I am planning to work on command groups and further integration with the Kavita API to enable new features.

## **Environment Variables:**
- KAVITA_OPDS_URL – The full OPDS URL from and account in your Kavita with appropriate priveleges.
- DISCORD_BOT_TKN – The token of your discord bot.
- DISCORD_SVR_ID – The ID of your Discord server to enable forced sync update.
- DISCORD_CHAN_ID – The channel ID where you want the bot to accept commands.
- DISCORD_ROLE_ID – The user role ID you want to be required to use the bot.

## **Bot Notes:**
- The server ID requirement is to force an update in the event the bot is updated with new commands or .
- Commands can be used by anyone and in any channel, however the bot will give an error message if the user doesn't have the specified role or makes a request from a non-specified channel.
- Emails entered are checked for general formatting. This consists of looking for an ' @ ' followed by a ' . ' In preactice it's looking for something like `username@domain.com` however something like `example.username@sub.domain.com` will also work.
- Role restrictions check will happen _before_ the channel check.
- Channel restrictions are checked only if role ID check passes or role ID is not present.
- If Role & Channel checks pass the bot will be check the submitted email against Kavita to see if the user has an account and whether it's active or pending. It will respond differently for each event.
- All messages can only be seen by the user that is making the request.

 ## **Bot Responses:**
 NOTE: `<newline>` denotes a carriage return
 - Request > No Role > Wrong Channel: "**[ERROR]** You do not have the required role."
 - Request > No Role > Correct Channel: "**[ERROR]** You do not have the required role."
 - Request > Has Role > Wrong Channel: "**[ERROR]** This bot only accepts commands in a specific channel."
 - Request > Has Role > Correct Channel: *\<dm is sent to user\>* - "Invitation email sent to: `<user email>`" `<newline>x2` "**Registration URL:** `<Kavita invite URL>`"
 - Request > Has Role > Correct Channel > Invalid Email Address: "**[ERROR]** Invalid email address!" *\<newline\>* "**[INFO]** Please check your email and try again."
 - Request > Has Kavita Account > Pending: "Your account exists and is pending activation. Please check your DMs or email for the activation link."
 - Request > Has Kavita Account > Active: "Your account exists and is activate.\nTo access navigate to: {invite url}\nThis message will self destruct in 5 minutes."
 - Request > User ID is invalid: "Invalid user ID format. Use !dm <user_id>"
 - Request > User doesn't exist: "User not found."
 - Request > Bot Cannot DM User: "Bot cannot DM this user."
 - Request > General Error: "An error occurred: {literal error message}"
