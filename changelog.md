# June 14th 2023
- Added a setup wizard that makes or edits a config
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
