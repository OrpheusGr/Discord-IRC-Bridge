import re
import os
import time
import pickle

myprint_count = 0
config = {}
newchannel_sets = {}

def myprint(stuff, erase=0):
    global myprint_count
    print(stuff)
    myprint_count += 1
    if erase == 1:
        for i in range(myprint_count-1):
            print("\033[F", end="")
            print("\033[K", end="")
        myprint_count = 1

def fixnick(nick):
    new_nick = re.sub(r'[^A-Za-z0-9 ^\[\]\\{}`_-]+', '', nick)
    if new_nick == "":
        return False
    else:
        return new_nick

def totype(of, to):
    r = ""
    if type(of) == int:
        try:
           r = int(to)
        except:
           r = ["non_same_type", "numeric"]
    elif type(of) == str:
        try:
           if of.isnumeric() == True and to.isnumeric() == False:
               r = ["non_same_type", "numeric"]
           else:
               if of.startswith("https://discord.com/api/webhooks/") == True and to.startswith("https://discord.com/api/webhooks/") == False:
                   return ["non_same_type", "starting with https://discord.com/api/webhooks/"]
               elif of[0] == "#" and to[1] != "#":
                   return "#" + to
               r = str(to)
        except:
           r = ["nom_same_type", "string"]
    elif type(of) == bool:
        if to == "False":
           r = False
        elif to == "True":
           r = True
        else:
           r = ""
    return r

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    OFF = '\033[0m'

def save_config():
    global config
    with open('config.pkl', 'wb') as fp:
        pickle.dump(config, fp)

def load_config():
    global config
    config = {}
    if os.path.getsize('config.pkl') > 0:
        with open('config.pkl', 'rb') as fp:
            config = pickle.load(fp)
    else:
        config = {}

def yninput():
    global myprint_count
    myprint_count += 1
    r = False
    x = input("y/n: ")
    if x.lower() == "y":
        r = True
    return r

if os.path.isfile("config.pkl") == False:
    open("config.pkl", 'w').close()

load_config()

x = True
print(bcolors.BOLD + bcolors.UNDERLINE + bcolors.OKGREEN + "*** Discord-IRC-Bridge Set Up Wizard ***" + bcolors.OFF)
if config != {}:
    print(" ")
    myprint(bcolors.WARNING + "You already have a saved config file. Do you want to make a new one?" + bcolors.OFF)
    x = yninput()
if x:
    config = {}
    myprint("", 1)
    time.sleep(1)
    myprint(bcolors.OKCYAN + "Let's go through the IRC settings.")
    myprint("Please input the host of the IRC server." + bcolors.OFF)
    IRCSERVER = input("IRC server host: ")
    srvsplit = IRCSERVER.split(".")
    while "." not in IRCSERVER or (len(srvsplit) == 2 and srvsplit[1] == ""):
        myprint("", 1)
        myprint(bcolors.WARNING + "The IRC host should be an IP or a domain name. Which consists of at least 1 .")
        myprint(bcolors.WARNING + "e.g irc.network or irc.network.here or 1.1.1.1 etc" + bcolors.OFF)
        IRCSERVER = input("IRC server host: ")
        srvsplit = IRCSERVER.split(".")
    config["IRCSERVER"] = IRCSERVER
    myprint(bcolors.OKGREEN + "The IRC server is set to: " + IRCSERVER + bcolors.OFF)
    time.sleep(2)
    myprint("", 1)
    myprint(bcolors.OKCYAN + "Now please input the IRC port. Leave empty for: default 6667" + bcolors.OFF)
    IRCPORT = input("IRC port: ")
    while IRCPORT.isnumeric() == False and IRCPORT != "":
        myprint("", 1)
        myprint(bcolors.WARNING + IRCPORT + "is not a numeric value. Please input a valid port" + bcolors.OFF)
        IRCPORT = input("IRC port: ")
    if IRCPORT == "":
        IRCPORT = "6667"
    IRCPORT = int(IRCPORT)
    myprint(bcolors.OKGREEN + "Port is set to " + str(IRCPORT) + bcolors.OFF)
    config["IRCPORT"] = IRCPORT
    time.sleep(2)
    myprint("", 1)
    time.sleep(2)
    myprint(bcolors.OKCYAN + "Next, input the bot's nick! (default: Bridge) Accepted characters: A-Z a-z 0-9 ^\[\]\\{}`_-]" + bcolors.OFF)
    IRCNICK = input()
    FIXEDIRCNICK = fixnick(IRCNICK)
    check = 1
    while check or FIXEDIRCNICK == False:
        if IRCNICK == "":
            IRCNICK = "Bridge"
            check = 0
            FIXEDIRCNICK = "A"
        if FIXEDIRCNICK == False:
            myprint("", 0)
            myprint(bcolors.FAIL + "The nick you gave me cannot be used, please input a valid nick A-Z a-z 0-9 ^\[\]\\{}`_-]" + bcolors.OFF)
            FIXEDIRCNICK = fixnick(input())
        else:
            IRCNICK = FIXEDIRCNICK
            myprint(bcolors.OKGREEN + "The Bot's IRC nick is set to " + IRCNICK + bcolors.OFF)
            check = 0
    config["IRCNICK"] = IRCNICK
    time.sleep(2)
    myprint("", 1)
    myprint(bcolors.OKCYAN + "Now we need to write a list of IRC nicks that will use the bot's moderation commands")
    myprint("Just type the nicks seperated by spaces (e.g Nick John Mary)" + bcolors.OFF)
    IRCBOTOPS = input("IRC bot operators: ")
    myprint(bcolors.OKGREEN + "IRC bot ops list set to: " + IRCBOTOPS + bcolors.OFF)
    config["IRCBOTOPS"] = IRCBOTOPS
    time.sleep(2)
    myprint("", 1)
    myprint(bcolors.OKCYAN + "Now to Discord! Please input the ID of the Discord server/guild that you've invited it to")
    myprint("It is a numerical ID, enable developer mode in Discord settings and copy the ID on the server's options" + bcolors.OFF)
    DISCORDSERVER = input("Discord Server ID (numeric): ")
    while DISCORDSERVER.isnumeric() == False:
        myprint("", 1)
        myprint(bcolors.WARNING + "That is not a numerical value! Please try again!" + bcolors.OFF)
        DISCORDSERVER = input("Discord server ID: ")
    config["DISCORDSERVER"] = DISCORDSERVER
    myprint(bcolors.OKGREEN + "Alright! The Discord server ID is set to " + DISCORDSERVER + bcolors.OFF)
    time.sleep(2)
    myprint("", 1)
    myprint(bcolors.OKCYAN + "Next we'll need the bot's token, you'll find it im the Discord Developer board")
    myprint("It should be an alphanumerical value" + bcolors.OFF)
    TOKEN = input("App/Bot token: ")
    config["TOKEN"] = TOKEN
    myprint(bcolors.OKGREEN + "Bot token is set to: " + TOKEN + bcolors.OFF)
    time.sleep(2)
    myprint("", 1)
    myprint(bcolors.OKCYAN + "Now we need to set a list of Discord bot ops, just like IRC, but instead of nicks...")
    myprint("You'll have to input their User IDs, which you can copy from eacha user's profile")
    myprint("Developer mode needs to be on for this as well" + bcolors.OFF)
    DISCORDBOTOPS = input("Discord Bot operators' ID'S: ")
    config["DISCORDBOTOPS"] = DISCORDBOTOPS
    myprint(bcolors.OKGREEN + "The list of Discord Bot Ops is set to: " + DISCORDBOTOPS + bcolors.OFF)
    time.sleep(2)
    myprint("", 1)
    myprint(bcolors.OKCYAN + "How much time, in seconds, should pass before a Discord user can rejoin IRC after a Discord Bot Op uses !kill  If you leave it empty or set it to 0, kills will be permanent" + bcolors.OFF)
    day = 3600 * 24
    tendays = day * 10
    myprint("Quick examples: 30 minutes: 1800 | 1 hour: 3600 | 1 day: " + str(day) + " | 10 days: " + str(tendays))
    TIMEKILLED = input("Time value: ")
    while TIMEKILLED.isnumeric() == False and TIMEKILLED != "":
        myprint("", 0)
        myprint(bcolors.WARNING + "This value should be numeric. Pick a number, any number! ...Wait i'm a wizard not a magician :D" + bcolors.OFF)
        TIMEKILLED = input()
    if TIMEKILLED == "":
        TIMEKILLED = "0"
    TIMEKILLED = int(TIMEKILLED)
    config["TIMEKILLED"] = TIMEKILLED
    myprint(bcolors.OKGREEN + "Kill time is set to: " + str(TIMEKILLED) + bcolors.OFF)
    time.sleep(2)
    myprint("", 1)
    myprint(bcolors.OKCYAN + "After how many seconds of inactivity should IRC clients be discconnected? Set to 0 or leave empty to keep this disabled." + bcolors.OFF)
    INACTIVITY = input()
    while INACTIVITY.isnumeric() == False and INACTIVITY != "":
        myprint("", 0)
        myprint(bcolors.WARNING + "This should also be a numerical value. Just numbers!" + bcolors.OFF)
        INACTIVITY = input()
    if INACTIVITY == "":
        INACTIVITY = "0"
    config["INACTIVITY"] = int(INACTIVITY)
    myprint(bcolors.OKGREEN + "Inactivity disconnection is set to: " + str(INACTIVITY) + " seconds." + bcolors.OFF)
    time.sleep(2)
    myprint("", 1)
    myprint("Should clients be created with a command by each user or automatically when a user sends a message? (y/n) y = command n = automatically")
    AUTOCLIENTS = yninput()
    if AUTOCLIENTS == False:
        config["AUTOCLIENTS"] = False
        myprint(bcolors.OKGREEN + "Clients will connect automatically when a user sends a message" + bcolors.OFF)
    else:
        config["AUTOCLIENTS"] = True
        myprint(bcolors.OKGREEN + "Clients will connect when a user uses the !joinirc command" + bcolors.OFF)
    time.sleep(2)
    myprint("", 1)
    myprint(bcolors.OKCYAN + "Should Discord users be allowed to use !nick to change their client's nick on IRC? y/n" + bcolors.OFF)
    NICKCHANGE = yninput()
    myprint(bcolors.OKGREEN + "Use of !nick command is set to: " + str(NICKCHANGE) + bcolors.OFF)
    myprint("", 1)
    myprint(bcolors.OKCYAN + "Lastly we need to set up the channels that will be relayed.")
    config["channel_sets"] = {}
    time.sleep(1.5)
    myprint("We need a Discord channel id, a Discord webhook that is set to work in the channel,")
    myprint(" and an IRC channel name. Let's call that a channel set.")
    time.sleep(1)
    myprint("You can set up more than one channel set! Just don't put the same channels in different sets!")
    time.sleep(2.5)
    myprint("-")
    myprint("Let's start with the Discord channel ID.")
    myprint("It should be a numerical value." + bcolors.OFF)
    setup_channels = True
    while setup_channels == True:
        discordchan = input("A Discord channel's ID: ")
        while discordchan.isnumeric() == False:
            myprint("", 1)
            myprint(bcolors.WARNING + discordchan + " is not a numeric value! You can find a Discord channel's ID in its info tab!")
            myprint("(Provided that you have enabled Developer mode!)" +  bcolors.OFF)
            discordchan = input("A Discord channel's ID: ")
        time.sleep(1)
        myprint("", 1)
        myprint(bcolors.OKCYAN + "Ok cool! Let's continue with the Webhook link!")
        myprint("You can find/create a webhook for the channel you just input in the Discord's Server settings." + bcolors.OFF)
        webhook = input("webhook: ")
        while webhook.startswith("https://discord.com/api/webhooks/") == False:
            myprint("", 1)
            myprint(bcolors.WARNING + "A Discord webhook URL should start with 'https://discord.com/api/webhooks/'" + bcolors.OFF)
            webhook = input("webhook: ")
        myprint("", 1)
        myprint(bcolors.OKCYAN + "Ok and now we just need the IRC channel name for this channel set." + bcolors.OFF)
        irc_chan = input("IRC channel: ")
        if irc_chan[0] != "#":
            irc_chan = "#" + irc_chan
        config["channel_sets"][discordchan] = {"webhook": webhook, "irc_chan": irc_chan}
        myprint("", 0)
        myprint(bcolors.OKGREEN + "We've set up the Discord channel with id " + discordchan + " to be relayed to " + irc_chan + " and vice versa. The webhook that will be used is " + webhook + bcolors.OFF)
        myprint(discordchan + " <-> " +  irc_chan)
        time.sleep(1.5)
        myprint(" ")
        myprint("Do you want to set up more channel sets?")
        setup_channels = yninput()
    save_config()
    myprint("This Wizard has reached its end! Here are all your settings!")
    time.sleep(2)
    paste = ""
    for item in config:
        value = config[item]
        line = item + ": " + str(value)
        myprint(line)
        myprint("-")
else:
    myprint("", 1)
    myprint("Do you want to edit any values in the config? y/n")
    x = yninput()
    if x:
        myprint("", 1)
        myprint("I will cycle through each item and ask you if you want to edit it!")
        for i in config:
            myprint("", 1)
            item = i
            if item != "channel_sets":
                value = config[i]
                myprint(item + " = " + str(value))
                myprint("Do you want to edit this value? (y/n)")
                x = yninput()
                if x:
                    myprint("Please input the new value, if you didn't want to edit it, just press Enter")
                    x = input()
                    y = totype(value, x)
                    while type(y) == list and y[0] == "non_same_type":
                        myprint("This is not an acceptable value for this setting. It should be", y[1])
                        myprint(item + " = " + str(value))
                        y = totype(value, input())
                    x = y
                    if x != "":
                        config[item] = x
                    myprint(item + " = " + str(config[item]))
        myprint("", 1)
        myprint("Do you want to edit any of the channel sets?")
        x = yninput()
        if x:
            for channelset in config["channel_sets"]:
                newchannel_sets[channelset] = config["channel_sets"][channelset]
                myprint("", 1)
                myprint("Do you want to edit this channel set?")
                myprint("'" + channelset + "': " + str(config["channel_sets"][channelset]))
                x = yninput()
                if x == True:
                    xconfirm = False
                    myprint("Do you want to delete this channel set entirely?")
                    x = yninput()
                    if x:
                        myprint(bcolors.BOLD + bcolors.WARNING + "Are you sure you want to " + bcolors.UNDERLINE + "delete" + bcolors.OFF + bcolors.BOLD + bcolors.WARNING +  " this channel set?" + bcolors.OFF)
                        xconfirm = yninput()
                    if xconfirm:
                        newchannel_sets.pop(channelset)
                        myprint(channelset + " channel set has been deleted.")
                    else:
                        myprint("Do you want to edit the Discord channel ID? " + channelset)
                        x = yninput()
                        newchannelset = channelset
                        if x:
                            myprint("Please input the new channel ID.")
                            discordchan = input("Discord channel ID: ")
                            y = totype(channelset, discordchan)
                            while type(y) == list and y[0] == "non_same_type":
                                myprint("This is not an acceptable value for this setting. It should be " + y[1])
                                myprint(channelset + "=" + str(value))
                                y = totype(value, input())
                            x = y
                            if x != "":
                                print("id change")
                                previouslyvalue = config["channel_sets"][channelset]
                                newchannel_sets.pop(channelset)
                                newchannel_sets[x] = previouslyvalue
                                myprint(x + " = " + str(previouslyvalue))
                                newchannelset = x
                        for subitem in config["channel_sets"][channelset]:
                            value = config["channel_sets"][channelset][subitem]
                            myprint("", 1)
                            myprint("Do you want to change the value of " + subitem + " ?")
                            myprint(subitem + " = " + str(value))
                            x = yninput()
                            if x:
                                x = input(subitem + ": ")
                                y = totype(value, x)
                                while type(y) == list and y[0] == "non_same_type":
                                    myprint("This is not an acceptable value for this setting. It should be " + y[1])
                                    myprint(subitem + " = " + str(value))
                                    y = totype(value, input())
                                x = y
                                if x != "":
                                    newchannel_sets[newchannelset][subitem] = x
                                    myprint(subitem + " = " + str(x))
            config["channel_sets"] = newchannel_sets
        myprint("Do you want to add new channel sets?")
        x = yninput()
        if x:
            setup_channels = True
            while setup_channels == True:
                discordchan = input("A Discord channel's ID: ")
                while discordchan.isnumeric() == False:
                    myprint("", 1)
                    myprint(bcolors.WARNING + discordchan + " is not a numeric value! You can find a Discord channel's ID in its info tab!")
                    myprint("(Provided that you have enabled Developer mode!)" +  bcolors.OFF)
                    discordchan = input("A Discord channel's ID: ")
                time.sleep(1)
                myprint("", 1)
                myprint(bcolors.OKCYAN + "Ok cool! Let's continue with the Webhook link!")
                myprint("You can find/create a webhook for the channel you just input in the Discord's Server settings." + bcolors.OFF)
                webhook = input("webhook: ")
                while webhook.startswith("https://discord.com/api/webhooks/") == False:
                    myprint("", 1)
                    myprint(bcolors.WARNING + "A Discord webhook URL should start with 'https://discord.com/api/webhooks/'" + bcolors.OFF)
                    webhook = input("webhook: ")
                myprint("", 1)
                myprint(bcolors.OKCYAN + "Ok and now we just need the IRC channel name for this channel set." + bcolors.OFF)
                irc_chan = input("IRC channel: ")
                if irc_chan[0] != "#":
                    irc_chan = "#" + irc_chan
                config["channel_sets"][discordchan] = {"webhook": webhook, "irc_chan": irc_chan}
                myprint("", 0)
                myprint(bcolors.OKGREEN + "We've set up the Discord channel with id " + discordchan + " to be relayed to " + irc_chan + " and vice versa. The webhook that will be used is " + webhook + bcolors.OFF)
                myprint(discordchan + " <-> " +  irc_chan)
                time.sleep(1.5)
                myprint(" ")
                myprint("Do you want to set up more channel sets?")
                setup_channels = yninput()
        myprint("", 1)
        save_config()
        time.sleep(1)
        myprint(config)
