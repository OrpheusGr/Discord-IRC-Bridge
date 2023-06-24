import re
import os
import time
import pickle

def fixnick(nick):
    new_nick = re.sub(r'[\W_]', '', nick)
    if new_nick == "":
        return False
    else:
        return new_nick

def totype(of, to):
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
               r = str(to)
        except:
           r = ["nom_same_type", "string"]
    elif type(of) == bool:
        if to == "False":
           r = False
        elif to == "True":
           r = "True"
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
    r = False
    x = input()
    if x.lower() == "y":
        r = True
    return r

if os.path.isfile("config.pkl") == False:
    open("config.pkl", 'w').close()

load_config()

x = True
if config != {}:
    print(bcolors.HEADER + "You already have a saved config file. Do you want to make a new one?" + bcolors.OFF)
    x = yninput()
if x:
    config = {}
    print(bcolors.OKCYAN + "Let's go through the IRC settings.")
    print("Please input the host of the IRC server." + bcolors.OFF)
    IRCSERVER = input()
    srvsplit = IRCSERVER.split(".")
    while "." not in IRCSERVER or (len(srvsplit) == 2 and srvsplit[1] == ""):
        print(bcolors.WARNING + "The IRC host should be an IP or a domain name. Which consists of at least 1 .")
        print(bcolors.OKWARNING + "e.g irc.network or irc.network.here or 1.1.1.1 etc" + bcolors.OFF)
        IRCSERVER = input()
        srvsplit = IRCSERVER.split(".")
    config["IRCSERVER"] = IRCSERVER
    print(bcolors.OKGREEN + "The IRC server is set to:", IRCSERVER, bcolors.OFF)
    time.sleep(2)
    print("____________________________")
    print(bcolors.OKCYAN + "Now please input the IRC port. Leave empty for: default 6667", bcolors.OFF)
    IRCPORT = input()
    while IRCPORT.isnumeric() == False and IRCPORT != "":
        print(bcolors.WARNING, IRCPORT, "is not a numeric value. Please input a valid port" + bcolors.OFF)
        IRCPORT = input()
    if IRCPORT == "":
        IRCPORT = "6667"
    IRCPORT = int(IRCPORT)
    print(bcolors.OKGREEN + "Port is set to " + str(IRCPORT), bcolors.OFF)
    config["IRCPORT"] = IRCPORT
    time.sleep(2)
    print("____________________________")
    print(bcolors.OKCYAN + "Please input the IRC channel name that the bot will join" + bcolors.OFF)
    IRCCHAN = input()
    if IRCCHAN[0] != "#":
        IRCCHAN = "#" + IRCCHAN
    config["IRCCHAN"] = IRCCHAN
    print(bcolors.OKGREEN + "The IRC channel is set to:", IRCCHAN, bcolors.OFF)
    time.sleep(2)
    print("____________________________")
    print(bcolors.OKCYAN + "Next, input the bot's nick! (default: Relay) Accepted characters: A-Z a-z 0-9", bcolors.OFF)
    IRCNICK = input()
    FIXEDIRCNICK = fixnick(IRCNICK)
    check = 1
    while check or FIXEDIRCNICK == False:
        if IRCNICK == "":
            IRCNICK = "Relay"
            check = 0
            FIXEDIRCNICK = "A"
        if FIXEDIRCNICK == False:
            print(bcolors.FAIL + "The nick you gave me cannot be used, please input a valid nick A-Z a-z 0-9", bcolors.OFF)
            FIXEDIRCNICK = fixnick(input())
        else:
            IRCNICK = FIXEDIRCNICK
            print(bcolors.OKGREEN + "The Bot's IRC nick is set to", IRCNICK, bcolors.OFF)
            check = 0
    config["IRCNICK"] = IRCNICK
    time.sleep(2)
    print("____________________________")
    print(bcolors.OKCYAN + "Now we need to write a list of IRC nicks that will use the bot's moderation commands")
    print("Just type the nicks seperated by spaces (e.g Nick John Mary)", bcolors.OFF)
    IRCBOTOPS = input()
    print(bcolors.OKGREEN + "IRC bot ops list set to:", IRCBOTOPS, bcolors.OFF)
    config["IRCBOTOPS"] = IRCBOTOPS
    time.sleep(2)
    print("____________________________")
    print(bcolors.OKCYAN + "Now to Discord! Please input the ID of the Discord server/guild that you've invited it to")
    print("It is a numerical ID, enable developer mode in Discord settings and copy the ID on the server's options")
    DISCORDSERVER = input()
    while DISCORDSERVER.isnumeric() == False:
        print(bcolors.WARNING,"That is not a numerical value! Please try again!", bcolors.OFF)
        DISCORDSERVER = input()
    config["DISCORDSERVER"] = DISCORDSERVER
    print(bcolors.OKGREEN + "Alright! The Discord server ID is set to", DISCORDSERVER, bcolors.OFF)
    time.sleep(2)
    print("____________________________")
    print(bcolors.OKCYAN + "Next, we need the ID of the Discord channel.")
    print("Given that you have enabled Developer mode, you'll find the ID on the channel's info", bcolors.OFF)
    DISCORDCHAN = input()
    while DISCORDCHAN.isnumeric() == False:
        print(bcolors.WARNING + "The Channel ID should be a numerical value. Please try again!", bcolors.OFF)
        DISCORDCHAN = input()
    config["DISCORDCHAN"] = DISCORDCHAN
    print(bcolors.OKGREEN + "The Discord channel ID is set to", DISCORDCHAN, bcolors.OFF)
    time.sleep(2)
    print("____________________________")
    print(bcolors.OKCYAN + "Next we'll need the bot's token, you'll find it Discord Developer board")
    print("It should be an alphanumerical value" + bcolors.OFF)
    TOKEN = input()
    config["TOKEN"] = TOKEN
    print(bcolors.OKGREEN + "Bot token is set to:", TOKEN, bcolors.OFF)
    time.sleep(2)
    print("____________________________")
    print(bcolors.OKCYAN + "Now we need to set a list of Discord bot ops, just like IRC, but instead of nicks...")
    print("You'll have to input their User IDs, which you can copy from eacha user's profile")
    print("Developer mode needs to be on for this as well", bcolors.OFF)
    DISCORDBOTOPS = input()
    config["DISCORDBOTOPS"] = DISCORDBOTOPS
    print(bcolors.OKGREEN + "The list of Discord Bot Ops is set to:", DISCORDBOTOPS, bcolors.OFF)
    time.sleep(2)
    print("____________________________")
    print("How much time, in seconds, should pass before a Discord user can rejoin IRC after a Discord Bot Op uses !kill  If you leave it empty or set it to 0, kills will be permanent")
    day = 3600 * 24
    tendays = day * 10
    print("Quick examples: 30 minutes: 1800 | 1 hour: 3600 | 1 day:", day, "| 10 days", tendays)
    TIMEKILLED = input()
    while TIMEKILLED.isnumeric() == False and TIMEKILLED != "":
        print(bcolors.WARNING + "This value should be numeric. Pick a number, any number! ...Wait i'm a wizard not a magician :D", bcolors.OFF)
        TIMEKILLED = input()
    if TIMEKILLED == "":
        TIMEKILLED = "0"
    TIMEKILLED = int(TIMEKILLED)
    config["TIMEKILLED"] = TIMEKILLED
    print(bcolors.OKGREEN + "Kill time is set to:", TIMEKILLED, bcolors.OFF)
    time.sleep(2)
    print("____________________________")
    print(bcolors.OKCYAN + "After how many seconds of inactivity should IRC clients be discconnected? Set to 0 or leave empty to keep this disabled.", bcolors.OFF)
    INACTIVITY = input()
    while INACTIVITY.isnumeric() == False and INACTIVITY != "":
        print(bcolors.WARNING + "This should also be a numerical value. Just numbers!", bcolors.OFF)
        INACTIVITY = input()
    if INACTIVITY == "":
        INACTIVITY = "0"
    config["INACTIVITY"] = int(INACTIVITY)
    print(bcolors.OKGREEN + "Inactivity disconnection is set to: " + str(INACTIVITY) + " seconds.")
    time.sleep(2)
    print("____________________________")
    print("Should clients be created with a command by each user or automatically when a user sends a message? (y/n)")
    AUTOCLIENTS = yninput()
    if AUTOCLIENTS:
        config["AUTOCLIENTS"] = True
        print(bcolors.OKGREEN + "Clients will connect automatically when a user sends a message" + bcolors.OFF)
    else:
        config["AUTOCLIENTS"] = False
        print(bcolors.OKGREEN + "Clients will connect when a user uses the !joinirc command" + bcolors.OFF)
    time.sleep(2)
    print("____________________________")
    print(bcolors.OKCYAN + "Should Discord users be allowed to use !nick to change their client's nick on IRC? y/n" + bcolors.OFF)
    NICKCHANGE = yninput()
    print(bcolors.OKGREEN + "Use of !nick command is set to: " + str(NICKCHANGE) + bcolors.OFF)
    print("____________________________")
    time.sleep(1)
    print(bcolors.OKCYAN + "Lastly, we need the URL of the webhook that the bot will use to post messages from IRC")
    print("e.g https://discord.com/api/webhooks/.../.../...")
    print("You can create a Webhook in your Server's settings. Make sure to make it work in the same channel you input earlier. i.e the channel where the Relaying should happen in.", bcolors.OFF)
    WEBHOOK = input()
    config["WEBHOOK"] = WEBHOOK
    save_config()
    print("This Wizard has reached its end! Here are all your settings!")
    time.sleep(2)
    paste = ""
    for item in config:
        value = config[item]
        line = item + ": " + str(value)
        print(line)
        print("-")
else:
    print("Do you want to edit any values in the config? y/n")
    x = yninput()
    if x:
        print("I will cycle through each item and ask you if you want to edit it!")
        for i in config:
            item = i
            value = config[i]
            print(item, "=", value)
            print("Do you want to edit this value? (y/n)")
            x = yninput()
            if x:
                print("Please input the new value, if you didn't want to edit it, just press Enter")
                x = input()
                y = totype(value, x)
                while type(y) == list and y[0] == "non_same_type":
                        print("This is not an acceptable value for this setting. It should be", y[1])
                        print(item, "=", value)
                        y = totype(value, input())
                x = y
                if x != "":
                    config[item] = x
                    print(item, "=", config[item])
            time.sleep(2)
            print("_____________________________________")
        save_config()
        time.sleep(1)
        print(config)
