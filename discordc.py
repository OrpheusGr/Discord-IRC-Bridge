# Imports
import discord
import asyncio
import re
import time
from asyncio import coroutines
import concurrent.futures
from asyncio import futures
import settings
import helpreplies
import sys
import random
global botlist
botlist = []
global condict
condict = {}
channel = ""
killed = {}
leftirc = {}
help = helpreplies.help
# Load the config
def load_the_config():
    config = settings.load_config()
    if config == False:
        sys.exit(0)
    else:
        print(config)
        for item in config:
            globals()[item] = config[item]

load_the_config()

# Create bot
intents = discord.Intents.all()
intents.members = True
intents.messages = True
client = discord.Client(intents=intents)

whid = WEBHOOK.split("/")[5]

def get_urls(attach):
    urls = ""
    for i in range(len(attach)):
        urls += " | <" + attach[i].url + ">"
    return urls

def set_classcon(con):
    global classcon
    classcon = con

def set_thread_lock(lock):
    global thread_lock
    thread_lock = lock

def fixnick(nick):
    new_nick = re.sub(r'[^A-Za-z0-9 ^\[\]\\{}`_-]+', '', nick)
    print(new_nick)
    if new_nick == "":
        return False
    else:
        return new_nick

def senduptime():
    time = classcon.get_uptime()
    classcon.sendtoboth("I've been running for " + time)

def ircdressup(m):
    msplit = m.split()
    for i in range(len(msplit)):
        if msplit[i].startswith("http") or msplit[i].startswith("<http"):
            msplit[i] = msplit[i].replace("_", "underdashreplacementplaceholderdiscordbotregexsucks")
    m = " ".join(msplit)
    m = m.replace("***", chr(29) + "\x02")
    m = m.replace("**", "\x02")
    m = m.replace("*", chr(29))
    m = m.replace("```", "")
    m = m.replace("_", chr(29))
    m = m.replace("underdashreplacementplaceholderdiscordbotregexsucks", "_")
    return m

def get_reference(r, p, a):
    rid = r.author.id
    rauthor = r.author.name
    rurl = ""
    if len(r.attachments) > 0:
        rurl = get_urls(r.attachments)
    for i in classcon.botdict:
        b = classcon.botdict[i]
        if b == rid:
            rauthor = i
    rcont = ircdressup(r.clean_content.replace("\n", "").strip())
    if rcont == "":
        rcont = rurl
    if p == False:
        rfull = "<" + rauthor + "> " + rcont + " <<< "
    else:
        rfull = a + " pinned a message <" + rauthor + "> " + rcont
    return rfull

def replace_emojis(content):
    regexc = re.compile('<:\w*:\d*>', re.UNICODE)
    findmoji = re.findall(regexc, content)
    for moji in findmoji:
        namemoji = ":" + moji.split(":")[1] + ":"
        content = content.replace(moji, namemoji)
    return content

def setstatus():
    asyncio.run_coroutine_threadsafe(setstatus_async(1), client.loop)

def send_my_message(message):
    global client
    asyncio.run_coroutine_threadsafe(send_my_message_async(message), client.loop)

def shutdown():
    classcon.momobj.sent_quit_on()
    time.sleep(2)
    asyncio.run_coroutine_threadsafe(shutdown_async(), client.loop)

async def send_my_message_async(message):
    global channel
    await channel.send(message.strip())

async def setstatus_async(a):
    if AUTOCLIENTS != True:
        status = "!joinirc to connect to IRC"
    else:
        status = "Discord & IRC"
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))

async def shutdown_async():
    await client.close()

@client.event
async def on_message(message):
    global thread_lock
    global condict
    global channel
    checknick = False
    ref = ""
    msgrefpin = False
    # Don't reply to itself or to the webhook or if the channel is not the one in settings
    if str(message.webhook_id) == whid:
        return
    if message.author == client.user:
        return
    if message.channel != channel:
        return

    if message.type == discord.MessageType.pins_add:
        msgrefpin = True

    if message.reference:
        refid = message.reference.message_id
        refinfo = await channel.fetch_message(refid)
        ref = get_reference(refinfo, msgrefpin, message.author.name)

    authorid = str(message.author.id)
    content = replace_emojis(message.clean_content.replace("\n", " ").strip())

    idarg = ""
    dirty_content = message.content.replace("\n", " ").strip()
    dirty_split = dirty_content.split()
    if len(dirty_split) > 1:
        dirty_one = dirty_split[1]
        dirty_one_len = len(dirty_one) - 1
        dirty_id = dirty_one[2:dirty_one_len]
        if dirty_one.startswith("<@") == True and dirty_one.endswith(">") == True and dirty_id.isnumeric() == True:
            idarg = dirty_id

    if len(message.attachments) > 0:
        urls = get_urls(message.attachments)
        if content == "":
            content = urls
        else:
            content = content + urls
    if content == "":
        print("Stickers/embed are not seen by discord.py")
        return
    content = ref + content
    contentsplit = content.split()
    cmd = contentsplit[0].lower()
    # botops commands block
    if authorid in DISCORDBOTOPS:

        #kill command - Kills (sends a quit message) a user's client by force (used for moderation)
        if cmd == "!kill":
            if len(contentsplit) == 1 or idarg == "":
                send_my_message("Usage: !kill @mention_here")
                return
            killid = idarg
            if killid not in condict:
                send_my_message("That user doesn't have a connected IRC client.")
                return
            reason = ""
            if "--delete" in contentsplit:
                contentsplit.remove("--delete")
                if killid in classcon.savedclients:
                    classcon.savedclients.pop(killid)
                    settings.saveclients(classcon.savedclients)
            if len(contentsplit) >= 3:
                 reason = " Reason: " + " ".join(contentsplit[2:])
            killed[killid] = round(time.time(), 0)
            tobekilled = condict[killid].conn
            setattr(tobekilled, "sent_quit", 1)
            tobekilled.disconnect("Client killed by " + message.author.name + reason)
            return

        #shutdown command -  Quits IRC, kills Discord bot, stops process.
        elif cmd == "!shutdown":
            uptime = classcon.get_uptime()
            send_my_message("**Shutdown request by " + message.author.name + ". I was alive for " + uptime + "**")
            shutdown()
            classcon.mom.disconnect("It was " + message.author.name +  " from Discord, they pressed the red button! Agh! *dead* I was alive for" + uptime)
            time.sleep(2)
            classcon.stoploop()
            return

        #fjoinirc command - Makes a client for another user
        elif cmd == "!fjoinirc":
            if idarg == "":
                send_my_message("You need to mention the user you want to forcejoin")
                return
            if idarg in condict:
                send_my_message("The user you provided has already joined IRC")
                return
            if classcon.mom.is_connected() == False:
                send_my_message("Central bot is currently disconnected from IRC, please wait and try again.")
                return
            idarg_user = await message.guild.fetch_member(int(idarg))
            idarg_name = idarg_user.name
            if "--nick" in contentsplit:
                contentsplit.remove("--nick")
                if idarg_user.nick:
                    idarg_name = idarg_user.nick
            if idarg in killed:
                killed.pop(idarg)
                print("Cleared user: " + idarg_name + " with ID: " + idarg + " from killed list, botop: " + message.author.name + " with ID: " + authorid + " used !fjoinirc")
            if idarg_name == None:
                idarg_name = "DiscordUser_" + str(random.randomint(10,99))
            if idarg not in classcon.savedclients:
                 if len(contentsplit) > 2:
                     checknick = fixnick(contentsplit[2])
                 else:
                     checknick = fixnick(idarg_name)
            else:
                 if idarg in classcon.savedclients:
                     checknick = classcon.savedclients[idarg]
                 else:
                     checknick = fixnick(idarg_name)
            if checknick == False:
                 send_my_message("The nickname you provided is invalid. IRC nicks must be A-Z a-z 0-9")
                 return

            newclient = classcon.IRCbots(checknick + "[R]", IRCSERVER, IRCPORT, IRCCHAN, None, False, idarg)
            newclientcon = newclient.conn
            condict[idarg] = newclient
            newclient.connect()
            return

        #fnick command - Forcefully changes a Discord user's IRC nick (used for moderation)
        elif cmd == "!fnick":
            if idarg == "":
                 send_my_message("You need to mention the user whose nick you want to change.")
                 return
            if idarg not in condict:
                 send_my_message("That user doesn't have a client. Did you mean !fjoinirc ?")
                 return
            if len(contentsplit) < 3:
                 send_my_message("Usage: !fnick @mention_here new_nick_here")
                 return
            urequest = contentsplit[2]
            ucon = condict[idarg].conn
            uconick = ucon.get_nickname()
            if urequest == uconick or urequest + "[R]" == uconick:
                send_my_message("User is already using " + urequest + " (" + uconick + ") on IRC.")
                return
            if urequest + "[R]" in classcon.botdict or urequest + "[R]_" in classcon.botdict or urequest in classcon.botdict:
                send_my_message("Another Discord User is using a simular/the same nick, please choose another one to avoid confusion.")
                return
            ucon.nick(urequest + "[R]")
            classcon.savedclients.pop(idarg)
            classcon.savedclients[idarg] = urequest + "[R]"
            settings.saveclients(classcon.savedclients)
            return

        #whois command - Shows what nick a Discord user is using on IRC (used for moderation)
        elif cmd == "!whois":
            if idarg == "":
                send_my_message("You need to mention a user.")
                return
            if idarg not in condict:
                if idarg in classcon.savedclients:
                    send_my_message("This user doesn't have a connected client at the moment, but the nick i have saved for them is: " + classcon.savedclients[idarg])
                    return
                else:
                    send_my_message("This user doesn't have a connected client and there's no saved client for them")
                    return
            else:
                send_my_message("This user's IRC nick is: " + classcon.find_nick_by_id(idarg))
                return

    #public commands block

    #joinirc command - Creates a client if the user doesn't already have one and their username/desired nick is acceptable.
    if cmd == "!joinirc" or AUTOCLIENTS == True:
        usenick = message.author.name
        if "--nick" in contentsplit:
            contentsplit.remove("--nick")
            if message.author.nick:
                usenick = message.author.nick
        if classcon.mom.is_connected() == False and cmd == "!joinirc" and AUTOCLIENTS == False:
            send_my_message("Central bot is currently disconnected from IRC, please wait and try again.")
            return

        if authorid in condict:
            if AUTOCLIENTS == False and cmd == "!joinirc":
                send_my_message("**Error**: You already have a client connected to IRC, your messages are being relayed!")
            condict[authorid].sendmsg(ircdressup(content))
            return

        if authorid in killed:
            ctime = round(time.time(), 0)
            timediff = ctime - killed[authorid]
            if timediff < TIMEKILLED or TIMEKILLED == 0:
                if cmd == "!joinirc" and AUTOCLIENTS == False:
                    if TIMEKILLED == 0:
                        killtimeleft = "Permanent"
                    else:
                        killtimeleft = TIMEKILLED - timediff
                    send_my_message("Your client has been killed by a botop (" + str(killtimeleft) + " secs left)")
                return
            else:
                killed.pop(authorid)

        if AUTOCLIENTS != True:
            if len(contentsplit) > 1:
                checknick = fixnick(contentsplit[1])
            else:
                if authorid in classcon.savedclients:
                    checknick = classcon.savedclients[authorid]
                    checknick = checknick[0:len(checknick)-3]
                else:
                    checknick = fixnick(usenick)
        else:
            if authorid in classcon.savedclients:
                checknick = classcon.savedclients[authorid]
                checknick = checknick[0:len(checknick)-3]
            else:
                checknick = fixnick(usenick)

        if checknick == False:
            if cmd == "!joinirc" and AUTOCLIENTS == False:
                send_my_message("**Error**: Your IRC nick can only contain A-Z a-z 0-9, your current username or requested nick cannot be used!")
                return
            checknick = "DiscordUser_" + random.randomint(100,999)
        if checknick + "[R]" in classcon.botdict or checknick + "_[R]" in classcon.botdict or checknick in classcon.botdict:
            send_my_message("**Error**: Another Discord User is using this nick, please provide another to avoid confusion with simular nicks.")
            return

        if authorid not in condict:
            newclient = classcon.IRCbots(checknick + "[R]", IRCSERVER, IRCPORT, IRCCHAN, None, False, authorid)
            newclientcon = newclient.conn
            condict[authorid] = newclient
            newclient.connect()
            return

    #relayuptime commmand - Simply sends the bot's uptime to Discord and IRC.
    elif cmd == "!relayuptime":
        senduptime()
        return

    elif cmd == "!relayhelp":
        if len(contentsplit) == 1:
            send_my_message(help["listcommands"])
        else:
            if contentsplit[1] in help:
                send_my_message(help[contentsplit[1]])
            else:
                send_my_message("Invalid parameter. Use '!relayhelp listcommands' to see a list of commands you can get help for.")
        return
    #leaveirc command - Disconnects the user's client from IRC, to get it back they must user !joinirc (wether AUTOCLIENTS is on or off)
    elif cmd == "!leaveirc":
        if authorid not in condict:
            send_my_message("You don't have a client connected. Did you mean: !joinirc ? :smirk:")
            return
        if "--delete" in contentsplit:
            contentsplit.remove("--delete")
            classcon.savedclients.pop(authorid)
            settings.saveclients(classcon.savedclients)
        reason = ""
        if len(contentsplit) > 1:
            reason = "Reason: " + ' '.join(contentsplit[1:])
        ucon = condict[authorid].conn
        setattr(ucon, 'sent_quit', 1)
        ucon.disconnect("Client removed by user. " + reason)
        leftirc[ucon] = 1

    #nick command - If the user has a client, changes its nick to the provided one. (if the nick isn't used)
    elif cmd == "!nick":
        if AUTOCLIENTS == True:
            print("!nick is disabled since AUTOCLIENTS is set to True")
            return
        if authorid not in condict:
            send_my_message("You don't have a client connected. Did you mean: !joinirc")
            return
        if len(contentsplit) == 1:
            send_my_message("Usage: !nick <nickhere>")
            return
        urequest = contentsplit[1]
        ucon = condict[authorid].conn
        uconick = ucon.get_nickname()
        if urequest == uconick or urequest + "[R]" == uconick:
            send_my_message("You are already using " + urequest + " (" + uconick + ") on IRC.")
            return
        if urequest + "[R]" in classcon.botdict or urequest + "[R]_" in classcon.botdict or urequest in classcon.botdict:
            send_my_message("Another Discord User is using a simular/the same nick, please choose another one to avoid confusion")
            return
        ucon.nick(urequest + "[R]")
        classcon.savedclients[authorid] = urequest + "[R]"
        settings.saveclients(classcon.savedclients)
        return

    #whoami command - Shows a Discord user their IRC nick
    elif cmd == "!whoami":
        if authorid not in condict:
            if authorid in classcon.savedclients:
                send_my_message("You don't have a connected client at the moment, but the nick i have saved for you is: " + classcon.savedclients[authorid])
                return
            else:
                send_my_message("You don't have a connected client and there's no saved client for you.")
                return
        send_my_message("Your IRC nick is: " + classcon.find_nick_by_id(authorid))
        return

    #public commands close block
    if authorid in condict:
        condict[authorid].sendmsg(ircdressup(content))


    with thread_lock:
        print("[Discord] " + message.author.name + ": " + content)

def run():
    client.run(TOKEN)

@client.event
async def on_ready():
    global channel
    global thread_lock

    with thread_lock:
        print("[Discord] Logged in as:")
        print("[Discord] " + client.user.name)
        print("[Discord] " + str(client.user.id))

        if len(client.guilds) == 0:
            print("[Discord] Bot is not yet in any server.")
            await client.close()
            return

        if DISCORDSERVER == "":
            print("[Discord] You have not configured a server to use in settings.json")
            print("[Discord] Please put one of the server IDs listed below in settings.json")

            for server in client.guilds:
                print("[Discord] %s: %s" % (server.name, server.id))

            await client.close()
            return

        findServer = [x for x in client.guilds if str(x.id) == DISCORDSERVER]
        if not len(findServer):
            print("[Discord] No server could be found with the specified id: " + DISCORDSERVER)
            print("[Discord] Available servers:")
            for server in client.guilds:
                print("[Discord] %s: %s" % (server.name, server.id))
            await client.close()
            return

        server = findServer[0]

        if DISCORDCHAN == "":
            print("[Discord] You have not configured a channel to use in settings.json")
            print("[Discord] Please put one of the channel IDs listed below in settings.json")
            for channel in server.channels:
                if channel.type == discord.ChannelType.text:
                    print("[Discord] %s: %s" % (channel.name, channel.id))

            await client.close()
            return

        findChannel = [x for x in server.channels if str(x.id) == DISCORDCHAN and x.type == discord.ChannelType.text]
        if not len(findChannel):
            print("[Discord] No channel could be found with the specified id: " + DISCORDSERVER)
            print("[Discord] Note that you can only use text channels.")
            print("[Discord] Available channels:")

            for channel in server.channels:
                if channel.type == discord.ChannelType.text:
                    print("[Discord] %s: %s" % (channel.name, channel.id))

            await client.close()
            return

        channel = findChannel[0]
