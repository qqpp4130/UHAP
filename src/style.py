from typing import Any, Self, Type, NamedTuple, Optional
import enum
import shc
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
        return

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

class Devices(enum.Enum):
    switch = Switch_Device
    thermostat = Thermostat_Device
    camera = Camera_Device
    multimedia = Multimedia_Device
