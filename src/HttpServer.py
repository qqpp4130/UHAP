# !/usr/bin/python
import multiprocessing
import shc
import os
from shc.web import WebServer
from shc.web.widgets import ButtonGroup, Switch, ToggleButton, icon

def server(logFile):
    server = WebServer('localhost', 8080)
    index_page = server.page('index', "Main page")

    state_variable = shc.Variable(bool, initial_value=False)

    # .connect() returns the object itself after connecting; so we can do connecting to the variable and adding to the
    # web page in a single line
    index_page.add_item(Switch(label="Foobar on/off").connect(state_variable))

    index_page.new_segment()

    # `ButtonGroup` is not connectable itself, but it takes a list of connectable Button spec objects
    index_page.add_item(ButtonGroup(label="Foobar on/off again", buttons=[
        ToggleButton(icon('power off')).connect(state_variable)
    ]))

def start_server(logFile):
    p = multiprocessing.Process(target=server, args=("2 > " + logFile,))
    # you have to set daemon true to not have to wait for the process to join
    p.daemon = True
    p.start()
    # Get the process ID of 
    # the current process 
    pid = os.getpid() 
    return pid