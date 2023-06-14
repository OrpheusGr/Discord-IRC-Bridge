import os
import pickle

if os.path.isfile("config.pkl") == False:
    open("config.pkl", 'w').close()

if os.path.isfile("savedclients.pkl") == False:
    open("savedclients.pkl", 'w').close()

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
