# python 3
from model.enums import SynthType, CmpType


class Trajectory():
    def __init__(self, id: str, x=0.0, y=0.0, z=0.0, heading=0.0, pitch=0.0, roll=0.0, file=None):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.heading = heading
        self.pitch = pitch
        self.roll = roll
        self.file = file

    def toString(self):
        if(self.file is None):
            tplTraj = "StationaryVec6 %.2f %.2f %.2f %.2f %.2f %.2f" % (self.x, self.y, self.z, self.heading, self.pitch, self.roll)
        else:
            tplTraj = "file %s" % self.file

        tpl = """traj %s
   %s
end
"""
        res = tpl % (self.id, tplTraj)
        return res


class Environment():
    def __init__(self, source_frames=[], receivers=[]):
        self.source_frames = source_frames
        self.receivers = receivers

    def toString(self):
        tpl = """Atmospec default
Terrain SimpleGround

sourceframes %s
%s

receivers %s
%s
"""
        source_frame_ids = " ".join([sf.id for sf in self.source_frames])
        receiver_ids = " ".join([r.id for r in self.receivers])
        source_frames_str = "\n".join([s.toString() for s in self.source_frames])
        receivers_str = "\n".join([r.toString() for r in self.receivers])
        res = tpl % (source_frame_ids, source_frames_str, receiver_ids, receivers_str)
        return res


class SourceFrame():
    def __init__(self, id: str, sources=[], seconds_offset=0.0, traj=Trajectory(None)):
        self.id = id
        self.sources = sources
        self.seconds_offset = seconds_offset
        self.traj = traj

    def toString(self):
        tpl = """sourceframe %s
   sources %s
   traj %s vec6 %.2f
end

%s
%s
"""
        source_ids = " ".join([s.id for s in self.sources])
        sources = "\n".join([s.toString() for s in self.sources])
        res = tpl % (self.id, source_ids, self.traj.id, self.seconds_offset, sources, self.traj.toString())
        return res


class Source():
    def __init__(self, id: str, components=[], seconds_offset=0.0, traj=Trajectory(None)):
        self.id = id
        self.components = components
        self.seconds_offset = seconds_offset
        self.traj = traj

    def toString(self):
        tpl = """source %s
   components %s
   traj %s vec6 %.2f
end

%s
%s
"""
        component_ids = " ".join([c.id for c in self.components])
        components = "\n".join([s.toString() for s in self.components])
        res = tpl % (self.id, component_ids, self.traj.id, self.seconds_offset, components, self.traj.toString())
        return res


class Component():
    def __init__(self, id: str, scale=0.0, gain=0.0, cmp_type=CmpType.base, synth_type=SynthType.testtone, key_value_pairs={}, wav_file=None):
        self.id = id
        self.scale = scale
        self.gain = gain # not used for now
        self.cmp_type = cmp_type
        self.synth_type = synth_type
        self.key_value_pairs = key_value_pairs
        self.wav_file = wav_file

    def toString(self):
        tpl = """Component %s
   scale %.2f
   cmptype %s
   synthtype %s
   syntharg %s
end
"""
        if self.wav_file is None:
            synth_args_str = " ".join("{}={}".format(k, v) for k, v in self.key_value_pairs.items())
        else:
            synth_args_str = self.wav_file
        res = tpl % (self.id, self.scale, self.cmp_type.value, self.synth_type.value, synth_args_str)
        return res

class Receiver():
    def __init__(self, id: str, sinks=[], seconds_offset=0.0, traj=Trajectory(None)):
        self.id = id
        self.sinks = sinks
        self.seconds_offset = seconds_offset
        self.traj = traj

    def toString(self):
        tpl = """receiver %s
   sinks %s
   traj %s vec6 %.2f
end

%s
%s
"""
        sink_ids = " ".join([s.id for s in self.sinks])
        sinks_str = "\n".join([s.toString() for s in self.sinks])
        res = tpl % (self.id, sink_ids, self.traj.id, self.seconds_offset, sinks_str, self.traj.toString())
        return res


class Sink():
    def __init__(self, id: str, seconds_offset=0.0, traj=Trajectory(None)):
        self.id = id
        self.seconds_offset = seconds_offset
        self.traj = traj

    def toString(self):
        tpl = """sink %s
    traj %s vec6 %.2f
end

%s
"""
        res = tpl % (self.id, self.traj.id, self.seconds_offset, self.traj.toString())
        return res


# test script
if __name__ == "__main__":
    t1 = Trajectory("t1", file="traj1.csv")
    t2 = Trajectory("t2", x=2, y=2, z=2, heading=2, pitch=2, roll=2)
    t3 = Trajectory("t3", x=3, y=3, z=3, heading=3, pitch=3, roll=3)

    s1 = Sink("s1", seconds_offset=10.1, traj=t1)
    s2 = Sink("s2", seconds_offset=20.1, traj=t2)

    r1 = Receiver("rec1", sinks=[s1, s2], seconds_offset=30.33, traj=t3)
    r2 = Receiver("r2", sinks=[s1, s2], seconds_offset=0.55, traj=t3)

    c1 = Component("c1", scale=2.5, synth_type=SynthType.testtone, key_value_pairs={'freq': 2000})
    c2 = Component("c2", scale=15.4, synth_type=SynthType.wave, wav_file="sample.wav")

    src = Source("src", seconds_offset=10, traj=t1, components=[c1, c2])

    sf = SourceFrame("aircraft", sources=[src], traj=t2, seconds_offset=0)

    e = Environment(source_frames=[sf], receivers=[r1, r2])
    print(e.toString())
