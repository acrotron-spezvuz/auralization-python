# python 3
from enum import Enum
from typing import List

class Environment():
    def __init__(self):
        self.source_frames = []
        self.recievers = []

class SourceFrame():
    def __init__(self):
        self.id = ""
        self.sources = []
        self.seconds_offset = 0
        self.traj = None

    def set_source_names(self, source_names):
        self._source_names = source_names

class Source():
    def __init__(self):
        self.id = ""
        self.components = []
        self.seconds_offset = 0
        self.traj = None

class Component():
    def __init__(self):
        self.id = ""
        self.scale = 0
        self.gain = 0
        self.cmp_type = CmpType.BASE 
        self.synth_type = SynthType.TESTTONE
        self.synth_arg = []

class Reciever():
    def __init__(self):
        self.id = ""
        self.sinks = []
        self.seconds_offset = 0
        self.traj = None

class Sink():
    def __init__(self):
        self.id = ""
        self.seconds_offset = 0
        self.traj = None

class Trajectory():
    def __init__(self):
        self.id = ""
        self.x = 0
        self.y = 0
        self.z = 0
        self.heading = 0
        self.pithc = 0
        self.roll = 0

class CmpType(Enum):
    BASE = "base"

class SynthType(Enum):
    BROADBAND = "broadband"
    PURETONE = "puretone"
    TESTTONE = "testtone"
    WAVE = "wave"
    RANDOM = "random"

