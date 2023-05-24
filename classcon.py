from discord_webhook import DiscordWebhook
import irc.client
import time
reactor = irc.client.Reactor()
irc.client.ServerConnection.buffer_class.encoding = "UTF-8"
irc.client.ServerConnection.buffer_class.errors = "replace"
loopin = 0
botdict = {}
network = ""

def set_chan(chan, wh):
    global channel
    global webhooklink
    channel = chan
    webhooklink = wh

def startloop(nick, server, prt, ch, wh):
    global start_time
    start_time = int(time.time())
    global mom
    global momobj
    momobj = IRCbots(nick, server, prt, ch, True, wh)
    mom = momobj.conn
    set_chan(ch, wh)
    momobj.connect()
    global loopin
    loopin = 1
    while loopin:
        reactor.process_once(0.2)
        time.sleep(0.2)

def stoploop():
    global loopin
    loopin = 0

def set_discord(disc):
    global discord
    discord = disc

def set_thread_lock(lock):
    global thread_lock
    thread_lock = lock

def momsendmsg(message):
    global momobj
    momobj.sendmsg(message)

def get_start_time():
    global start_time
    return start_time

def get_uptime():
    uptime = int(time.time()) - get_start_time()
    day = uptime // (24 * 3600)
    uptime = uptime % (24 * 3600)
    hour = uptime // 3600
    uptime %= 3600
    minutes = uptime // 60
    uptime %= 60
    seconds = uptime
    result = "%sd%sh%sm%s" % (day, hour, minutes, seconds)
    result = result + "s"
    return result

def on_connectbot(connection, event):
    global botdict
    global mom
    global channel
    if connection != mom:
        botdict[connection.get_nickname()] = connection.discordid
        print(botdict)
    elif connection == mom:
        discord.setstatus()
    connection.join(channel)


def on_nicknameinuse(connection, event):
    x = connection.get_nickname() + "_"
    connection.nick(x)

def on_pubmsg(connection, event):
    global botdict
    global channel
    global webhooklink
    global discord
    global thread_lock
    if event.target != channel:
        return
    if connection != mom:
        return
    sender = event.source.nick
    if sender in botdict:
        return
    host = event.source.host
    messagenot = event.arguments[0]
    message = messagenot.split()
    if message[0] == "!uptime":
        uptime = get_uptime()
        momsendmsg("I've been running for " + uptime)
        discord.send_my_message("I've been running for  " + uptime)
    for i in range(len(message)):
        msgi = message[i]
        msgii = msgi[:-1]
        ml = [msgi, msgii]
        check_dict = [msgi in botdict, msgii in botdict]
        if any(check_dict):
            message[i] = "<@" + botdict[ml[check_dict.index(True)]] + ">"
    finalmsg = ' '.join(message)
    if event.type == "action":
        finalmsg = "*" + finalmsg + "*"
    with thread_lock:
        print("[IRC]", sender, ":", finalmsg)
    webhook = DiscordWebhook(url=webhooklink, content=finalmsg, username=sender + "_[IRC]")
    response = webhook.execute()

def on_join(connection, event):
    global mom
    global channel
    global discord
    if event.target != channel:
        connection.part(event.target)
        return
    if connection != mom:
        return
    if connection.get_nickname() != event.source.nick:
        discord.send_my_message("-> **" + event.source.nick + " joined " + event.target + "**")
    else:
        time.sleep(5)
        discord.send_my_message("**Relay is up, do !joinirc to get a client**")

def on_part(connection, event):
    if event.target != channel:
        return
    if connection != mom:
        return
    if connection.get_nickname() != event.source.nick:
        discord.send_my_message("<- **" + event.source.nick + " left " + event.target + "**")
    else:
        connection.join(channel)

def on_quit(connection, event):
    if connection != mom:
         return
    if event.arguments[0]:
         reason = "(" + event.arguments[0] + ")"
    else:
         reason = ""
    discord.send_my_message("<- **" + event.source.nick + " quit " + network + " " + reason + "**")

def on_kick(connection, event):
    nick = event.source.nick
    knick = event.arguments[0]
    if event.target != channel:
        return
    if connection == mom:
        try:
            extras = "(" + event.arguments[1] + ")"
        except IndexError:
            extras = ""
        discord.send_my_message("**%s kicked %s %s**" % (nick, knick, extras))
        if knick == connection.get_nickname():
             time.sleep(2)
             connection.join(channel)
    else:
        if knick == connection.get_nickname():
            time.sleep(2)
            connection.join(channel)

def on_featurelist(connection, event):
    if connection != mom:
        return
    global network
    featlen = len(event.arguments)
    for i in range(featlen):
        ce = event.arguments[i]
        spl = ce.split("=")
        if spl[0] == "NETWORK":
            network = spl[1]

def on_nick(connection, event):
    if connection != mom:
        return
    nick = event.source.nick
    host = event.source.host
    newnick = event.target
    event_msg = "**%s** *is now known as* **%s**" % (nick, newnick)
    discord.send_my_message(event_msg)

class IRCbots():
    def __init__(self, nik, srv, prt, ch, mom=False, wh=None, discordid=None):
        self.nick = nik
        self.server = srv
        self.port = prt
        self.chan = ch
        self.conn = reactor.server()
        if discordid:
            self.conn.discordid = discordid
        else:
            self.conn.discordid = "Relay Mother Bot"
        if mom == True:
            self.mother = self.conn
        else:
            self.mother = None
        if wh:
            self.webhook = wh
        else:
            self.webhook = None

    def connect(self):
        c = self.conn.connect(self.server, self.port, self.nick, None, "Discord", self.conn.discordid)
        if self.mother:
            c.add_global_handler("pubmsg", on_pubmsg)
            c.add_global_handler("join", on_join)
            c.add_global_handler("part", on_part)
            c.add_global_handler("action", on_pubmsg)
            c.add_global_handler("quit", on_quit)
            c.add_global_handler("welcome", on_connectbot)
            c.add_global_handler("nicknameinuse", on_nicknameinuse)
            c.add_global_handler("kick", on_kick)
            c.add_global_handler("featurelist", on_featurelist)
            c.add_global_handler("nick", on_nick)

    def sendmsg(self, msg):
        if self.conn.is_connected() == False:
            return
        self.conn.privmsg(channel, msg)
