# python 3
from enum import Enum
from typing import List
from abc import ABC

class Environment():
    def __init__(self):
        self.source_frames = []
        self.recievers = []

class SourceFrame():
    def __init__(self, id: str):
        self.id = id
        self.sources = []
        self.seconds_offset = 0
        self.traj = None

class Source():
    def __init__(self, id: str):
        self.id = id
        self.components = []
        self.seconds_offset = 0
        self.traj = None

class Component():
    def __init__(self, id: str):
        self.id = id
        self.scale = 0
        self.gain = 0
        self.cmp_type = "" # CmpType.BASE 
        self.synth_type = "" #SynthType.TESTTONE
        self.synth_arg = {}

class Reciever():
    def __init__(self, id: str):
        self.id = id
        self.sinks = []
        self.seconds_offset = 0
        self.traj = None

class Sink():
    def __init__(self, id: str):
        self.id = id
        self.seconds_offset = 0
        self.traj = None

class Trajectory():
    def __init__(self, id: str):
        self.id = id
        self.is_vec6 = False
        self.is_stationary = False
        self.x = 0
        self.y = 0
        self.z = 0
        self.heading = 0
        self.pitch = 0
        self.roll = 0

