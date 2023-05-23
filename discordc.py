# Imports
import discord
import asyncio
import re
from asyncio import coroutines
import concurrent.futures
from asyncio import futures
from settings import *
global botlist
botlist = []
global condict
condict = {}

# Create bot
intents = discord.Intents.all()
intents.members = True
intents.messages = True
client = discord.Client(intents=intents)

whid = WEBHOOK.split("/")[5]

def get_urls(attach):
    urls = ""
    for i in range(len(attach)):
        urls += " " + attach[i].url
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
    send_my_message("I've been running for " + time)
    classcon.momsendmsg("I've been running for " + time)

def setstatus():
    asyncio.run_coroutine_threadsafe(setstatus_async(1), client.loop)

def send_my_message(message):
    global client
    asyncio.run_coroutine_threadsafe(send_my_message_async(message), client.loop)

async def send_my_message_async(message):
    global channel
    await channel.send(message.strip())

async def setstatus_async(a):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Do !joinirc to connect to IRC!"))

@client.event
async def on_message(message):
    global thread_lock
    global condict
    global channel
    checknick = False
    # Don't reply to itself
    if str(message.webhook_id) == whid:
        return
    if message.author == client.user:
        return
    if message.channel != channel:
        return

    authorid = str(message.author.id)
    content = message.clean_content.replace("\n", " ").strip()
    if content == "":
        content = "_empty_content_discord_bot_"
    contentsplit = content.split()
    for i in range(len(contentsplit)):
        c = contentsplit[i]
        if c[0] == "@" and c[-11:] == "_[IRC]#0000":
            contentsplit[i] = c[:-11][1:]
    content = ' '.join(contentsplit)

    if len(message.attachments) > 0:
        urls = get_urls(message.attachments)
        if content == "_empty_content_discord_bot_":
            content = urls
        else:
            content = content + urls

    if contentsplit[0] == "!uptime":
        senduptime()

    if contentsplit[0] == "!joinirc":
        if authorid in condict:
            send_my_message("You already have a client connected to IRC, your messages are being relayed!")
            return

        if len(contentsplit) > 1:
            checknick = fixnick(contentsplit[1])
        else:
            checknick = fixnick(message.author.name)
        if checknick == False:
            send_my_message("Your IRC nick can only contain A-Z a-z 0-9, your current username or requested nick cannot be used!")
            return
        if authorid not in condict:
            newclient = classcon.IRCbots(checknick + "[R]", IRCSERVER, IRCPORT, IRCCHAN, None, False, authorid)
            newclientcon = newclient.conn
            condict[authorid] = newclient
            newclient.connect()
            return
    if authorid in condict:
        condict[authorid].sendmsg(content)

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
