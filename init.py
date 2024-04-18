import random
import shc
import os
import sys
from itertools import islice
from datetime import datetime
from src import style
import shc
import os
from shc.web import WebServer
from shc.datatypes import *
from shc.web.widgets import *
from shc.base import logger
import enum
import markupsafe


global PWD, CURRENTTIME, DEVICELIST
PWD = os.getcwd()
CURRENTTIME = datetime.now().strftime("%Y%m%d%H%M%S")
logger.info("Server is starting at %s", CURRENTTIME)
# initialize the device list, shc._ALL_VARIABLES is accssable as the all variable set
# this list is using name as key and following by the value of the shc.variable
# loading device list from the database
DEVICELIST: dict[str, shc.Variable] = style.deviceReader(None, PWD)
print(DEVICELIST)

# device selection to add bar
newDevice_type = shc.Variable(style.DevicesEnum, 'Device', initial_value=style.DevicesEnum.Switch)

class Device(enum.Enum):
    Speakers = 0
    Light = 1
    Thermometer = 2
    Alarm = 3
    Door = 4
# WARNING, folloing assignment of variable is subject to remove in the following commit. Please change the code accordingly
# TODO: implemented with device.db, move all variable to the config file.
foo = shc.Variable(bool, 'foo', initial_value=False)
bar = shc.Variable(bool, 'bar', initial_value=False)
foobar = shc.Variable(bool, 'foobar', initial_value=False)
yaks_favorite_Device = shc.Variable(Device, 'yaks_favorite_Device', initial_value=Device.Light)
number_of_yaks = shc.Variable(int, 'number_of_yaks', initial_value=0)
yak_wool = shc.Variable(RangeFloat1, 'yak_wool', initial_value=0.0)
yak_color = shc.Variable(RGBUInt8, 'yak_color', initial_value=RGBUInt8(RangeUInt8(0), RangeUInt8(0), RangeUInt8(0)))

#set up Device types
#style.deviceStore(DEVICELIST, None)

#New device setup scheme. Using class for different type of device and group the arguments together in one shc.Variable
#DEVICELIST['dimmer_light'] = shc.Variable(style.Switch_Device, "dimmer_light", initial_value=style.Switch_Device(False, True, False, 0.0, RGBUInt8(RangeUInt8(0), RangeUInt8(0), RangeUInt8(0))))
thermostat = shc.Variable(style.Thermostat_Device, 'theromostat', initial_value=style.Thermostat_Device(True, False, False, 1.0, 20.0, 35.0, 35.0, 35.0))
multimedia = shc.Variable(style.Multimedia_Device, "speaker", initial_value=style.Multimedia_Device(False, "None", 0.0))
#DEVICELIST['neon_light'] = shc.Variable(style.Switch_Device, 'neon_light', initial_value=style.Switch_Device(False, False, True, color=RGBUInt8(RangeUInt8(0), RangeUInt8(0), RangeUInt8(0))))
#connect old variable to new form of variable group
speaker = multimedia.field('power')
switch = DEVICELIST['dimmer_light'].field('power')
dimmer = DEVICELIST['dimmer_light'].field('brightness')
fan = thermostat.field('fan')
therometer = thermostat.field('tempadjust')
temperture = thermostat.field('temperature')
humidity = thermostat.field('humidadjust')

# connect the device power with the field converted to bool
DEVICELIST['dimmer_light'].field('power').connect(DEVICELIST['dimmer_light'].field('brightness'), convert=True)
thermostat.field('fan').connect(thermostat.field('level'), convert=True)

# initialilze httpserver object
# Define server main function and child components
# WebServer running at port 8080
web_server = shc.web.WebServer('localhost', 8080, index_name='index')

# Page index (Home)
index_page = web_server.page('index', 'Home', menu_entry=True, menu_icon='home')

# Toggle button bar
index_page.add_item(ButtonGroup("State of the Device", [
    ToggleButton(speaker.parent.name).connect(speaker),
    # Foobar requires confirmation when switched on.
    ToggleButton(DEVICELIST['camera'].name, color='black',
                confirm_message="Do you want to turn it on?", confirm_values=[True]).connect(DEVICELIST['camera']),
]))
# We can also use ValueButtons to represent individual states (here in the 'outline' version)
index_page.add_item(ButtonGroup("Thermostat", [
    ValueButton(False, "Off", outline=True, color="black").connect(fan),
    ValueButton(True, "On", outline=True).connect(fan),
    TextInput(float, icon('temperature high', f"{temperture._value} ") + therometer.parent.name, min=16.0, max=36.0, step=0.5, input_suffix="°C").connect(temperture),
    TextDisplay(RangeFloat1, icon('tint', f"{humidity._value} "), humidity.parent.name).connect(humidity)
]))
index_page.add_item(ButtonGroup("State of the Device", [
    ToggleButton("Foo").connect(foo),
    ToggleButton("Bar", color='red').connect(bar),
    # Foobar requires confirmation when switched on.
    ToggleButton("Foobar", color='black',
                 confirm_message="Do you want the foobar?", confirm_values=[True]).connect(foobar),
]))
index_page.add_item(ButtonGroup("The Foo", [
    ValueButton(False, "Off", outline=True, color="black").connect(foo),
    ValueButton(True, "On", outline=True).connect(foo),
]))
index_page.add_item(ValueListButtonGroup([(style.DevicesEnum.Switch, '💡'),
                                          (style.DevicesEnum.Multimedia, '🔊'),
                                          (style.DevicesEnum.Thermostat, '🌡️'),
                                          (style.DevicesEnum.Camera, '🔒')], "Which Device?").connect(newDevice_type))
index_page.add_item(EnumButtonGroup(style.DevicesEnum, "Which Device, again?").connect(newDevice_type))

# … or, let's simply take a dropdown
index_page.add_item(Select([(style.DevicesEnum.Switch, '💡'),
                            (style.DevicesEnum.Multimedia, '🔊'),
                            (style.DevicesEnum.Thermostat, '🌡️'),
                            (style.DevicesEnum.Camera, '🔒')], "Now really, which Device?").connect(newDevice_type))
# Another segment in the right column
# We also have buttons, that are only readable (disabled) …
index_page.add_item(ButtonGroup("State of the Device", [
    DisplayButton(label=icon('hat wizard'), color="teal").connect(bar),
]))

# color light bulb
index_page.new_segment("The neon light bulb with dimmer")

index_page.add_item(Switch(switch.parent.name, color='red').connect(switch))
index_page.add_item(ColorChoser().connect(DEVICELIST['neon_light'].field("color")))
magic_button = StatelessButton(None, label=icon('magic'), color="orange")
index_page.add_item(ButtonGroup("Supprise!", [magic_button]))

# Trigger to randomize color
@magic_button.trigger
@shc.handler()
async def do_rand(_v, _o) -> None:
    await DEVICELIST['neon_light'].write(RGBUInt8(RangeUInt8(random.randint(0, 255)), RangeUInt8(random.randint(0, 255)), RangeUInt8(random.randint(0, 255))))

index_page.add_item(MinMaxButtonSlider(dimmer.parent.name, color='black').connect(dimmer))


# Overview page
overview_page = web_server.page('overview', "Overview", menu_entry=True, menu_icon='tachometer alternate')

# ImageMap supports all the different Buttons as items, as well as the special ImageMapLabel
# The optional fourth entry of each item is a list of WebPageItems (everything we have shown so far – even an ImageMap))
# to be placed in a popup shown when the item is clicked.
overview_page.add_item(ImageMap(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Newburn_Flats_Floor_Plan.pdf"
    "/page1-543px-Newburn_Flats_Floor_Plan.pdf.jpg",
    [
        (0.20, 0.30, ToggleButton(switch.parent.name, outline=True).connect(switch)),
        (0.33, 0.30, ToggleButton(fan.parent.name, color='red', outline=True).connect(fan)),
        # DEVICELIST['camera'] requires confirmation when switched on.
        (0.67, 0.30, ToggleButton(DEVICELIST['camera'].name, color='black', outline=True,
                                  confirm_message="Do you want the DEVICELIST['camera'] on?", confirm_values=[True]).connect(DEVICELIST['camera'])),

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
    # The optional button in the HideRow is completely independent from the row itself. Thus, we must connect the DEVICELIST['camera']
    # variable individually to the button and to the HideRow
    HideRow(DEVICELIST['camera'].name, color='black', button=StatelessButton(False, icon('power off'), color='red').connect(DEVICELIST['camera']))
    .connect(DEVICELIST['camera']),
]))

# create a new page for new elements
add_device_page = web_server.page('add', "Add", menu_entry=True, menu_icon='plus circle icon')
add_device_page.add_item(EnumSelect(style.DevicesEnum, "Add device type selection").connect(newDevice_type))

# impliment the button to add the device to the page
add_button = StatelessButton(None, label=icon('plus'), color="black")
add_device_page.add_item(ButtonGroup("Add the device to the page", [add_button]))

# segment for adding the input of the device
add_device_page.new_segment("New Devices setup")
add_device_page.new_segment(same_column=True)

# For entering numbers or strings, use the TextInput widget


# it even allows to HTML-format the value (or use a custom function for formatting):

add_device_page.add_item(ValueListButtonGroup([(style.DevicesEnum.Switch, '💡'),
                                          (style.DevicesEnum.Multimedia, '🔊'),
                                          (style.DevicesEnum.Thermostat, '🌡️'),
                                          (style.DevicesEnum.Camera, '🔒')], "Which Device?").connect(newDevice_type))
# edit the argument of the new device
newDevice_name = shc.Variable(str, initial_value="New Device")
add_device_page.add_item(TextInput(str, 'The name of the device').connect(newDevice_name))
newDevice_instanse = style.EnumDevice[newDevice_type._value.value]()
add_device_page.add_item(TextInput(str, 'Value of the device: Not initialized ', "{} "))
valuefield = add_device_page.segments[-1].items[-1]
# Trigger to update the element of the value input format
# FIXME device type does not change with update
@newDevice_type.trigger
@shc.blocking_handler()
def sync(newDevice_instanse) -> shc.Variable:
    print("Device type changed")
    newDevice_instanse = style.EnumDevice[newDevice_type._value.value]()
    add_device_page.segments[-1].items.pop()
    add_device_page.add_item(TextInput(style.EnumDevice[newDevice_type._value.value], 'Value of the device', "{} ").connect(newDevice_instanse))
    print("value set: " + str(newDevice_instanse._asdict()))
    print("List of variables: " + str(DEVICELIST))
    return newDevice_instanse

# Trigger to add the device after the trigger
# FIXME the added device cannot be determained with error message: Could not route message from websocket to connector, since no connector with id 140542855234896 is known.
@add_button.trigger
@shc.handler()
async def add_to() -> None:
    print("New button pressed")
    _turnable = newDevice_instanse.turnable()
    _turnlist = []
    _adjustable = newDevice_instanse.minmaxadjust()
    _coloradjustable = newDevice_instanse.coloradjust()
    _floatinput = newDevice_instanse.floatinput()
    _textdisplay = newDevice_instanse.textdisplay()
    print("initialized list of variables")
    DEVICELIST.update({newDevice_name._value:shc.Variable(style.EnumDevice[newDevice_type._value.value], newDevice_name._value)})
    # initialize the newdevice shc.Variable object to return
    print("Device " + newDevice_name._value + " is initialized: "+ str(DEVICELIST[newDevice_name._value]._variable_fields))
    if _turnable != None:
        for key in _turnable.keys():
            _turnlist.append(Switch(key).connect(DEVICELIST[newDevice_name._value].field(key)))
        add_device_page.add_item(ButtonGroup("Toggle of the Device " + newDevice_name._value, _turnlist))
    if _adjustable != None:
        for key in _adjustable.keys():
            add_device_page.add_item(MinMaxButtonSlider(newDevice_name._value + " " + key).connect(DEVICELIST[newDevice_name._value].field(key)))
    if _coloradjustable != None:
        for key in _coloradjustable.keys():
            add_device_page.add_item(ColorChoser().connect(DEVICELIST[newDevice_name._value].field(key)))
    if _floatinput != None:
        for key in _floatinput.keys():
            add_device_page.add_item(TextInput(type(_floatinput[key][0]), newDevice_name._value + " " + key, _floatinput[key][1], _floatinput[key][2], _floatinput[key][3], _floatinput[key][4]).connect(DEVICELIST[newDevice_name._value].field(key)))
    if _textdisplay != None:
        for key in _textdisplay.keys():
            add_device_page.add_item(TextDisplay(type(_textdisplay[key](0)), label=newDevice_name._value + _textdisplay[key](1)).connect(DEVICELIST[newDevice_name._value].field(key)))
    print("Item add to page")
    await valuefield.render()
    print("Render successful")

# TODO
# furrther action need async action taker to connect to devices.
# markup the device with syntax of lambda functions like the followint 
# @magic_button.trigger
# @shc.handler()
# async def do_rand(_v, _o) -> None:

# Startup the deamon by shc.main() and preform clean exit after daemon has closed
logger.info('Server is starting...')
sys.exit(shc.main())