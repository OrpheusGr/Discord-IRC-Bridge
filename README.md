# Discord-IRC-Bridge
- A multi-channel IRC <-> Discord Bridge. 
- Each Discord user can make a unique IRC client, it will connect to the IRC server and relay that user's messages. 
- Messages from IRC are sent to Discord through a webhook, making them look almost like real Discord Users (with a bot tag).  
- NOTE: To run this you'll need to have a clone exception set up on your IRCd's config or one to be requested from the IRC network's opers, as most networks allow 3 clones from the same IP. 

## Requirements
- A minimum of Python 3.9

- Install the following python libraries using pip:

  - [irc](https://pypi.org/project/irc/)
  - [discord.py](https://pypi.org/project/discord.py/)
  - [discord-webhook](https://pypi.org/project/discord-webhook/)

- Note: Lower versions down to 3.7 will probably run the bot but might limit it. 
discord.py version defaults to <2.0 if the Python version is 3.8 or lower.
Some feats on this bot need 2.0+

## Installation & Discord Bot Creation

(See the [Wiki](https://github.com/OrpheusGr/Discord-IRC-Bridge/wiki) for more details)

- Clone/Download this repository and do 'python3 setupwizard.py' to create a config file.

- Add a new application and bot user to your Discord account, (on the [Discord Developer Portal](https://discord.com/developers/applications)) then invite your bot to a server you manage:

https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID&scope=bot&permissions=3072  

- (change CLIENT_ID to your application's client_id)

**For all the feats of the bot to work you'll need to enable all the Intents in the Bot page of your Discord Bot  Application**.

## Features

- You can set up multiple channel sets that will be relayed.
  - e.g #foo to be bridged with Discord channel 292838383893930 (Discord channel ID)
  - and #python to be bridged with Discord channel 404949399393939
  - you can do this for as many channel combinations as you need 
  - you may edit/add/delete channel sets using the setupwizard.py (once you're done you need to restart the bot for the changes to take effect.)
- Uses webhooks to spoof IRC nicks as Discord "users" (bot tag next to their name, all webhooks have it.)
- SSL connection option
- Makes an IRC client for a Discord user upon their request (use !joinirc in the relayed Discord channel.) Or automatically when they send a Discord message. You can choose between a command or auto connecting when you run the setupwizard.py
- NickServ identification for the main bot or all the IRC clients (most networks have a limit of nicks that can identify to an account at the same time.)
- Bot ops for both IRC and Discord that can use moderation/maintainance commands.
- The bot picks up on Discord user's status changes and sets them as their AWAY status on IRC (provided they have an IRC client connected)
- IRC users can mention Discord users just by typing the nick of their IRC client.
- Auto Disconnecting of IRC clients after a time limit that you can set. (can be disabled)
- The IRC clients that are created are saved and will reconnect if you restart the bot.
- IRC color codes such as bold and italics are converted to Discord equivalents and vice versa.
- The following commands are provided:
  - !kill command to disconnect someone's client (only for botops)
  - !nick to change your IRC client's nick (can be disabled)
  - !fjoinirc make an IRC client for another Discord user (only for botops)
  - !fnick change a Discord user's IRC nick (only for botops)
  - !whois shows another Discord user's IRC nick (only for botops)
  - !whoami shows the Discord sender's IRC nick
  - !bridgeshutdown to kill the bot. (only for botops) (works on IRC too)
  - !bridgehelp for usage of any of the above commands
  - !leaveirc Disconnects the Discord User's IRC client
  - !leavechan Discord User's IRC client leaves the matching IRC channel

## Stuff that will be added at some point when i'm less busy

- DM !config command to edit values of the config without needing to restart the bot (with some exceptions such as  changing IRC or Discord servers)
- More ideas that i'm forgetting right now.

## Setting up and running 
- Before starting the bot you need to `python3 setupwizard.py` to make a config file for the bot.
- When you're done with the setup wizard, launch the bot using `python3 main.py`.
- You may also use the setup wizard to edit any of the values in the future. (It will ask if you want to make a new config and when you say no it will ask if you want to edit the values) Remember to restart the bot for the new settings to be loaded.
- When new settings are added with updates they will be added to your config with default values when you can run the setupwizard, which you can also use to edit those values.

## For any suggestions, questions or to say hi!
- Come chat with me/us on IRC at IrCQchat #Discord-IRC-Bridge . Through the [webclient](http://icqchat.us/)
- Or through your IRC client: icqchwt.us: 6667 #Discord-IRC-Bridge

## License

Feel free to fork this repo copy/borrow stuff for your own projects but provide a link to this as credit!


## Credits

Some of the Discord side code, as well as the skeleton of main.py originates from [this](https://github.com/milandamen/Discord-IRC-Python) repo which i originally forked and "developed" into a... junky mess of code that kinda worked.
When the mess became too much, turning a Relay into a client-making-machine Bridge was impossible, so i had to start over...
main.py is the same script with some changes (mostly to filenames)
The on_ready event in discordc.py is the same only with some variable names changed.
I used the same IRC library and spent a few days trying to use its Reactor class to make clients at will.
