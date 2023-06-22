help = {
    "listcommands": "!joinirc !leaveirc !nick !whoami !relayuptime !fjoinirc !kill !fnick !whois \n Use !relayhelp <command> for verbose info for a command. <parameter> means mandatory, [parameter] meams optional.",
    "!joinirc": "```!joinirc [--nick] [nickhere]``` All parameters are optional. \n If you use --nick amd you have a local nickname, it will be used as your IRC nick if suitable. \n The allowed characters areA-Z a-z 0-9 _^[]{}\-",
    "!leaveirc": "```!leaveirc [--delete] [quitmsg]``` All parameters are optional. \n If you use --delete your saved client will be deleted and won't be connected when the bot restarts. \n When you use this command, even if AUTOCLIENTS is True (clients created on message and not by !joinirc, you must use !joinirc to make a client. \n quitmsg is just a msg being sent when a client disconnects. (Some nets do not show these.)",
    "!nick": "```!nick <new_nick_here>``` Parameter is mandatory. Simply changes your nick to your desired new nick, if suitable",
    "!whoami": "This commamd takes no parameters. Simply shows what nick you are currently using on IRC",
    "!relayuptime": "This command takes no arguments. Simply shows for how long the bot has been running.",
    "!fjoinirc": "```!fjoinirc <@mention> [irc_nick_here] [--nick]``` Restricted to bot ops. Makes a client for another user. \n @mention is mandatory as it determines which user the client will be made for. \n If you provide a nick it will be used as their IRC nick. If --nick is used the user's local nick will be used, if they have one.",
    "!kill": "```!kill <@mention> [reason] [--delete]``` Restricted to bot ops. Disconnects another user's IRC client. @mention is mamdatory as it determines which user's client will be disconnected. reason is optional and will be put in the quit msg. If --delete is used the user's saved client will be deleted and won't be connected when the bot is restarted."
    "!fnick": "```!fnick <@mention> <new_nick>``` Restrictrd to bot ops. Changes another user's IRC nick. \n @mention is mandatory as it determines which user's IRC nick will be changed. new_nick is mandatory as it determines the users new IRC nick.",
    "!whois" "```!whois <@mention>``` Restricted to bot ops. Shows a user's IRC nick.  @mention is mandatory for obvious reasons."
    }
