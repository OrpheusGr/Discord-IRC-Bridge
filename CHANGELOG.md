# July 26 2023
- hotfix for a lil bug

# July 25 2023

- Added the relaying of message edits to IRC. 
  - When a Discord user that has an IRC client edits one of their Discord messages it will be shown on IRC as: ```EDIT: their post-edit message will be here```
- Improved the AWAY feature to check a User's status when their IRC client connects (instead of relying only on the time the user actually changes their status
  - Previously a user that was not online when the Bridge started up or when the Discord user created their IRC client, their AWAY message wouldn't be set on IRC as the bot only listened for status *changes*. Now when a client connects to IRC the Discord user's status is checked and set accordingly as their AWAY message. 
- Improved the connection of the saved clients when the bot starts
  - The dictionary containing the nessecary info will be made before the main bot connects to IRC.
  - That fixes a bug where double clients where created when a Discord user was sending messages during the bot was starting. 
  - The clients and connection objects are made as the bot connects to Discord, that way the bot doesn't try to make new objects, since there is already one for every Discord User with saved client.
  - Once the main bot is done connecting to IRC it loops through the objects and uses connect() on all of them.

# July 20th 2023

- When a Discord user changes their status from online to Idle, Dnd or offline, it will be set as their away message on IRC
  - When they go back online their away will be cleared
- Changed the alternative nicknames to be ```nickhere_[R]``` instead of ```nickhere[R]_```
- When the bot connects the saved IRC clients (during start up) it will no longer connect the IRC clients of users that are not in the Discord server. (removed/left/any reason)
- Fixed a bug in replacing IRC italics with Discord italics style.
- README updates, removed updates from README, added link to the Wiki, added Credits, raised minimum required Python version to 3.9 to support discord.py 2.0+ feats.

# July 9th 2023
- Fixed crashing bug (hopefully) The msg_split function was causing an infinite loop which eventually kills the bot

# June 29th 2023
- Bugs fixed
- Added a function that splits long messages into appropriate pieces. (IRC has a limit of 512 characters per line sent to the server.)
- When a Discord user replies to a Discord message, if the sender of the original message is a Discord user has an IRC client through the relay, their client's nick will be shown (their Discord username was shown previously.) This is done for clarity of the IRC users, as they only see the IRC nicks and not the Discord usernames.

# June 22nd 2023
- Some commands have been renamed for clarity:
  - !myircnick - New name: !whoami (same functionality)
  - !ircnick   - New name: !nick   (same functionality)
  - !usernick  - New name: !whois  (same functionality)
  - !fircnick  - New name: !fnick  (same functionality)
- New command - ```!leaveirc [--delete] [reason]``` Disconnects the user's client. (both parameters are opt
ional)
  - If --delete is used the saved client will be deleted and will not be rejoined when the bot restarts.
  - If AUTOCLIENTS is True and a user has left IRC, a client will not be made for them unless they use !joi
nirc
- !joinirc updated to use the user's saved nick (if a nick is not provided)
  - If the user doesn't have a saved nick, their username will be used (as it used to be)
  - If a nick is provided it will be saved.
  - Added an optional parameter --nick - If used, and the user has a local nick, it will be used on IRC
- --nick does the same in !fjoinirc
- Kill has been updated to accept a --delete parameter. If used it will delete the user's saved client.
- New command - ```!relayhelp <listcommands|command>``` Shows a list of available commamds or verbose info
for a command

# June 19th 2023
- Added 4 new commands
  - !fjoinirc - Makes a client for another user, used only by users in the botop list
  - !fircnick - Forcefully changes a user's nick, used only by users in the botop list, for moderation use
  - !usernick - Shows another user's nick, or their saved nick, only used by users in botop list
  - !myircnick - Shows the user's IRC nick, or their saved one, if there is one, when they don't have a connected client.
- Found and fixed a couple bugs

# June 14th 2023
- Added a setup wizard that makes or edits a config
- The clients that are made will be saved and reconnected when the bot is restarted
- The settings are now saved in a .pkl file and are not edited by hand
- Added !rehash command to reload the config if you make any changes
- Added 2 distinct modes of client creation. a) use of !joinirc command or b) automated client creation when a user sends a message.
- Added a time limit to disconnect clients for inactivity (no messages sent for X amount of time)

# June 3rd 2023
- Added botops list for Discord and IRC
- Added !kill command
- Added !ircnick command
- Added an unexpected disconnection message for the clients, that memtions the user that it belons to
- Added a 3 attempt reconnect for the main bot in the event of getting disconnected.
- Fixed a bug where the bot thought a user had a connected client, while it was not conected.
