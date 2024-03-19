# Depretaed
# to be removed in future commit
# !/usr/bin/python
import multiprocessing
import enum
import shc
import os
from shc.web import WebServer
from shc.datatypes import *
from shc.web.widgets import *

# set up Device types
speaker = shc.Variable(bool, 'speaker', initial_value=False)
camera = shc.Variable(bool, 'camera', initial_value=False)
switch = shc.Variable(bool, 'switch', initial_value=False)
theromostat = shc.Variable(float, 'theromostat', initial_value=20.0)
dimmer = shc.Variable(RangeUInt8, 'dimmer', initial_value=0)
neon_light = shc.Variable(RGBUInt8, 'neon_light', initial_value=RGBUInt8(RangeUInt8(0), RangeUInt8(0), RangeUInt8(0)))

# Define server main function and child components
def server(logFile):
    # WebServer running at port 8080
    server = WebServer('localhost', 8080, index_name='UHAP')

    state_variable = shc.Variable(bool, initial_value=False)

    # .connect() returns the object itself after connecting; so we can do connecting to the variable and adding to the
    # web page in a single line
    index_page.add_item(Switch(label="Foobar on/off").connect(state_variable))

    index_page.new_segment()

    # `ButtonGroup` is not connectable itself, but it takes a list of connectable Button spec objects
    index_page.add_item(ButtonGroup(label="Foobar on/off again", buttons=[
        ToggleButton(icon('power off')).connect(state_variable)
    ]))

    # Page index (Home)
    index_page = server.page('index', 'Home', menu_entry=True, menu_icon='home')

    #initialize state of devices
    states = devices.Interacts()
    
    # Toggle button bar
    index_page.add_item(ButtonGroup("State of the Device", [
        ToggleButton(states.speaker.name).connect(states.speaker),
        ToggleButton(states.switch.name, color='red').connect(states.switch),
        # Foobar requires confirmation when switched on.
        ToggleButton(states.camera.name, color='black',
                    confirm_message="Do you want the camera on?", confirm_values=[True]).connect(states.camera),
    ]))

    # We can also use ValueButtons to represent individual states (here in the 'outline' version)
    index_page.add_item(ButtonGroup("The Foo", [
        ValueButton(False, "Off", outline=True, color="black").connect(states.switch),
        ValueButton(True, "On", outline=True).connect(states.switch),
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

def __init__(arg):
    server("running.log")
    return

if __name__ == '__main__':
    shc.main()
