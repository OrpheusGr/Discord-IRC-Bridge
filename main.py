import json
import threading

#from classcon import *
#from discordc import *
import discordc
import classcon

thread_lock = threading.Lock()

classcon.set_discord(discordc)
discordc.set_classcon(classcon)

classcon.set_thread_lock(thread_lock)
discordc.set_thread_lock(thread_lock)

t1 = threading.Thread(target=classcon.startloop, args=("Relay", discordc.IRCSERVER, discordc.IRCPORT, discordc.IRCCHAN, discordc.WEBHOOK))
t1.daemon = True
t1.start()

discordc.run()
classcon.stoploop()
