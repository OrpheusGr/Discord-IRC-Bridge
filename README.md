# DiscIRC-Relay
An IRC &lt;-> Discord Relay that creates a new IRC client for a Discord User upon their request and uses a Discord webhook to post IRC messages, faking a Discord user for better readability.

## Requirements
A minimum of Python 3.5

## Installation
Install the following python libraries using pip:

- irc
- discord.py

Clone/Download this repository and then make a copy of examplesettings.py as settings.py

Add a new application and bot user to your Discord account, (on the Discord Developer Portal https://discord.com/developers/applications)  then invite your bot to a server you manage:

https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID&scope=bot&permissions=3072  
(change CLIENT_ID to your application's client_id)

Fill in the info in your settings.py (Don't remove any quotes!)

The token can be found also in the Discord Developer Portal

## Features

- Uses webhooks to spoof IRC nicks as Discord "users"
- Makes an IRC client for a Discord user upon their request, use !joinirc in the relayed Discord channel.


## Running and setting up details
Just launch the bot using `python3 main.py`.
