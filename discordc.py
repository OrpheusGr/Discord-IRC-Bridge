# Imports
import discord
import asyncio
import re
import time
from asyncio import coroutines
import concurrent.futures
from asyncio import futures
from settings import *
global botlist
botlist = []
global condict
condict = {}
channel = ""
killed = {}

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
    new_nick = re.sub(r'[\W_]', '', nick)
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
        mi = msplit[i]
        if "<https://" == mi[0:9] or "<http://" == mi[0:8] or "https://" == mi[0:8] or "http://" == mi[0:7]:
            msplit[i] = mi.replace("_", "pholderurlunderdash13095")
    m = " ".join(msplit)
    m = m.replace("_", chr(29))
    m = m.replace("***", chr(29) + "\x02")
    m = m.replace("**", "\x02")
    m = m.replace("*", chr(29))
    m = m.replace("```", "")
    m = m.replace("pholderurlunderdash13095", "_")
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

def setstatus():
    asyncio.run_coroutine_threadsafe(setstatus_async(1), client.loop)

def send_my_message(message):
    global client
    asyncio.run_coroutine_threadsafe(send_my_message_async(message), client.loop)

def shutdown():
    setattr(classcon.mom, "sent_quit_mom", 1)
    asyncio.run_coroutine_threadsafe(shutdown_async(), client.loop)

async def send_my_message_async(message):
    global channel
    await channel.send(message.strip())

async def setstatus_async(a):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Do !joinirc to connect to IRC!"))

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
    content = message.clean_content.replace("\n", " ").strip()

    if len(message.attachments) > 0:
        urls = get_urls(message.attachments)
        if content == "":
            content = urls
        else:
            content = content + urls
    content = ref + content
    contentsplit = content.split()
    cmd = contentsplit[0].lower()
    # botops commands block
    if authorid in DISCORDBOTOPS:

        #kill command - Kills a  user's client by force (used for moderation)
        if cmd == "!kill":
            if len(contentsplit) == 1:
                send_my_message("Usage: !kill useridhere")
                return
            killid = contentsplit[1]
            if killid not in condict and killid.isnumeric() == True:
                send_my_message("That user doesn't have a connected IRC client.")
                return
            if killid.isnumeric() == False:
                send_my_message("User ID's are numeric values!")
                return
            reason = ""
            if len(contentsplit) >= 3:
                 reason = " Reason: " + " ".join(contentsplit[2:])
            killed[killid] = round(time.time(), 0)
            tobekilled = condict[killid].conn
            setattr(tobekilled, "sent_quit", 1)
            tobekilled.quit("Client killed by " + message.author.name + reason)

        #shutdown command -  Quits IRC, kills Discord bot, stops process.
        if cmd == "!shutdown":
            uptime = classcon.get_uptime()
            send_my_message("**Shutdown request by " + message.author.name + ". I was alive for " + uptime + "**")
            classcon.mom.quit("It was " + message.author.name +  " from Discord, they pressed the red button! Agh! *dead* I was alive for" + uptime)
            time.sleep(2)
            shutdown()
            classcon.stoploop()

    #public commands block

    #relayuptime commmand - Simply sends the bot's uptime to Discord and IRC.
    if cmd == "!relayuptime":
        senduptime()

    #joinirc comand - Creates a client if the user doesn't already have one and their username/desired nick is acceptable.
    if cmd == "!joinirc":
        if classcon.mom.is_connected() == False:
            send_my_message("Central bot is currently disconnected from IRC, please wait and try again.")
            return

        if authorid in condict:
            send_my_message("**Error**: You already have a client connected to IRC, your messages are being relayed!")
            return

        if authorid in killed:
            ctime = round(time.time(), 0)
            timediff = ctime - killed[authorid]
            if timediff < 60:
                return

        if len(contentsplit) > 1:
            checknick = fixnick(contentsplit[1])
        else:
            checknick = fixnick(message.author.name)

        if checknick == False:
            send_my_message("**Error**: Your IRC nick can only contain A-Z a-z 0-9, your current username or requested nick cannot be used!")
            return
        if checknick + "[R]" in classcon.botdict or checknick + "_[R]" in classcon.botdict or checknick in classcon.botdict:
            send_my_message("**Error**: Another Discord User is using this nick, please provide another to avoid confusion with simular nicks.")
            return

        if authorid not in condict:
            newclient = classcon.IRCbots(checknick + "[R]", IRCSERVER, IRCPORT, IRCCHAN, None, False, authorid)
            newclientcon = newclient.conn
            condict[authorid] = newclient
            newclient.connect()
            return

    #ircnick commmand - If the user has a client, changes its nick to the provided one. (if the nick isn't used)
    if cmd == "!ircnick":
        if authorid not in condict:
            send_my_message("You don't have a client connected. Did you mean: !joinirc")
            return
        if len(contentsplit) == 1:
            send_my_message("Usage: !ircnick <nickhere>")
            return
        urequest = contentsplit[1]
        ucon = condict[authorid].conn
        uconick = ucon.get_nickname()
        if urequest == uconick or urequest + "[R]" == uconick:
            send_my_message("You are already using " + urequest + " (" + uconick + ") on IRC.")
            return
        if urequest + "[R]" in classcon.botdict or urequest + "[R]_" in classcon.botdict or urequest in classcon.botdict:
            send_my_message("Another Discord User is using a simular/the same nick, please choose another ome to avoid confusion")
            return
        ucon.nick(urequest + "[R]")

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
