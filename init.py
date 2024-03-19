# !/usr/bin/python
import errno
import random
import shc
import os
import sys
import signal
from datetime import datetime
from src import Logger
import enum
import shc
import os
from shc.web import WebServer
from shc.datatypes import *
from shc.web.widgets import *

global PWD
PWD = os.getcwd()
LOGDIR = PWD + "/log"
CURRENTTIME = datetime.now().strftime("%Y%m%d%H%M%S")
LOGFILE = LOGDIR + "/" + CURRENTTIME + ".log"

isLogDir = os.path.exists(LOGDIR)

LOG = Logger.TimestampLogger()

if isLogDir:
    msg = "Log is goint to be logged in " + LOGFILE + "\n"
    LOG.print(msg)
else:
    msg = "./log is incorrect form, trying to fix \n"
    LOG.print(msg)
    try:
        os.remove(LOGDIR)
    except OSError as e:
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise e # re-raise exception if a different error occurred
    except:
        print("Something else went wrong")
        raise
    finally:
        os.makedirs(LOGDIR, exist_ok=True)
        msg = "log directory created \n"
        LOG.print(msg)

# set up Device types
speaker = shc.Variable(bool, 'speaker', initial_value=False)
camera = shc.Variable(bool, 'camera', initial_value=False)
switch = shc.Variable(bool, 'switch', initial_value=False)
theromostat = shc.Variable(float, 'theromostat', initial_value=20.0)
dimmer = shc.Variable(RangeFloat1, 'dimmer', initial_value=0)
neon_light = shc.Variable(RGBUInt8, 'neon_light', initial_value=RGBUInt8(RangeUInt8(0), RangeUInt8(0), RangeUInt8(0)))
fan = shc.Variable(bool, 'Fan', initial_value=False)
temperture = shc.Variable(float, 'temperture', initial_value=16.0)
humidity = shc.Variable(RangeInt0To100, 'humidity', initial_value=0)

# set up enum devices
# not yet implimented
class Devices(enum.Enum):
    phone = 0
    pad = 1
    laptop = 2
    pc = 3
    tv = 4

currentDevice = shc.Variable(Devices, 'Devices', initial_value=Devices.pc)

# start httpserver
# Define server main function and child components
# WebServer running at port 8080
web_server = WebServer('localhost', 8080, index_name='index')

# Page index (Home)
index_page = web_server.page('index', 'Home', menu_entry=True, menu_icon='home')

# device selection bar
index_page.add_item(EnumSelect(Devices, "Device connected selection").connect(currentDevice))

# Toggle button bar
index_page.add_item(ButtonGroup("State of the Device", [
    ToggleButton(speaker.name).connect(speaker),
    # Foobar requires confirmation when switched on.
    ToggleButton(camera.name, color='black',
                confirm_message="Do you want the camera on?", confirm_values=[True]).connect(camera),
]))
# We can also use ValueButtons to represent individual states (here in the 'outline' version)
index_page.add_item(ButtonGroup("Thermostat", [
    ValueButton(False, "Off", outline=True, color="black").connect(fan),
    ValueButton(True, "On", outline=True).connect(fan),
    TextInput(float, icon('temperature high', "{} ") + theromostat.name, min=16.0, max=36.0, step=0.5, input_suffix="°C").connect(temperture),
    TextDisplay(int, icon('tint', "{} "), humidity.name).connect(humidity)
]))

# Another segment in the right column
# color light bulb
index_page.new_segment("The neon light bulb with dimmer")

index_page.add_item(Switch(switch.name, color='red').connect(switch))
index_page.add_item(ColorChoser().connect(neon_light))
magic_button = StatelessButton(None, label=icon('magic'), color="orange")
index_page.add_item(ButtonGroup("Supprise!", [magic_button]))

# Trigger to randomize color
@magic_button.trigger
@shc.handler()
async def do_rand(_v, _o) -> None:
    await neon_light.write(RGBUInt8(RangeUInt8(random.randint(0, 255)), RangeUInt8(random.randint(0, 255)), RangeUInt8(random.randint(0, 255))))

index_page.add_item(MinMaxButtonSlider(dimmer.name, color='black').connect(dimmer))

# Overview page
overview_page = web_server.page('overview', "Overview", menu_entry='Some Submenu', menu_icon='tachometer alternate',
                                menu_sub_label="Overview")

# ImageMap supports all the different Buttons as items, as well as the special ImageMapLabel
# The optional fourth entry of each item is a list of WebPageItems (everything we have shown so far – even an ImageMap))
# to be placed in a popup shown when the item is clicked.
overview_page.add_item(ImageMap(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Newburn_Flats_Floor_Plan.pdf"
    "/page1-543px-Newburn_Flats_Floor_Plan.pdf.jpg",
    [
        (0.20, 0.30, ToggleButton(switch.name, outline=True).connect(switch)),
        (0.33, 0.30, ToggleButton(fan.name, color='red', outline=True).connect(fan)),
        # camera requires confirmation when switched on.
        (0.67, 0.30, ToggleButton(camera.name, color='black', outline=True,
                                  confirm_message="Do you want the camera on?", confirm_values=[True]).connect(camera)),

        (0.26, 0.42, ToggleButton(label=icon('volume up icon'), color="red").connect(speaker)),
        (0.67, 0.42, ToggleButton(label=icon('volume up icon'), color="red").connect(speaker)),

        # We use the RangeFloat1 → bool conversion here to highlight the button with the popup, whenever the dimmer
        # value is > 0. To use another condition, you can pass a (lambda) function to the `convert` parameter
        (0.42, 0.52, DisplayButton(label=icon('lightbulb outline icon'), color="black").connect(dimmer, convert=True), [
            Slider(dimmer.name).connect(dimmer)
        ]),
    ]
))

overview_page.new_segment()
overview_page.add_item(HideRowBox([
    TextDisplay(str, "Device that has powered up", " List view"),
    HideRow(speaker.name, color='blue').connect(speaker),
    HideRow(fan.name, color='red').connect(fan),
    HideRow(dimmer.name, color='green').connect(dimmer),
    # The optional button in the HideRow is completely independent from the row itself. Thus, we must connect the camera
    # variable individually to the button and to the HideRow
    HideRow(camera.name, color='black', button=StatelessButton(False, icon('power off'), color='red').connect(camera))
    .connect(camera),
]))

# TODO
# furrther action need async action taker to connect to devices.
# markup the device with syntax of lambda functions like the followint 
# @magic_button.trigger
# @shc.handler()
# async def do_rand(_v, _o) -> None:

# TODO
# devices should be in seprate py file.

# Startup the deamon by shc.main() and preform clean exit after daemon has closed
sys.exit(shc.main())
