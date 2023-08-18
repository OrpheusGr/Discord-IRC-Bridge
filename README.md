# Discord-IRC-Bridge
A multi-channel  IRC <-> Discord Bridge. Each Discord user of a chosen channel gets a unique IRC client. IRC messages are sent through a webhook, making them look almost like real Discord Users (with a bot tag).  
To run this you'll need to have a clone exception set up on your IRCd's config or one to be requested from the IRC network's opers, as most networks allow 3 clones from the same IP. 

## Requirements
A minimum of Python 3.9
Note: Lower versions down to 3.7 will probably run the bot but might limit it. 
discord.py version defaults to <2.0 if the Python version is 3.8 or lower.
Some feats on this bot need 2.0+

## Installation

(See the [Wiki](https://github.com/OrpheusGr/Discord-IRC-Bridge/wiki) for more details)

Install the following python libraries using pip:

- irc
- discord.py 
- discord-webhook

Clone/Download this repository and do 'python3 setupwizard.py' to create a config file.

Add a new application and bot user to your Discord account, (on the Discord Developer Portal https://discord.com/developers/applications) then invite your bot to a server you manage:

https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID&scope=bot&permissions=3072  
(change CLIENT_ID to your application's client_id)

**For all the feats of the bot to work you'll need to enable all the Intents in the Bot page of your Application**.

## Features

- You can set up multiple channel sets that will ne relayed.
  - e.g #foo to be bridged with Discord channel 292838383893930 (Discord channel ID)
  - and #python to be bridged with Discord channel 404949399393939
  - you can do this for as many channel combinations as you need 
  - you may edit/add/delete channel sets using the setupwizard.py (once you're done you need to restart the bot for the changes to take effect)
- Uses webhooks to spoof IRC nicks as Discord "users" (bot tag next to their name, all webhooks have it)
- Makes an IRC client for a Discord user upon their request (use !joinirc in the relayed Discord channel.) Or automatically when they send a Discord message. You can choose between a command or auto connecting when you run the setupwizard.py
- Bot ops for both IRC and Discord that can use moderation/maintainance commands.
- The bot picks up on Discord user's status changes and sets them as their AWAY status on IRC (provided they have an IRC client connected)
- IRC users can mention Discord users just by typing the nick of their IRC client.
- Auto Disconnecting of IRC clients after a time limit that you can set. (can be disabled)
- The IRC clients that are created are saved and will reconnect if you restart the bot.
- IRC color codes such as bold and italics are converted to Discord equivalents and vice versa.
- The following commands are provided:
  - !kill command to disconnect someone's client (only for botops)
  - Change your IRC client's nick with !nick (can be disabled)
  - !fjoinirc make an IRC client for another Discord user (only for botops)
  - !fnick change a Discord user's IRC nick (only for botops)
  - !whois shows another Discord user's IRC nick (only for botops)
  - !whoami shows the sender's IRC nick
  - !bridgeshutdown to kill the bot. (only for botops) (works on IRC too)
  - !bridgehelp for usage of any of the above commands


## Setting up and running 
- Before starting the bot you need to `python3 setupwizard.py` to make a config file for the bot.
- When you're done with the setup wizard, launch the bot using `python3 main.py`.
- You may also use the setup wizard to edit any of the values in the future. (It will ask if you want to make a new config and when you say no it will ask if you want to edit the values) Remember to restart the bot for the new settings to be loaded.
- When new settings are added with updates they will be added to your config with default values, when you pull the update and start the bot. You can then use the setupwizard to edit those values.

## License

Feel free to fork this repo copy/borrow stuff for your own projects but provide a link to this as credit!


## Credits

Some of the Discord side code, as well as the skeleton of main.py originates from [this](https://github.com/milandamen/Discord-IRC-Python) repo which i originally forked and "developed" into a... junky mess of code that kinda worked.
When the mess became too much, turning a Relay into a client-making-machine Bridge was impossible, so i had to start over...
main.py is the same script with some changes (mostly to filenames)
The on_ready event in discordc.py is the same only with some variable names changed.
I used the same IRC library and spent a few days trying to use its Reactor class to make clients at will.
