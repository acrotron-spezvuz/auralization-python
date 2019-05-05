# python 3
from enum import Enum

class CmpType(Enum):
    base = "base"

class SynthType(Enum):
    broadband = "broadband"
    puretone = "puretone"
    testtone = "testtone"
    wave = "wave"
    random = "random"

