import threading
import sys
import discordc
import classcon
import logging

logger_classcon = logging.getLogger('classcon')
logger_classcon.setLevel(logging.ERROR)

# Create a FileHandler for logging to a file
file_handler = logging.FileHandler('classcon_errors.log')  # Log to this file
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger_classcon.addHandler(file_handler)

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
