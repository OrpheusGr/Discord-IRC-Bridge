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
