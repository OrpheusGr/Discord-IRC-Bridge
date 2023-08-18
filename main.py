import threading
import sys
import discordc
import classcon

thread_lock = threading.Lock()

classcon.set_discord(discordc)
discordc.set_classcon(classcon)

classcon.set_thread_lock(thread_lock)
discordc.set_thread_lock(thread_lock)

t1 = threading.Thread(target=classcon.startloop, args=(discordc.IRCNICK, discordc.IRCSERVER, discordc.IRCPORT))
t1.daemon = True
t1.start()

discordc.run()
classcon.stoploop()
