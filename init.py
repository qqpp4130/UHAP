# !/usr/bin/python
import errno
import random
import shc
import os
import sys
import signal
from datetime import datetime
from src import Logger
from src import style
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
camera = shc.Variable(bool, 'camera', initial_value=False)

#New device setup scheme. Using class for different type of device and group the arguments together in one shc.Variable
dimmer_light = shc.Variable(style.Switch_Device, "dimmer light", initial_value=style.Switch_Device(False, True, False, 0.0, RGBUInt8(RangeUInt8(0), RangeUInt8(0), RangeUInt8(0))))
thermostat = shc.Variable(style.Thermostat_Device, 'theromostat', initial_value=style.Thermostat_Device(True, False, False, 1.0, 20.0, 35.0, 35.0, 35.0))
multimedia = shc.Variable(style.Multimedia_Device, "speaker", initial_value=style.Multimedia_Device(False, "None", 0.0))
neon_light = shc.Variable(style.Switch_Device, 'neon_light', initial_value=style.Switch_Device(False, False, True, color=RGBUInt8(RangeUInt8(0), RangeUInt8(0), RangeUInt8(0))))

#connect old variable to new form of variable group
speaker = multimedia.field('power')
switch = dimmer_light.field('power')
dimmer = dimmer_light.field('brightness')
fan = thermostat.field('fan')
therometer = thermostat.field('tempadjust')
temperture = thermostat.field('temperature')
humidity = thermostat.field('humidadjust')

# connect the device power with the field converted to bool
dimmer_light.field('power').connect(dimmer_light.field('brightness'), convert=True)
thermostat.field('fan').connect(thermostat.field('level'), convert=True)

# initialilze httpserver object
# Define server main function and child components
# WebServer running at port 8080
web_server = WebServer('localhost', 8080, index_name='index')

# Page index (Home)
index_page = web_server.page('index', 'Home', menu_entry=True, menu_icon='home')

# Toggle button bar
index_page.add_item(ButtonGroup("State of the Device", [
    ToggleButton(speaker.parent.name).connect(speaker),
    # Foobar requires confirmation when switched on.
    ToggleButton(camera.name, color='black',
                confirm_message="Do you want the camera on?", confirm_values=[True]).connect(camera),
]))
# We can also use ValueButtons to represent individual states (here in the 'outline' version)
index_page.add_item(ButtonGroup("Thermostat", [
    ValueButton(False, "Off", outline=True, color="black").connect(fan),
    ValueButton(True, "On", outline=True).connect(fan),
    TextInput(float, icon('temperature high', "{} ") + therometer.parent.name, min=16.0, max=36.0, step=0.5, input_suffix="°C").connect(temperture),
    TextDisplay(RangeFloat1, icon('tint', "{} "), humidity.parent.name).connect(humidity)
]))

# Another segment in the right column
# color light bulb
index_page.new_segment("The neon light bulb with dimmer")

index_page.add_item(Switch(switch.parent.name, color='red').connect(switch))
index_page.add_item(ColorChoser().connect(neon_light.field("color")))
magic_button = StatelessButton(None, label=icon('magic'), color="orange")
index_page.add_item(ButtonGroup("Supprise!", [magic_button]))

# Trigger to randomize color
@magic_button.trigger
@shc.handler()
async def do_rand(_v, _o) -> None:
    await neon_light.write(RGBUInt8(RangeUInt8(random.randint(0, 255)), RangeUInt8(random.randint(0, 255)), RangeUInt8(random.randint(0, 255))))

index_page.add_item(MinMaxButtonSlider(dimmer.parent.name, color='black').connect(dimmer))

# Overview page
overview_page = web_server.page('overview', "Overview", menu_entry='Overview', menu_icon='tachometer alternate',
                                menu_sub_label="Overview")

# ImageMap supports all the different Buttons as items, as well as the special ImageMapLabel
# The optional fourth entry of each item is a list of WebPageItems (everything we have shown so far – even an ImageMap))
# to be placed in a popup shown when the item is clicked.
overview_page.add_item(ImageMap(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Newburn_Flats_Floor_Plan.pdf"
    "/page1-543px-Newburn_Flats_Floor_Plan.pdf.jpg",
    [
        (0.20, 0.30, ToggleButton(switch.parent.name, outline=True).connect(switch)),
        (0.33, 0.30, ToggleButton(fan.parent.name, color='red', outline=True).connect(fan)),
        # camera requires confirmation when switched on.
        (0.67, 0.30, ToggleButton(camera.name, color='black', outline=True,
                                  confirm_message="Do you want the camera on?", confirm_values=[True]).connect(camera)),

        (0.26, 0.42, ToggleButton(label=icon('volume up icon'), color="red").connect(speaker)),
        (0.67, 0.42, ToggleButton(label=icon('volume up icon'), color="red").connect(speaker)),

        # We use the RangeFloat1 → bool conversion here to highlight the button with the popup, whenever the dimmer
        # value is > 0. To use another condition, you can pass a (lambda) function to the `convert` parameter
        (0.42, 0.52, DisplayButton(label=icon('lightbulb outline icon'), color="black").connect(dimmer, convert=True), [
            Slider(dimmer.parent.name).connect(dimmer)
        ]),
    ]
))

overview_page.new_segment()
overview_page.add_item(HideRowBox([
    TextDisplay(str, "Device that has powered up", " List view"),
    HideRow(speaker.parent.name, color='blue').connect(speaker),
    HideRow(fan.parent.name, color='red').connect(fan),
    # The optional button in the HideRow is completely independent from the row itself. Thus, we must connect the camera
    # variable individually to the button and to the HideRow
    HideRow(camera.name, color='black', button=StatelessButton(False, icon('power off'), color='red').connect(camera))
    .connect(camera),
]))

# create a new page for new elements
add_device_page = web_server.page('add', "Add", menu_entry='Add devices', menu_icon='plus circle icon',
                                menu_sub_label="add devices")

# device selection to add bar
newDevice_type = shc.Variable(style.Devices, 'Device', initial_value=style.Devices.switch)
add_device_page.add_item(EnumSelect(style.Devices, "Add device type selection").connect(newDevice_type))

# impliment the button to add the device to the page
add_button = StatelessButton(None, label=icon('plus'), color="black")
format_button = StatelessButton(None, label=icon('sync'), color="black")
add_device_page.add_item(ButtonGroup("Add the device to the page, use Sync button first to sync the format of the device value type", [add_button, format_button]))

# segment for adding the input of the device
add_device_page.new_segment()

# edit the argument of the new device
newDevice_name = "New Device"
add_device_page.add_item(TextInput(str, 'The name of the device', "{} ").connect(newDevice_name))
newDevice_instanse = newDevice_type._value.value()
add_device_page.add_item(TextInput(str, 'Value of the device: Not initialized ', "{} "))
# Trigger to update the element of the value input format
@format_button.trigger
@shc.handler()
async def sync(_v, _o) -> None:
    newDevice_instanse = newDevice_type._value.value()
    add_device_page.segments[-1].items[-1] = TextInput(NamedTuple, 'Value of the device', "{} ").connect(newDevice_instanse)
    add_device_page.segments[-1].items[-1].render()
# Trigger to add the device after the trigger
@add_button.trigger
@shc.handler()
async def add_to(_v, _o) -> shc.Variable:
    _turnable = newDevice_instanse.turnable()
    _turnlist = []
    _adjustable = newDevice_instanse.minmaxadjust()
    _coloradjustable = newDevice_instanse.coloradjust()
    _floatinput = newDevice_instanse.floatinput()
    _textdisplay = newDevice_instanse.textdisplay()
    # initialize the newdevice shc.Variable object to return
    newDevice = shc.Variable(newDevice_type._value.value, newDevice_name, initial_value=newDevice_type._value.value(**newDevice_instanse._asdict()))
    if _turnable != None:
        for key in _turnable.keys():
            _turnlist.append(Switch(newDevice_name + " " + key).connect(newDevice.field(key)))
        add_device_page.add_item(ButtonGroup("Toggle of the Device", _turnlist))
    if _adjustable != None:
        for key in _adjustable.keys():
            add_device_page.add_item(MinMaxButtonSlider(newDevice_name + " " + key).connect(newDevice.field(key)))
    if _coloradjustable != None:
        for key in _coloradjustable.keys():
            add_device_page.add_item()
            pass
    if _floatinput != None:
        for key in _floatinput.keys():
            add_device_page.add_item(TextInput(type(_floatinput[key][0]), newDevice_name + " " + key, _floatinput[key][1], _floatinput[key][2], _floatinput[key][3], _floatinput[key][4]))
    if _textdisplay != None:
        for key in _textdisplay.keys():
            add_device_page.add_item(TextDisplay(type(_textdisplay[key](0)), label=newDevice_name + _textdisplay[key](1)).connect(newDevice.field(key)))
    return newDevice

# TODO
# furrther action need async action taker to connect to devices.
# markup the device with syntax of lambda functions like the followint 
# @magic_button.trigger
# @shc.handler()
# async def do_rand(_v, _o) -> None:

# Startup the deamon by shc.main() and preform clean exit after daemon has closed
sys.exit(shc.main())
