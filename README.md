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
- !kill command to disconnect someone's client (only for botops)
- Change your client's nick with !nick (can be disabled)
- IRC users can mention Discord users just by typing the nick of their client.
- !shutdown to kill the bot. (only for botops)
- Auto Disconnecting of IRC clients after a time limit that you can set. (can be disabled)
- !fjoinirc make a client for another user (only for botops)
- !fnick change a user's IRC nick (only for botops)
- !whois shows another user's IRC nick (only for botops)
- !whoami shows the sender's IRC nick

## Latest updates
June 29th 2023
- Bugs fixed
- Added a function that splits long messages into appropriate pieces. (IRC has a limit of 512 characters per line sent to the server)
- When a Discord user replies to a Discord message, if the sender of the original message is a Discord user and has an IRC client through the relay, their client's nick will be shown (their Discord username was shown previously.) This is done for clarity of the IRC users, as they only see the IRC nicks and not the Discord usernames.  

June 25-27th 2023
- Bug fixes, improvements
- When new settings are added with updates they will be added with default values, when you pull the updates and start the bot. You can then use the setupwizard to edit those values.  

June 24th 2023
- Hot fix for a June 22 bug
- use of !nick is now independent from AUTOCLIENTS and has its own True/False setting when wizard is ra
- misc improvements  



For less recent updates see changelog.md

## Running and setting up details
- Before starting the bot you need to `python3 setupwizard.py` to make a config file for the bot.
- When you're done with the setup wizard, launch the bot using `python3 main.py`.
- You may also use the setup wizard to edit some of the values in the future. (It will ask if you want to make a new config and when you say no it will ask if you want to edit the values) Remember to restart the bot for the new settings to be loaded.
- When new settings are added with updates they will be added to your config with default values, when you pull the update and start the bot. You can then use the setupwizard to edit those values.

## License

Feel free to fork this repo copy/borrow stuff for your own projects but provide a link to this as credit!
