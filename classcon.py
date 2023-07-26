from discord_webhook import DiscordWebhook
import irc.client
import time
import re
import settings
reactor = irc.client.Reactor()
irc.client.ServerConnection.buffer_class.encoding = "utf-8"
irc.client.ServerConnection.buffer_class.errors = "replace"
loopin = 0
botdict = {}
network = ""
disconnectretries = 0
quitf = {}
savedclients = {}

# Load the config
def load_the_config():
    global savedclients
    config = settings.load_config()
    savedclients = settings.load_saved_clients()
    if config == False:
        sys.exit(0)
    else:
        for item in config:
            globals()[item] = config[item]


load_the_config()

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
    time.sleep(15)
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

def sendtoboth(message):
    time.sleep(1)
    momsendmsg(message)
    discord.send_my_message(message)

def get_start_time():
    global start_time
    return start_time

def get_uptime():
    result = ""
    uptime = int(time.time()) - get_start_time()
    day = uptime // (24 * 3600)
    uptime = uptime % (24 * 3600)
    hour = uptime // 3600
    uptime %= 3600
    minutes = uptime // 60
    uptime %= 60
    seconds = uptime
    if day > 0:
        result += str(day) + "d "
    if hour > 0:
        result += str(hour) + "h "
    if minutes > 0:
        result += str(minutes) + "m "
    if seconds > 0:
        result += str(seconds) + "s "
    return result

def IrcToDiscText(message):
    bold_italic = 0
    regexc = re.compile(chr(3) + "(\d{,2}(,\d{,2})?)?", re.UNICODE)
    message = message.replace("\x1d", "\\x1d")
    msplit = message.split()
    for i in range(len(msplit)):
        mi = msplit[i]
        if mi.startswith("http") or mi.startswith("<http"):
            msplit[i] = mi.replace("_", "pholderunderdash95130")
    message = " ".join(msplit)
    message = message.replace(r"\x31", "")
    message = message.replace("\x0f", "")
    message = message.replace(chr(2) + chr(29), "***")
    message = message.replace(chr(29) + chr(2), "***")
    message = message.replace(chr(2), "**")
    if message.count(chr(29)) % 2 != 0:
        message = message + " " + chr(29)
    message = message.replace("\\x1d", "_")
    message = regexc.sub("", message)
    if message.count("***") % 2 != 0:
        message = message + "***"
        bold_italic = 1
    if message.count("**") % 2 != 0:
        if bold_italic == 0:
            message = message + "**"
    message = message.replace("pholderunderdash95130", "_")
    return message

def split_msg(msg, max_chars):
    piece = ""
    all_pieces = []
    msgsplit = re.split('\s+(?=\x1d)', msg)
    if len(msgsplit) == 1 and len(msgsplit[0]) > max_chars:
        msgsplit = [msgsplit[0][0:max_chars], msgsplit[0][max_chars:]]
    i = 0
    while i < len(msgsplit):
        if piece != "":
            to_be_piece = piece + " " + msgsplit[i]
        else:
            to_be_piece = piece + msgsplit[i]
        if len(piece) <= max_chars and len(to_be_piece) <= max_chars:
            piece = to_be_piece
        else:
            if piece == "":
                msgsplit = msgsplit[0:i-1] + [to_be_piece[0:max_chars], to_be_piece[max_chars:]] + msgsplit[i+1:]
                piece = msgsplit[i-1]
            all_pieces.append([piece])
            piece = ""
            i -= 1
        i += 1
    all_pieces.append([piece])
    return all_pieces

def find_nick_by_id(uid):
    for i in botdict:
        if botdict[i] == uid:
            return i
    return False

def on_connectbot(connection, event):
    global botdict
    global mom
    global channel
    global disconnectretries
    disconnectretries = 0
    if connection != mom:
        botdict[connection.get_nickname()] = connection.discordid
        member = discord.is_member(connection.discordid)
        if member != None:
            raw_status = member.raw_status
            if raw_status != "online":
                ucon = discord.condict[connection.discordid]
                ucon.set_away("Discord Status: " + raw_status)
    elif connection == mom:
        print("[IRC] Successful connection to", event.source)
        for client in discord.condict:
            discord.condict[client].connect()
        time.sleep(2)
        discord.setstatus()
    connection.join(channel)


def on_nicknameinuse(connection, event):
    cnick = connection.get_nickname()
    if cnick[-3:] == "[R]":
        newnick = cnick[0:len(cnick)-3] + "_[R]"
    else:
        newnick = cnick + "_"
    connection.nick(newnick)

def on_pubmsg(connection, event):
    global botdict
    global channel
    global webhooklink
    global discord
    global thread_lock
    if len(event.arguments[0].split()) == 0:
        return
    if event.target != channel:
        return
    if connection != mom:
        return
    sender = event.source.nick
    if sender in botdict:
        return
    host = event.source.host
    messagenot = IrcToDiscText(event.arguments[0])
    message = messagenot.split()
    if len(message) == 0:
        return
    cmd = message[0].lower()
    #public commands block
    if cmd == "!relayuptime":
        uptime = get_uptime()
        sendtoboth("I've been running for " + uptime)
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
    webhook = DiscordWebhook(url=webhooklink, content=finalmsg, username=sender + " [IRC]")
    response = webhook.execute()
    #IRC bot ops commands block
    if sender in IRCBOTOPS:
        if cmd == "!shutdown":
            uptime = get_uptime()
            discord.send_my_message("**Shutdown request by " +  sender + " on IRC. I was alive for " + uptime + "**")
            time.sleep(2)
            discord.shutdown(0, sender, "on IRC")
            stoploop()

def on_join(connection, event):
    global mom
    global channel
    global discord
    connection_name = connection.get_nickname()
    if event.target != channel:
        connection.part(event.target)
        return
    if connection != mom:
        return
    if connection_name != event.source.nick:
        if event.source.nick in botdict:
            did = botdict[event.source.nick]
            conobj = discord.condict[did]
            conobj.myprivmsg_line = event.source + " PRIVMSG " + channel + " :"
        discord.send_my_message("-> **" + event.source.nick + " joined " + event.target + "**")
    else:
        momobj.myprivmsg_line = event.source + " PRIVMSG " + channel + " :"
        time.sleep(2)
        with thread_lock:
             print("[IRC] Joined", channel)
        if AUTOCLIENTS != True:
            joinmsg = "**Relay is up, do !joinirc to get a client!**"
        else:
            joinmsg = "**Relay is up!**"
        discord.send_my_message(joinmsg)
        '''
        if savedclients != {}:
            for client in savedclients:
                time.sleep(3)
                checkmember = discord.is_member(client)
                if checkmember != None:
                    newclient = IRCbots(savedclients[client], IRCSERVER, IRCPORT, IRCCHAN, None, False, client)
                    newclientcon = newclient.conn
                    discord.condict[client] = newclient
                    newclient.connect()
        '''

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
    global botdict
    if connection != mom:
        return
    nick = event.source.nick
    host = event.source.host
    newnick = event.target
    if nick in botdict:
        x = botdict[nick]
        botdict.pop(nick)
        botdict[newnick] = x
        conobj = discord.condict[x]
        conobj.myprivmsg_line = newnick + "".join(event.source.split("!")[1:]) + " PRIVMSG " + channel + " :"
    else:
        if connection.get_nickname() == event.source.nick:
            momobj.myprivmsg_line = event.source + " PRIVMSG " + channel + " :"
    event_msg = "**%s** *is now known as* **%s**" % (nick, newnick)
    discord.send_my_message(event_msg)

def on_disconnect(connection, event):
    connection_name = connection.get_nickname()
    if connection == mom:
        if momobj.sent_quit == 1:
             momobj.sent_quit = 0
             return
        global disconnectretries
        disconnectretries += 1
        if disconnectretries == 3:
             discord.send_my_message("Retried  3 times, cannot connect to " + event.source + " " + event.arguments[0] + " Closing process.")
             time.sleep(1)
             discord.shutdown()
             stoploop()
             return
        connection.reconnect()
        return
    if connection.sent_quit != 1:
        discord.send_my_message("<@" + connection.discordid + ">" + " Unexpectedly disconnected from " + event.source + " " + event.arguments[0])
    if connection.discordid in discord.condict:
        obj = discord.condict[connection.discordid]
        del obj
        discord.condict.pop(connection.discordid)
    cn = connection.get_nickname()
    if cn in botdict:
        botdict.pop(connection.get_nickname())

def on_error(connection, event):
    print(event.source, event.arguments)

class IRCbots():
    def __init__(self, nik, srv, prt, ch, mom=False, wh=None, discordid=None):
        self.nick = nik
        self.server = srv
        self.port = prt
        self.chan = ch
        self.conn = reactor.server()
        self.lastmsg = round(time.time(),0)
        self.sent_quit = 0
        if discordid:
            self.conn.discordid = discordid
        else:
            self.conn.discordid = "Relay Mother Bot"
        if mom == True:
            self.mother = self.conn
        else:
            self.mother = None
            self.conn.sent_quit = 0
            self.myprivmsg_line = ""
            savedclients[discordid] = self.nick
            settings.saveclients(savedclients)
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
            c.add_global_handler("disconnect", on_disconnect)
            c.add_global_handler("ping", self.on_ping)
            c.add_global_handler("error", on_error)

    def on_ping(self, connection, event):
        if connection == mom:
            return
        if INACTIVITY > 0:
            timediff = round(time.time(),0) - self.lastmsg
            if timediff >= INACTIVITY:
                setattr(connection, "sent_quit", 1)
                connection.disconnect("Client killed for inactivity")

    def sent_quit_on(self):
        self.sent_quit = 1

    def sendmsg(self, msg, action=False):
        print(msg, repr(msg))
        if self.conn.is_connected() == False:
            return
        msg = split_msg(msg, 512-len(self.myprivmsg_line))
        print(msg[0][0], repr(msg[0][0]))
        self.delay_msg = 0
        for i in range(len(msg)):
            self.delay_msg += 0.5
            time.sleep(self.delay_msg)
            joint = msg[i][0]
            if action == False:
                self.conn.privmsg(channel, joint)
            else:
                self.conn.action(channel, joint)
        self.lastmsg = round(time.time(),0)
        self.delay_msg = 0

    def set_away(self, msg=None):
        if self.conn.is_connected() == False:
            return
        if msg == None:
            self.conn.send_raw("AWAY")
        else:
            self.conn.send_raw("AWAY :" + msg)
