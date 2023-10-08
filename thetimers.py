import time
timers = {}

def check_timers():
    global timers
    for i in timers.copy():
        timer = timers[i]
        timertime = timer["time"]
        currtime = time.time()
        if currtime >= timertime:
            target = timer["target"]
            arguments = timer["arguments"]
            timers.pop(i)
            if arguments != None:
                target(*arguments)
            else:
                target()

def add_timer(name, delay, target, *arguments):
    global timers
    if name in timers:
        raise Exception("a timer with this name already exists")
        return
    currtime = time.time()
    if name == "":
        name = str(currtime)
    if type(delay) != int and type(delay) != float:
         raise TypeError("delay argument is expected to be int or float")
    timetodo = currtime + float(delay)
    timers[name] = {"time": timetodo, "target": target, "arguments": arguments}

def cancel_timer(name):
    global timers
    if name in timers:
        timers.pop(name)
    else:
        raise Exception("No timer with name " + name + " found.")


