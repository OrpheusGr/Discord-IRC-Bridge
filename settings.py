import os
import pickle

if os.path.isfile("config.pkl") == False:
    open("config.pkl", 'w').close()

def load_config():
    global config
    config = {}
    if os.path.getsize('config.pkl') > 0:
        with open('config.pkl', 'rb') as fp:
           config = pickle.load(fp)
    if config == {}:
        print("You have no config file setup. Please run 'python3 setupwizard.py' to create one.")
        return False
    else:
        return config
