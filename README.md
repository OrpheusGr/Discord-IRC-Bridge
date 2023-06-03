# DiscIRC-Relay
An IRC &lt;-> Discord Relay that creates a new IRC client for a Discord User upon their request and uses a Discord webhook to post IRC messages to Discord, faking a Discord user for better readability.

## Requirements
A minimum of Python 3.5

## Installation
Install the following python libraries using pip:

- irc
- discord.py
- discord-webhook

Clone/Download this repository and then make a copy of examplesettings.py as settings.py

Add a new application and bot user to your Discord account, (on the Discord Developer Portal https://discord.com/developers/applications)  then invite your bot to a server you manage:

https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID&scope=bot&permissions=3072  
(change CLIENT_ID to your application's client_id)

Fill in the info in your settings.py (Don't remove any quotes!)

The token can be found also in the Discord Developer Portal

## Features

- Uses webhooks to spoof IRC nicks as Discord "users"
- Makes an IRC client for a Discord user upon their request, use !joinirc in the relayed Discord channel.
- Bot ops for both IRC and Discord that can use moderation/maintainance commands.
- !kill command to disconnect someone's client
- Change your client's nick with !ircnick
- IRC users can mention Discord users just by typing the nick of their client.

Feature ideas:

- an option to make a client for everyone, instead of each user using a command
- an option to disconnect an IRC client when it doesn't send a msg for X amount of time

## Changelog
June 3rd 2023
- Added botops list for Discord and IRC
- Added !kill command
- Added !ircnick command
- Added an unexpected disconnection message for the clients, that memtions the user that it belons to
- Added a 3 attempt reconnect for the main bot in the event of getting disconnected.
- Fixed a bug where the bot thought a user had a connected client, while it was not conected.

## Running and setting up details
Just launch the bot using `python3 main.py`.

## License

Feel free to fork this repo copy/borrow stuff for your own projects but provide a link to this as credit!
