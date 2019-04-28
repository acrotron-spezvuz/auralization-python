# python 3
# is an exmple of using library methods 

import sys
# import naf library
from nafServiceClient import nafClient
from pathlib import Path
import json
from environment import *

if __name__ == "__main__":
    zerotraj = Trajectory("zerotraj")
    listraj = Trajectory("listraj", z=5)
    traj1 = Trajectory("traj1", file="traj1.csv")

    s1 = Sink("s1", traj=zerotraj)

    r1 = Receiver("rec1", sinks=[s1], traj=listraj)

    comp_rand = Component("rand", scale=20, synth_type=SynthType.random)
    comp_tone1 = Component("tone1", scale=10, synth_type=SynthType.testtone, synth_arg={'freq': 1000})
    comp_tone2 = Component("tone2", scale=2.5, synth_type=SynthType.testtone, synth_arg={'freq': 2000})

    src = Source("src", traj=zerotraj, components=[comp_rand, comp_tone1, comp_tone2])

    sf = SourceFrame("aircraft", sources=[src], traj=traj1)

    e = Environment(source_frames=[sf], receivers=[r1])
    print(e.toString())

    # read all data
    content = e.toString()

    # send
    naf_client = nafClient()
    auralization_result = naf_client.auralize_from_content2(content)

    print(auralization_result)
