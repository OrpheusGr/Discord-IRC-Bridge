# Imports
import discord
from discord.ext import commands
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
import thetimers
import atexit
import logging
condict = {}
killed = {}
leftirc = {}
leftirc_chan = {}
help = helpreplies.help
shutting_down = 0
savedclients = {}
mymessages = ""
channel_sets = {}
clockmoji = u"\U0001F552"
cmdlist = ["!joinirc", "!leaveirc", "!quitirc", "!leavechan", "!nick", "!whoami", "!bridgeuptime", "!bridgeshutdown", "!fjoinirc", "!kill", "!fnick", "!whois"]
cooldown = {}
statuses = ["Discord & IRC", "the sound of IRC", "Bridging IRC & Discord", "IRC & Discord", "Oldschool IRC mixtape", "The world of IRC", "IRC ambience"]
statusindex = 0
timesleep = 0
lastmsg = {}
sendmymsg_lastcall = 0
sendmymsg_delay = 0
lastchannel_disc_irc = ""
handler = logging.FileHandler(filename='discordc_errors.log', encoding='utf-8', mode='w')

for i in cmdlist:
    cooldown[i] = {}
cooldown["globalcool"] = {}
cooldown["alreadyreact"] = {}

# Load the config
def load_the_config():
    global savedclients
    config = settings.load_config()
    savedclients = settings.load_saved_clients()
    if config == False:
        sys.exit(0)
    else:
        print(config)
        for item in config:
            globals()[item] = config[item]

load_the_config()

# Create bot
Intents = discord.Intents.all()
Intents.members = True
Intents.messages = True
Intents.presences = True
bot = commands.Bot(command_prefix="!", intents=Intents)

def get_urls(attach):
    urls = ""
    add = ""
    for i in range(len(attach)):
        urls += add + attach[i].url
        if add == "":
            add = " | "
    return urls

def set_classcon(con):
    global classcon
    classcon = con

def set_thread_lock(lock):
    global thread_lock
    thread_lock = lock

def fixnick(nick):
    new_nick = re.sub(r'[^A-Za-z0-9 ^\[\]\\{}`_-]+', '', nick)
    if new_nick == "":
        return False
    else:
        return new_nick

def senduptime(discord_chan, irc_chan):
    time = classcon.get_uptime()
    classcon.sendtoboth(discord_chan, irc_chan, "I've been running for " + time)

def ircdressup(m):
    msplit = m.split()
    for i in range(len(msplit)):
        if msplit[i].startswith("http") or msplit[i].startswith("<http"):
            msplit[i] = msplit[i].replace("_", "underdashreplacementplaceholderdiscordbotregexsucks")
    m = " ".join(msplit)
    m = dressup_replace(m, "***", "\x1d" + "\x02")
    m = dressup_replace(m, "**", "\x02")
    m = dressup_replace(m, "*", "\x1d")
    m = dressup_replace(m, "```", "")
    m = dressup_replace(m, "_", "\x1d")
    m = m.replace("underdashreplacementplaceholderdiscordbotregexsucks", "_")
    return m

def dressup_replace(m, substr, replacement):
    if m.count(substr) == 1:
        return m
    m = m.replace(substr, replacement)
    return m

def get_reference(r, p, a, whid):
    rid = r.author.id
    ircnick = classcon.find_nick_by_id(str(rid))
    if ircnick == False:
        rauthor = r.author.name
    else:
        rauthor = ircnick
    if str(r.webhook_id) == whid:
        rauthor = rauthor[0:len(rauthor)-6]
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
        rfull = "\"<" + rauthor + "> " + rcont + "\" <<< "
    else:
        rfull = a + " pinned a message: \"<" + rauthor + ">\" " + rcont
    return rfull

def replace_emojis(content):
    regexc = re.compile('<:\w*:\d*>', re.UNICODE)
    findmoji = re.findall(regexc, content)
    for moji in findmoji:
        namemoji = ":" + moji.split(":")[1] + ":"
        content = content.replace(moji, namemoji)
    return content

def setstatus():
    global statusindex
    c_status = statuses[statusindex]
    asyncio.run_coroutine_threadsafe(setstatus_async(c_status), bot.loop)
    if statusindex < len(statuses)-1:
        statusindex += 1
    else:
        statusindex = 0
    thetimers.add_timer("setstatus", 900, setstatus)

# send_my_message actually used to contain what send_my_message_b contains now. I wanted to prevent the bot from flooding Discord and this was the easier way to do it without
# changing every single line that called send_my_message. So i just changed send_my_message into a kind of buffer that delays the calls by adding a timer that calls _b
# This way the system of editing the join/part/quit messages (instead of sending a new one) worked out the best, as the bot needed time to track the lastmsg in on_message
# before send_my_message was called again.

def send_my_message(discord_chan, message):
    global sendmymsg_lastcall
    global sendmymsg_delay
    if sendmymsg_lastcall == 0:
        sendmymsg_lastcall = time.time()
    ctime = time.time()
    diff = ctime - sendmymsg_lastcall
    if diff < 2:
        sendmymsg_delay += 2
        thetimers.add_timer("", sendmymsg_delay, send_my_message_b, *(discord_chan, message))
    else:
        sendmymsg_delay = 0
        send_my_message_b(discord_chan, message)
    sendmymsg_lastcall = ctime

def send_my_message_b(discord_chan, message):
    global bot
    global lastmsg
    orig_message = message
    chanid = str(discord_chan.id)
    if chanid in lastmsg:
        lastmsgchan = lastmsg[chanid]
    else:
        lastmsgchan = None
    if lastmsgchan == None or str(lastmsgchan.author.id) != str(bot.user.id) or (lastmsgchan.clean_content == "**Bridge is now running!**" and str(lastmsgchan.author.id) == str(bot.user.id)):
        asyncio.run_coroutine_threadsafe(send_my_message_async(discord_chan, message), bot.loop)
    elif lastmsgchan != None and str(lastmsgchan.author.id) == str(bot.user.id):
        editedmsg = lastmsgchan.content + " | " + message
        if "[R] joined" in lastmsgchan.clean_content:
            if "[R] joined" in message and classcon.get_uptime(True) <= 120:
                editedmsg = lastmsgchan.content + " | " + " ".join(message.split()[1:2]) + "**"
                jointitle = "Bridge Clients Joined: "
                if jointitle in lastmsgchan.clean_content:
                    jointitle = ""
                editedmsg = jointitle + editedmsg
            elif "[R] joined" not in message:
                asyncio.run_coroutine_threadsafe(send_my_message_async(discord_chan, message), bot.loop)
                return
        else:
            if (lastmsgchan.content[0:4] in ["-> *", "<- *"] and message[0:4] not in ["-> *", "<- *"]) or (message[0:4] in ["-> *", "<- *"] and lastmsgchan.content[0:4] not in ["-> *", "<- *"]) and lastmsgchan.content[0:5] != "[...]":
                asyncio.run_coroutine_threadsafe(send_my_message_async(discord_chan, message), bot.loop)
                return
            if message[0:4] in ["-> *", "<- *"] or message[0:4] == "[...]":
                message = " ".join(message.split()[1:3]) + "**"
                editedmsg = lastmsgchan.content + " | " + message
        if len(editedmsg) > 350:
            asyncio.run_coroutine_threadsafe(edit_my_message_async(lastmsgchan, "[...] " + orig_message), bot.loop)
            #asyncio.run_coroutine_threadsafe(del_my_message_async(lastmsgchan), bot.loop)
            #asyncio.run_coroutine_threadsafe(send_my_message_async(discord_chan, orig_message), bot.loop)
            return
        asyncio.run_coroutine_threadsafe(edit_my_message_async(lastmsgchan, editedmsg), bot.loop)

def send_to_all(message):
    for item in channel_sets:
        send_my_message(channel_sets[item]["real_chan"], message)

def shutdown(reason="", exiting=False):
    if exiting == False:
        atexit.unregister(shutdown)
    global shutting_down
    shutting_down = 1
    quitall(reason, exiting)

def die():
    asyncio.run_coroutine_threadsafe(shutdown_async(), bot.loop)
    classcon.stoploop()

def quitall(reason, exiting):
    copycondict = list(condict.keys())
    timesleep = 0
    clientreason = "Bridge Shutting Down"
    for item in copycondict:
        timesleep += 1
        con = condict[item].conn
        setattr(con, "sent_quit", 1)
        if exiting == False:
            thetimers.add_timer("", timesleep, con.disconnect, clientreason)
        else:
            con.disconnect(clientreason)
    classcon.momobj.sent_quit_on()
    uptime = classcon.get_uptime()
    if exiting == False:
        thetimers.add_timer("", timesleep+1, classcon.mom.disconnect, "Bridge is shutting down after running for " + uptime + " " + reason)
        asyncio.run_coroutine_threadsafe(do_async_stuff(die, timesleep + 3), bot.loop)
    else:
        classcon.mom.disconnect("Bridge is shutting down after running for " + uptime + " " + reason)

atexit.register(shutdown, "Bridge killed from Terminal", True)

async def send_my_message_async(discord_chan, message):
    await discord_chan.send(message.strip())

async def edit_my_message_async(msg_object, edit):
    await msg_object.edit(content=edit)

async def del_my_message_async(msg_object):
    await msg_object.delete()

def is_member(id):
    guild = bot.get_guild(int(DISCORDSERVER))
    member = guild.get_member(int(id))
    return member

def check_global_cooldown(authorid):
    global cooldown
    foundincool = 0
    for i in cooldown:
        cmd = cooldown[i]
        if authorid in cmd:
            foundincool += 1
    return foundincool

async def setstatus_async(status):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))

async def shutdown_async():
    await asyncio.sleep(2)
    await bot.close()

async def do_async_stuff(target, delay, *arguments):
    await asyncio.sleep(delay)
    target(*arguments)

@bot.event
async def on_message_edit(before, after):
    global channel
    global condict
    # Certain conditions on which we don't want the bot to act
    if before.author == bot.user:
        return
    if str(before.channel.id) not in channel_sets:
        return
    if shutting_down == 1:
        return
    irc_chan = channel_sets[str(before.channel.id)]["irc_chan"]
    authorid = str(before.author.id)
    beforecontent = replace_emojis(before.clean_content.replace("\n", " ").strip())
    aftercontent = replace_emojis(after.clean_content.replace("\n", " ").strip())

    if authorid in condict:
        if beforecontent != aftercontent:
            condict[authorid].sendmsg(irc_chan, "EDIT: " + ircdressup(aftercontent))

@bot.event
async def on_presence_update(before, after):
    userid = str(after.id)
    dname = after.display_name
    if userid in condict:
        ucon = condict[userid]
        if after.raw_status == "online":
            ucon.set_away()
        else:
            awayline = "Discord Status: " + after.raw_status
            ucon.set_away(awayline)

@bot.event
async def on_message(message):
    global thread_lock
    global condict
    global leftirc
    global cooldown
    global lastmsg

    uptime = classcon.get_uptime(True)

    if uptime <= 20:
        return

    lastchannel_irc_disc = message.channel
    classcon.lastchannel_irc_disc = message.channel

    checknick = False
    ref = ""
    msgrefpin = False
    action_msg = False
    channel_id = str(message.channel.id)

    lastmsg[channel_id] = message

    # Certain conditions on which we don't want the bot to act
    if message.author == bot.user:
        return
    if channel_id not in channel_sets:
        return
    whid = channel_sets[channel_id]["webhook"].split("/")[5]
    if str(message.webhook_id) == whid:
        return
    if shutting_down == 1:
        return

    irc_chan = channel_sets[channel_id]["irc_chan"]
    if irc_chan not in leftirc_chan:
        leftirc_chan[irc_chan] = []
    # Detect if a message was pinned

    if message.type == discord.MessageType.pins_add:
        msgrefpin = True

    # Detect if the message is a reply to another message and fetch the old message content

    if message.reference:
        refid = message.reference.message_id
        refinfo = await message.channel.fetch_message(refid)
        ref = get_reference(refinfo, msgrefpin, message.author.name, whid)

    authorid = str(message.author.id)
    content = replace_emojis(message.clean_content.replace("\n", " ").strip())
    contentsplit = content.split()

    # Detect if the message is in italics (usually when /me is used)

    if len(contentsplit) > 0 and contentsplit[0].startswith("_") == True and contentsplit[len(contentsplit)-1].endswith("_") == True:
        action_msg = True

    # Detect if the second word is a mention and replace the spaces of the mention with a dash
    # This is done for commands that take a mention as an argument
    # (if the username contains spaces it is split into diff items
    # So we use the raw mention, we get the user's id, and with that their username or nick
    # Then we replace the spaces with underdashes.

    idarg = ""
    idarg_user = ""
    idarg_name = ""
    idarg_nick = ""
    dirty_content = message.content.replace("\n", " ").strip()
    dirty_split = dirty_content.split()
    if len(dirty_split) > 1:
        dirty_one = dirty_split[1]
        dirty_one_len = len(dirty_one) - 1
        dirty_id = dirty_one[2:dirty_one_len]
        if dirty_one.startswith("<@") == True and dirty_one.endswith(">") == True and dirty_id.isnumeric() == True and dirty_content[0].startswith("!"):
            idarg = dirty_id
            idarg_user = await message.guild.fetch_member(int(idarg))
            idarg_name = idarg_user.name
            content = contentsplit[0] + " " + idarg_name + " " + " ".join(dirty_split[2:])
            if idarg_user.nick:
                idarg_nick = idarg_user.nick
                content = contentsplit[0] + " " + idarg_nick.replace(" ", "_") + " " + " ".join(dirty_split[2:])

    if len(message.attachments) > 0:
        urls = get_urls(message.attachments)
        if content == "":
            content = urls
        else:
            content = content + " " + urls
    if content == "" and msgrefpin == False:
        print("Stickers/embed are not seen by discord.py")
        return
    content = ref + content
    contentsplit = content.split()

    cmd = contentsplit[0].lower()

    # simple command cooldown system, 10 seconds long, adds a clock emoji reaction if the author
    # is in cooldown for the command used, and if they are in cooldown for 3 or more commamds
    # adds them to global cooldown for 60 seconds.

    if cmd in cmdlist and authorid not in DISCORDBOTOPS:
        if authorid in cooldown[cmd] or authorid in cooldown["globalcool"]:
            if authorid not in cooldown["alreadyreact"]:
                cooldown["alreadyreact"][authorid] = 1
                reactdel = 10
                if authorid in cooldown["globalcool"]:
                    reactdel = 60
                thetimers.add_timer("", reactdel, cooldown["alreadyreact"].pop, authorid)
                await message.add_reaction(clockmoji)
            return
        else:
            cooldown[cmd][authorid] = 1
            thetimers.add_timer("", 10, cooldown[cmd].pop, authorid)
            checkhowmany = check_global_cooldown(authorid)
            if checkhowmany == 3:
                cooldown["globalcool"][authorid] = 1
                thetimers.add_timer("", 60, cooldown["globalcool"].pop, authorid)

    # NOTE: add DM command !config to edit the config here

    # This is a message catcher, it comes before all the other commands cause it's responsible for making and connecting an IRC client for the user that just sent a message
    # This only gets triggeted if you enable the AUTOCLIENTS setting when running setupwizard.py to create or edit the config

    if AUTOCLIENTS == True and authorid not in leftirc_chan[irc_chan] and cmd.startswith("!") == False and cmd != "!joinirc":
        if authorid not in condict:
            if authorid in killed:
                ctime = round(time.time(), 0)
                timediff = ctime - killed[authorid]
                if timediff < TIMEKILLED or TIMEKILLED == 0:
                   return
            if authorid in classcon.savedclients:
                checknick = fixnick(classcon.savedclients[authorid]["nick"])
                checknick = checknick[0:len(checknick)-3]
                savedchans = classcon.savedclients[authorid]["channels"]
                if irc_chan not in savedchans:
                    savedchans.append(irc_chan)
            else:
                checknick = fixnick(message.author.name)
            while checknick == False:
                if message.author.nick:
                    checknick = fixnick(message.author.nick.replace(" ", "_"))
                else:
                    checknick = "DiscordUser_" + str(random.randomint(100,9999))
            newclient = classcon.IRCbots(checknick + "[R]", IRCSERVER, IRCPORT, [irc_chan], None, False, authorid)
            newclientcon = newclient.conn
            condict[authorid] = newclient
            newclient.connect()
        elif authorid in condict:
            ucon = condict[authorid].conn
            if ucon.is_connected() == False:
                return
            irc_nick = ucon.get_nickname()
            check_ison_chan = classcon.ison_chan(irc_chan, irc_nick)
            if check_ison_chan == False:
                ucon.join(irc_chan)
                savedchans = classcon.savedclients[authorid]["channels"]
                if irc_chan not in savedchans:
                    savedchans.append(irc_chan)
                    settings.saveclients(classcon.savedclients)

    # botops commands block
    if authorid in DISCORDBOTOPS:

        #kill command - Kills (sends a quit message) a user's client by force (used for moderation)
        if cmd == "!kill":
            if len(contentsplit) == 1 or idarg == "":
                send_my_message(message.channel, "Usage: !kill @mention_here")
                return
            killid = idarg
            if killid not in condict:
                send_my_message(message.channel, "That user doesn't have a connected IRC client.")
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

        #bridgeshutdown command -  Quits IRC, kills Discord bot, stops process.
        elif cmd == "!bridgeshutdown":
            uptime = classcon.get_uptime()
            reason = ""
            if len(contentsplit) > 1:
                reason = "Reason: " + ' '.join(contentsplit[1:])
            send_to_all("Bridge shutting down after running for " + uptime + " " + reason)
            shutdown(reason)
            return

        #fjoinirc command - Makes a client for another user
        elif cmd == "!fjoinirc":
            if idarg == str(bot.user.id):
                send_my_message(message.channel, "You can't make an IRC client for me!")
                return
            if idarg == "":
                send_my_message(message.channel, "You need to mention the user you want to forcejoin")
                return
            if idarg in condict:
                ucon = condict[idarg].conn
                irc_nick = ucon.get_nickname()
                check_ison_chan = classcon.ison_chan(irc_chan, irc_nick)
                if check_ison_chan == False:
                    ucon.join(irc_chan)
                    savedchans = classcon.savedclients[idarg]["channels"]
                    if irc_chan not in savedchans:
                        savedchans.append(irc_chan)
                        settings.saveclients(classcon.savedclients)
                    return
                else:
                    send_my_message(message.channel, "The user you provided has already joined " + irc_chan + " on IRC")
                    return
            if classcon.mom.is_connected() == False:
                send_my_message(message.channel, "Central bot is currently disconnected from IRC, please wait and try again.")
                return

            if idarg in leftirc_chan[irc_chan]:
                leftirc_chan[irc_chan].remove(idarg)
            if "--nick" in contentsplit:
                contentsplit.remove("--nick")
                if idarg_nick:
                    idarg_name = idarg_nick.replace(" ", "_")
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
                     checknick = classcon.savedclients[idarg]["nick"]
                     checknick = checknick[0:len(checknick)-3]
                 else:
                     checknick = fixnick(idarg_name)
            if checknick == False:
                 send_my_message(message.channel, "The nickname you provided is invalid. IRC nicks must be A-Z a-z 0-9")
                 return

            newclient = classcon.IRCbots(checknick + "[R]", IRCSERVER, IRCPORT, [irc_chan], None, False, idarg)
            newclientcon = newclient.conn
            condict[idarg] = newclient
            newclient.connect()
            if authorid in leftirc:
                leftirc.pop(authorid)
            return

        #fnick command - Forcefully changes a Discord user's IRC nick (used for moderation)
        elif cmd == "!fnick":
            if idarg == "":
                 send_my_message(message.channel, "You need to mention the user whose nick you want to change.")
                 return
            if idarg not in condict:
                 send_my_message(message.channel, "That user doesn't have a client. Did you mean !fjoinirc ?")
                 return
            if len(contentsplit) < 3:
                 send_my_message(message.channel, "Usage: !fnick @mention_here new_nick_here")
                 return
            urequest = contentsplit[2]
            ucon = condict[idarg].conn
            uconick = ucon.get_nickname()
            if urequest == uconick or urequest + "[R]" == uconick:
                send_my_message(message.channel, "User is already using " + urequest + " (" + uconick + ") on IRC.")
                return
            if urequest + "[R]" in classcon.botdict or urequest + "[R]_" in classcon.botdict or urequest in classcon.botdict:
                send_my_message(message.channel, "Another Discord User is using a simular/the same nick, please choose another one to avoid confusion.")
                return
            ucon.nick(urequest + "[R]")
            classcon.savedclients.pop(idarg)
            classcon.savedclients[idarg] = {}
            classcon.savedclients[idarg]["nick"] = urequest + "[R]"
            settings.saveclients(classcon.savedclients)
            return

        #whois command - Shows what nick a Discord user is using on IRC (used for moderation)
        elif cmd == "!whois":
            if idarg == "":
                send_my_message(message.channel, "You need to mention a user.")
                return
            if idarg not in condict:
                if idarg in classcon.savedclients:
                    send_my_message(message.channel, "This user doesn't have a connected client at the moment, but the nick i have saved for them is: " + classcon.savedclients[idarg]["nick"])
                    return
                else:
                    send_my_message(message.channel, "This user doesn't have a connected client and there's no saved client for them")
                    return
            else:
                send_my_message(message.channel, "This user's IRC nick is: " + str(classcon.find_nick_by_id(idarg)))
                return

        #fleavechan command - User's IRC client leaves the IRC channel matching the Discord channel.
        elif cmd == "!fleavechan" or cmd == "!flvchan":
            if idarg == "":
                send_my_message(message.channel, "You need to mention a user as an argument to this command. \n e.g " + cmd + " @mention-here")
            if idarg not in condict:
                send_my_message(message.channel, "User has no client connected. Did you mean: !fjoinirc ?")
                return
            ucon = condict[idarg].conn
            irc_nick = ucon.get_nickname()
            check_ison_chan = classcon.ison_chan(irc_chan, irc_nick)
            if check_ison_chan == False:
                send_my_message(message.channel, "User is not in" + irc_chan + " in IRC.")
                return
            reason = ""
            if len(contentsplit) > 1:
                reason = "Reason: " + ' '.join(contentsplit[1:])
            ucon.part(irc_chan, "Client removed from " + irc_chan + " by botop: " + message.author.name + " " + reason)
            savedchans = classcon.savedclients[idarg]["channels"]
            if irc_chan in savedchans:
                savedchans.remove(irc_chan)
            settings.saveclients(classcon.savedclients)
            leftirc_chan[irc_chan].append(idarg)

    #public commands block

    #joinirc command - Creates an IRC client if the user doesn't already have one and their username/desired nick is acceptable.
    # If the user already has an IRC client, checks if it's in the correspondimg IRC channel.
    # If not it saves the channel on the user's saved channels and joins the channel.
    if (cmd == "!joinirc" and AUTOCLIENTS == False) or (cmd == "!joinirc" and AUTOCLIENTS == True and (authorid in leftirc or authorid in leftirc_chan[irc_chan])):
        usenick = message.author.name
        join_chans = [irc_chan]
        if "--nick" in contentsplit:
            contentsplit.remove("--nick")
            if message.author.nick:
                usenick = message.author.nick.replace(" ", "_")
        if "--all" in contentsplit:
            contentsplit.remove("--all")
            if authorid in classcon.savedclients:
                join_chans = classcon.savedclients[authorid]["channels"]
            else:
                join_chans = [irc_chan]
        if classcon.mom.is_connected() == False:
            send_my_message(message.channel, "Central bot is currently disconnected from IRC, please wait and try again.")
            return

        if authorid in condict:
            ucon = condict[authorid].conn
            irc_nick = ucon.get_nickname()
            check_ison_chan = classcon.ison_chan(irc_chan, irc_nick)
            if check_ison_chan == False:
                ucon.join(irc_chan)
                savedchans = classcon.savedclients[authorid]["channels"]
                if irc_chan not in savedchans:
                    savedchans.append(irc_chan)
                    settings.saveclients(classcon.savedclients)
                return
            else:
                send_my_message(message.channel, "You have already joined " + irc_chan + " on IRC.")
                return

        if authorid in killed:
            ctime = round(time.time(), 0)
            timediff = ctime - killed[authorid]
            if timediff < TIMEKILLED or TIMEKILLED == 0:
                if TIMEKILLED == 0:
                    killtimeleft = "Permanent"
                else:
                    killtimeleft = TIMEKILLED - timediff
                send_my_message(message.channel, "Your client has been killed by a botop (" + str(killtimeleft) + " secs left)")
                return
            else:
                killed.pop(authorid)

        if len(contentsplit) > 1 and idarg == "":
            checknick = fixnick(contentsplit[1])
        else:
            if authorid in classcon.savedclients:
                checknick = classcon.savedclients[authorid]["nick"]
                checknick = checknick[0:len(checknick)-3]
            else:
                checknick = fixnick(usenick)

        if checknick == False:
            send_my_message(message.channel, "**Error**: Your IRC nick can only contain A-Z a-z 0-9, your current username or requested nick cannot be used!")
            return
        if checknick + "[R]" in classcon.botdict or checknick + "_[R]" in classcon.botdict or checknick in classcon.botdict:
            send_my_message(message.channel, "**Error**: Another Discord User is using this nick, please provide another to avoid confusion with simular nicks.")
            return

        if authorid not in condict:
            newclient = classcon.IRCbots(checknick + "[R]", IRCSERVER, IRCPORT, join_chans, None, False, authorid)
            newclientcon = newclient.conn
            condict[authorid] = newclient
            newclient.connect()
            if authorid in leftirc:
                leftirc.pop(authorid)
            return

    #bridgeuptime commmand - Simply sends the bot's uptime to Discord and IRC.
    elif cmd == "!bridgeuptime":
        senduptime(message.channel, irc_chan)
        return

    elif cmd == "!bridgehelp":
        if len(contentsplit) == 1:
            send_my_message(message.channel, help["listcommands"])
        else:
            if contentsplit[1] in help:
                send_my_message(message.channel, help[contentsplit[1]])
            else:
                send_my_message(message.channel, "Invalid parameter. Use '!bridgehelp listcommands' to see a list of commands you can get help for.")
        return

    #leaveirc command - Disconnects the user's client from IRC, to get it back they must user !joinirc (wether AUTOCLIENTS is on or off)
    elif cmd == "!leaveirc" or cmd == "!quitirc":
        if authorid not in condict:
            send_my_message(message.channel, "You don't have a client connected. Did you mean: !joinirc ? :smirk:")
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
        leftirc[authorid] = 1
        return

    #leavechan command - User's IRC client leaves the IRC channel matching the Discord channel.
    if cmd == "!leavechan":
        if authorid not in condict:
            send_my_message(message.channel, "You don't have a client connected. Did you mean: !joinirc ?")
            return
        ucon = condict[authorid].conn
        irc_nick = ucon.get_nickname()
        check_ison_chan = classcon.ison_chan(irc_chan, irc_nick)
        if check_ison_chan == False:
            send_my_message(message.channel, "You haven't joined " + irc_chan + " in IRC.")
            return
        reason = ""
        if len(contentsplit) > 1:
            reason = "Reason: " + ' '.join(contentsplit[1:])
        ucon.part(irc_chan, "Client removed from " + irc_chan + " by user. " + reason)
        savedchans = classcon.savedclients[authorid]["channels"]
        if irc_chan in savedchans:
            savedchans.remove(irc_chan)
        settings.saveclients(classcon.savedclients)
        leftirc_chan[irc_chan].append(authorid)

    #nick command - If the user has a client, changes its nick to the provided one. (if the nick isn't used)
    elif cmd == "!nick":
        if NICKCHANGE == False:
            return
        if authorid not in condict:
            send_my_message(message.channel, "You don't have a client connected. Did you mean: !joinirc")
            return
        if len(contentsplit) == 1:
            send_my_message(message.channel, "Usage: !nick <nickhere>")
            return
        urequest = contentsplit[1]
        ucon = condict[authorid].conn
        uconick = ucon.get_nickname()
        if urequest == uconick or urequest + "[R]" == uconick:
            send_my_message(message.channel, "You are already using " + urequest + " (" + uconick + ") on IRC.")
            return
        if urequest + "[R]" in classcon.botdict or urequest + "[R]_" in classcon.botdict or urequest in classcon.botdict:
            send_my_message(message.channel, "Another Discord User is using a simular/the same nick, please choose another one to avoid confusion")
            return
        ucon.nick(urequest + "[R]")
        classcon.savedclients[authorid]["nick"] = urequest + "[R]"
        settings.saveclients(classcon.savedclients)
        return

    #whoami command - Shows a Discord user their IRC nick
    elif cmd == "!whoami":
        if authorid not in condict:
            if authorid in classcon.savedclients:
                send_my_message(message.channel, "You don't have a connected client at the moment, but the nick i have saved for you is: " + classcon.savedclients[authorid]["nick"])
                return
            else:
                send_my_message(message.channel, "You don't have a connected client and there's no saved client for you.")
                return
        send_my_message(message.channel, "Your IRC nick is: " + str(classcon.find_nick_by_id(authorid)))
        return

    #public commands close block
    if authorid in condict:
        if action_msg == False:
            condict[authorid].sendmsg(irc_chan, ircdressup(content))
        else:
            condict[authorid].sendmsg(irc_chan, ircdressup(content), True)


    with thread_lock:
        print("[Discord] " + message.channel.name + " > " + irc_chan + " " + message.author.name + ": " + content)

def run():
    bot.run(TOKEN, log_handler=handler, log_level=logging.ERROR)

@bot.event
async def on_ready():
    global channel_sets
    global thread_lock
    global condict
    global savedclients

    with thread_lock:
        print("[Discord] Logged in as:")
        print("[Discord] " + bot.user.name)
        print("[Discord] " + str(bot.user.id))

        if len(bot.guilds) == 0:
            print("[Discord] Bot is not yet in any server.")
            await bot.close()
            return

        if DISCORDSERVER == "":
            print("[Discord] You have not configured a server to use in the config, please run: python3 setupwizard.py")
            print("[Discord] Input one of the ID's below when you are asked for the Discord Server ID")

            for server in bot.guilds:
                print("[Discord] %s: %s" % (server.name, server.id))

            await bot.close()
            return

        findServer = [x for x in bot.guilds if str(x.id) == DISCORDSERVER]
        if not len(findServer):
            print("[Discord] No server could be found with the specified id: " + DISCORDSERVER)
            print("[Discord] Available servers:")
            for server in bot.guilds:
                print("[Discord] %s: %s" % (server.name, server.id))
            await bot.close()
            return

        server = findServer[0]

        if channel_sets == {}:
            print("[Discord] You have not configured any channels sets. Please run python3 setupwizard.py")
            print("[Discord] Input one of the channel IDs listed below when asked for channel ID")
            for channel in server.channels:
                if channel.type == discord.ChannelType.text:
                    print("[Discord] %s: %s" % (channel.name, channel.id))

            await bot.close()
            return

        for item in channel_sets:
            findChannel = [x for x in server.channels if str(x.id) == item and x.type == discord.ChannelType.text]
            if not len(findChannel):
                print("[Discord] No channel could be found with the specified id: " + item)
                print("[Discord] Note that you can only use text channels.")
                print("[Discord] Available channels:")

                for channel in server.channels:
                    if channel.type == discord.ChannelType.text:
                        print("[Discord] %s: %s" % (channel.name, channel.id))

                print("You can edit this channel set by running setupwizard.py")
                await bot.close()
                return
            channel_sets[item]["real_chan"] = findChannel[0]
    classcon.set_channel_sets(channel_sets)
    if savedclients != {}:
        for savedclient in savedclients:
            checkmember = is_member(savedclient)
            if checkmember != None:
                newclient = classcon.IRCbots(savedclients[savedclient]["nick"], IRCSERVER, IRCPORT, savedclients[savedclient]["channels"], None, False, savedclient)
                condict[savedclient] = newclient
