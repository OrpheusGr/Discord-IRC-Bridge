# Discord-IRC-Bridge
An IRC <-> Discord Bridge. Each Discord user of a chosen channel gets a unique IRC client. IRC messages are sent through a webhook, making them look almost like real Discord Users (with a bot tag). To run this you'll need to have a clone exception set up on your IRCd's config or one to be requested from the IRC network's opers. 

## Requirements
A minimum of Python 3.5

## Installation
Install the following python libraries using pip:

- irc
- discord.py
- discord-webhook

Clone/Download this repository and do 'python3 setupwizard.py' to create a config file.

Add a new application and bot user to your Discord account, (on the Discord Developer Portal https://discord.com/developers/applications) then invite your bot to a server you manage:

https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID&scope=bot&permissions=3072  
(change CLIENT_ID to your application's client_id)

The token can also be found in the Discord Developer Portal

## Features

- Uses webhooks to spoof IRC nicks as Discord "users" (bot tag next to their name, all webhooks have it)
- Makes an IRC client for a Discord user upon their request (use !joinirc in the relayed Discord channel.) Or automatically when they send a Discord message. You can choose between a command or auto connecting when you run the setupwizard.py
- Bot ops for both IRC and Discord that can use moderation/maintainance commands.
- The following commands work on Discord:
  - !kill command to disconnect someone's client (only for botops)
  - Change your IRC client's nick with !nick (can be disabled)
  - IRC users can mention Discord users just by typing the nick of their client.
  - Auto Disconnecting of IRC clients after a time limit that you can set. (can be disabled)
  - !fjoinirc make an IRC client for another Discord user (only for botops)
  - !fnick change a Discord user's IRC nick (only for botops)
  - !whois shows another Discord user's IRC nick (only for botops)
  - !whoami shows the sender's IRC nick
  - !shutdown to kill the bot. (only for botops) (works on IRC too)  

## Latest updates
July 9th 2023
- Fixed crashing bug (hopefully) The msg_split function was causing an infinite loop which eventually killed the bot/timedout the connections  

June 29th 2023
- Bugs fixed
- Added a function that splits long messages into appropriate pieces. (IRC has a limit of 512 characters per line sent to the server)
- When a Discord user replies to a Discord message, if the sender of the original message is a Discord user and has an IRC client through the relay, their client's nick will be shown (their Discord username was shown previously.) This is done for clarity of the IRC users, as they only see the IRC nicks and not the Discord usernames.  

For less recent updates see changelog.md

## Running and setting up details
- Before starting the bot you need to `python3 setupwizard.py` to make a config file for the bot.
- When you're done with the setup wizard, launch the bot using `python3 main.py`.
- You may also use the setup wizard to edit some of the values in the future. (It will ask if you want to make a new config and when you say no it will ask if you want to edit the values) Remember to restart the bot for the new settings to be loaded.
- When new settings are added with updates they will be added to your config with default values, when you pull the update and start the bot. You can then use the setupwizard to edit those values.

## License

Feel free to fork this repo copy/borrow stuff for your own projects but provide a link to this as credit!
