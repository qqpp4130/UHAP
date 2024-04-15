import errno
from io import TextIOWrapper
from typing import Any, Self, Type, NamedTuple, Optional, Generic
import enum
import shc
from shc.base import logger
import simplejson as json
from pydoc import locate
import os
from shc.datatypes import *

class Switch_Device(NamedTuple):
    power: bool = False
    dimmable: bool = True
    colorable: bool = True
    brightness: RangeFloat1 = 0.0
    color: RGBUInt8 = RGBUInt8(RangeUInt8(0), RangeUInt8(0), RangeUInt8(0))
    def turnable(self):
        return{"power" : self.power}
    def minmaxadjust(self):
        if self.dimmable:
            return {"brightness" : self.brightness}
        else:
            return None
    def coloradjust(self):
        if self.colorable:
            return {"color" : self.color}
        else:
            return None
    def floatinput(self):
        return None
    def textdisplay(self):
        return None
    def fromJSON(String: str):
        _temp = Switch_Device(**json.loads(String))
        # correct the format by recreate the field variable
        self = _temp._replace(brightness = RangeFloat1(_temp.brightness))
        self = _temp._replace(color = RGBUInt8(**_temp.color))
        return self

class Thermostat_Device(NamedTuple):
    power: bool = False
    fan: bool = False
    humidifier: bool = False
    level: RangeFloat1 = 0.0
    temperature: float = 0.0
    tempadjust: float = 16.0
    humidity: RangeFloat1 = 0.0
    humidadjust: RangeFloat1 = 0.0
    def turnable(self):
        return {"power":self.power, "fan":self.fan, "humidifier":self.humidifier}
    def minmaxadjust(self):
        return {"level":self.level}
    def coloradjust(self):
        return None
    def floatinput(self):
        return {"tempadjust":(self.tempadjust, 16.0, 32.0, 0.5, "℃"), "humidadjust":(self.humidadjust, 30.0, 80.0, 5.0, "%")}
    def textdisplay(self):
        return {"temperature":(self.temperature, " Current temperature ℃ "), "humidity":(self.humidity, " Current humidity % ")}
    def fromJSON(String: str):
        _temp = Thermostat_Device(**json.loads(String))
        # correct the format by recreate the field variable
        self = _temp._replace(level = RangeFloat1(_temp.level))
        self = _temp._replace(humidity = RangeFloat1(_temp.humidity))
        self = _temp._replace(humidadjust = RangeFloat1(_temp.humidadjust))
        return self

class Camera_Device(NamedTuple):
    power: bool = False
    rotatable: bool = True
    bidirectional: bool = True
    xaxis: RangeFloat1 = 0.0
    yaxis: RangeFloat1 = 0.0
    def turnable(self):
        return {"power":self.power}
    def minmaxadjust(self):
        if self.rotatable:
            if self.bidirectional:
                return {"xaxis":self.xaxis, "yaxis":self.yaxis}
            else:
                return {"xaxis":self.xaxis}
        else:
            return None
    def coloradjust(self):
        return None
    def floatinput(self):
        return None
    def textdisplay(self):
        return None
    def fromJSON(String: str):
        _temp = Camera_Device(**json.loads(String))
        # correct the format by recreate the field variable
        self = _temp._replace(xaxis = RangeFloat1(_temp.xaxis))
        self = _temp._replace(yaxis = RangeFloat1(_temp.yaxis))
        return self

class Multimedia_Device(NamedTuple):
    power: bool = False
    metadata: str = ''
    level: RangeFloat1 = 0.0
    def turnable(self):
        return {"power":self.power}
    def minmaxadjust(self):
        return {"volume":self.level}
    def coloradjust(self):
        return None
    def floatinput(self):
        return None
    def textdisplay(self):
        return {"metadata":(self.metadata, "Now Playing ")}
    def fromJSON(String: str):
        _temp = Multimedia_Device(**json.loads(String))
        # correct the format by recreate the field variable
        self = _temp._replace(level = RangeFloat1(_temp.level))
        return self

#Devices = [(Switch_Device, "Switch"), (Thermostat_Device, "Thermostat"), (Camera_Device, "Camera"), (Multimedia_Device, "Multimedia")]

class DevicesEnum( enum.Enum ):
    Switch = 0
    Thermostat = 1
    Camera = 2
    Multimedia = 3

EnumDevice = [Switch_Device, Thermostat_Device, Camera_Device, Multimedia_Device]

def fileHandler( file:str, operator:str ) -> TextIOWrapper:
    handle:TextIOWrapper
    if os.path.isfile(file):
        logger.info(f"{file} exists and is a file.")
    else:
        try:
            # remove the potential directory with the same name and recreate a file to write
            logger.warning(f"{file} is not seems to be a file or not exist, performing fix.")
            os.remove(file)
        except OSError as e:
            if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
                logger.error("Error removing the path %s as not exist, error value: %s",file, exc_info=e)
        except BaseException as e:
            logger.error("Error removing the path %s when operating, error value: %s",file, exc_info=e)
            raise e
        finally:
            try:
                # try to create the file
                open(file, 'a').close
            except BaseException as e:
                logger.error("Error on creating the %s when operating, error value: %s",file, exc_info=e)
                raise e
            finally:
                logger.info(f"{file} has created.")
    try:
        handle = open(file, operator)
    except BaseException as e:
        logger.error("Error on opening file %s , error value: %s",file, exc_info=e)
        raise e
    return handle

def writer(variables: dict[str, shc.Variable], JSONvalue: dict[str, dict]) -> dict[str,dict]:
    _newvalues = JSONvalue.copy()
    for k, v in variables.items():
        '''
        try:
            reading = v._value
        except shc.base.UninitializedError:
            reading = None
        '''
        reading = v._value
        if reading == None:
            try:
                _newvalues.pop(k)
            except KeyError:
                logger.error(f"{k} key is not find in the JSON list provided")
                pass
        # return a string form of class name
        typing = reading.__class__.__name__
        _newvalues[k]['values'] = json.loads(json.dumps(reading))
        _newvalues[k]['type'] = typing
    return _newvalues

def deviceStore(variables: dict[str, shc.Variable], handle: TextIOWrapper | None, root: str = os.getcwd()):
    """
    Input operation with w+ for overwrite the sending value, or a+ to append the sending value
    The value sent as value shall be a dict of {str, Variable}, or a list of those kind of dict.
    If a handler is been pass though, it shall not been closed. The passing handle should have operator with a+, do not use w+ to pass it in until method been modified.
    """
    _subjectClose = False
    _oldvalues = JSONreader()
    # argument check
    if handle == None:
        _store = fileHandler(root + "/var/db/device.db", 'w+')
        _subjectClose = True
    elif type(handle) == TextIOWrapper:
        _store = handle
    else:
        # handle is in incorrect format
        raise IOError("Handle pass into the program is invalid, %s with type %s is received", handle, type(handle))
    _newvalue = writer(variables, _oldvalues)
    json.dump(_newvalue, _store)
    # close the handle if subject to close
    if _subjectClose:
        _store.close()

def JSONinterpreter(key: str, value: dict[str, dict], variables: dict[str, shc.Variable]) -> dict[str, shc.Variable]:
    """
    Receiving a str key that is in origin. The dict is structure as {type, values} for the stored JSON value. By checking the shc.variable value method can findout if the class is able to use buildin method to phrase JSON into correct datatype. If it is a regular NameTuple it may imported with the dictonary depacked, if it is regular python class it may directly import from the value reads from JSON
    """
    tp = locate(value['type'])
    val = None
    # NamedTuple special implimentation
    if issubclass(tp, tuple):
        if hasattr(tp, 'fromJSON') and callable(tp.fromJSON):
            val = tp.fromJSON(value['values'])
        else:
            val = tp(**value['values'])
    # regular value implimentation
    else:
        val = tp(value['values'])
    variables.update(key = shc.Variable(tp, key, val))
    return variables

def JSONreader(root: str = os.getcwd()) -> dict[str, dict]:
    """
    Receiving a str key that is in origin. The dict is structure as {type, values} for the stored JSON value. By checking the shc.variable value method can findout if the class is able to use buildin method to phrase JSON into correct datatype. If it is a regular NameTuple it may imported with the dictonary depacked, if it is regular python class it may directly import from the value reads from JSON
    """
    with fileHandler(root + "/var/db/device.db", 'r') as _store:
        _content: dict[str, dict] = json.load(_store)
    return _content

def deviceReader(variables: dict[str, shc.Variable] | None, root: str = os.getcwd()) -> dict[str, shc.Variable]:
    """
    Given a list of variables, if it is empty, then proceed with the read from the file of $pwd/src/var/db/device.db and fill with the data that has been stored.
    If the list has item, then it will read the value from the database file using json.load
    root dir is optional, if not given it will use the current directory by execute the getcwd().
    db will maintain a format of a dictionary with a dictionary inherited within as {name : {type, values}, name2 : {type, values}, ...}
    """
    _content = JSONreader(root)
    _variablesRead: dict[str,shc.Variable] = {}
    # if the list is empty, then it return a list of all variable stored in db
    if not bool(variables):
        for k, v in _content.items():
            JSONinterpreter(k, v, _variablesRead)
    # if input with a list of value, it trigger the update the value from the file
    else:
        _variablesRead = variables.copy()
        for k in _variablesRead.keys():
            JSONinterpreter(k, _content[k], _variablesRead)
    return _variablesRead