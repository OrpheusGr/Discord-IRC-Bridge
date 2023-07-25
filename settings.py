import os
import pickle

default_values = {"NICKCHANGE": True, "TIMEKILLED": 1, "INACTIVITY": 0, "AUTOCLIENTS": False}

if os.path.isfile("config.pkl") == False:
    open("config.pkl", 'w').close()

if os.path.isfile("savedclients.pkl") == False:
    open("savedclients.pkl", 'w').close()

def save_config():
    global config
    with open('config.pkl', 'wb') as fp:
        pickle.dump(config, fp)

def load_config():
    global config
    missing = 0
    config = {}
    if os.path.getsize('config.pkl') > 0:
        with open('config.pkl', 'rb') as fp:
           config = pickle.load(fp)
    if config == {}:
        print("You have no config file setup. Please run 'python3 setupwizard.py' to create one.")
        return False
    else:
        for item in default_values:
            if item not in config:
                missing = 1
                config[item] = default_values[item]
        if missing == 1:
            save_config()
        return config

def load_saved_clients():
    global savedclients
    savedclients = {}
    if os.path.getsize('savedclients.pkl') > 0:
        with open('savedclients.pkl', 'rb') as fp:
           savedclients = pickle.load(fp)
    return savedclients

def saveclients(clients):
    with open('savedclients.pkl', 'wb') as fp:
        pickle.dump(clients, fp)
