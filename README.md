# DiscIRC-Relay
An IRC &lt;-> Discord Relay that creates an IRC client for a Discord User and uses a Discord webhook to post IRC messages to Discord, faking a Discord user for better readability.

## Requirements
A minimum of Python 3.5

## Installation
Install the following python libraries using pip:

- irc
- discord.py
- discord-webhook

Clone/Download this repository and do 'python3 setupwizard.py' to create a config file.

Add a new application and bot user to your Discord account, (on the Discord Developer Portal https://discord.com/developers/applications)  then invite your bot to a server you manage:

https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID&scope=bot&permissions=3072  
(change CLIENT_ID to your application's client_id)

The token can also be found in the Discord Developer Portal

## Features

- Uses webhooks to spoof IRC nicks as Discord "users"
- Makes an IRC client for a Discord user upon their request (use !joinirc in the relayed Discord channel.) Or automatically when they send a Discord message. You can choose between a command or auto connecting when you run the setupwizard.py
- Bot ops for both IRC and Discord that can use moderation/maintainance commands.
- !kill command to disconnect someone's client
- Change your client's nick with !ircnick (if auto connecting is not enabled)
- IRC users can mention Discord users just by typing the nick of their client.
- !shutdown to kill the bot.
- Auto Disconnecting of IRC clients after a time limit that you can set.

## Latest updates
June 19th 2023
- Added 4 new commands
  - !fjoinirc - Makes a client for another user, used only by users in the botop list
  - !fircnick - Forcefully changes a user's nick, used only by users in the botop list, for moderation use
  - !usernick - Shows another user's nick, or their saved nick, only used by users in botop list
  - !myircnick - Shows the user's IRC nick, or their saved one, if there is one, when they don't have a connected client.
- Found and fixed a couple bugs
June 14th 2023
- Added a setup wizard that makes or edits a config
- The clients that are made will be saved and reconnected when the bot is restarted
- The settings are now saved in a .pkl file and are not edited by hand
- Added 2 distinct modes of client creation. a) use of !joinirc command or b) automated client creation when a user sends a message.
- Added a time limit to disconnect clients for inactivity (no messages sent for X amount of time)

For less recent updates see changelog.md

## Running and setting up details
- Before starting the bot you need to `python3 setupwizard.py` to make a config file for the bot.
- When you're done with the setup wizard, launch the bot using `python3 main.py`.
- You may also use the setup wizard to edit some of the values in the future. (It will ask if you want to make a new config and when you say no it will ask if you want to edit the values) Remember to restart the bot for the new settings to be loaded.

## License

Feel free to fork this repo copy/borrow stuff for your own projects but provide a link to this as credit!
