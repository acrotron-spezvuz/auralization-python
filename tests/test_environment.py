from model.environment import *

class TestTrajectory():

    def test_toString_id(self):
        test = Trajectory("t1")
        expected = "traj t1\n   StationaryVec6 0.00 0.00 0.00 0.00 0.00 0.00\nend\n"
        assert test.toString() == expected

    def test_toString_filename(self):
        test = Trajectory("t1", file="test.csv")
        expected = "traj t1\n   file test.csv\nend\n"
        assert test.toString() == expected

    def test_toString_full(self):
        test = Trajectory("t1", x=1, y=2, z=3, heading=4, pitch=5, roll=6)
        expected = "traj t1\n   StationaryVec6 1.00 2.00 3.00 4.00 5.00 6.00\nend\n"
        assert test.toString() == expected

    def test_toString_full_with_filename(self):
        test = Trajectory("t1", x=1, y=2, z=3, heading=4, pitch=5, roll=6, file="test.csv")
        expected = "traj t1\n   file test.csv\nend\n"
        assert test.toString() == expected
        
class TestSourceFrame():
    def test_toString_id(self):
        test = SourceFrame("id1")
        expected = "sourceframe id1\n   sources \n   traj None vec6 0.00\nend\n\n\ntraj None\n   StationaryVec6 0.00 0.00 0.00 0.00 0.00 0.00\nend\n\n"
        assert test.toString() == expected

    def test_toString_sources(self):
        sourceOne = SourceFrame("one")
        sourceTwo = SourceFrame("two")
        test = SourceFrame("id1", sources=[sourceOne, sourceTwo])
        expected = "sourceframe id1\n   sources one two\n   traj None vec6 0.00\nend\n\n%s\n%s\ntraj None\n   StationaryVec6 0.00 0.00 0.00 0.00 0.00 0.00\nend\n\n" % (sourceOne.toString(), sourceTwo.toString())
        assert test.toString() == expected

    def test_toString_trjectory(self):
        trajectory = Trajectory("t1")
        test = SourceFrame("id1", traj=trajectory)
        print(test.toString())
        expected = "sourceframe id1\n   sources \n   traj t1 vec6 0.00\nend\n\n\ntraj t1\n   StationaryVec6 0.00 0.00 0.00 0.00 0.00 0.00\nend\n\n"
        assert test.toString() == expected

class TestSink():
    def test_toString_id(self):
        test = Sink("s1")
        expected = "sink s1\n    traj None vec6 0.00\nend\n\ntraj None\n   StationaryVec6 0.00 0.00 0.00 0.00 0.00 0.00\nend\n\n"
        assert test.toString() == expected

    def test_toString_trajectory(self):
        trajectory = Trajectory("t1")
        test = Sink("s1", traj=trajectory)
        expected = "sink s1\n    traj t1 vec6 0.00\nend\n\ntraj t1\n   StationaryVec6 0.00 0.00 0.00 0.00 0.00 0.00\nend\n\n"
        print(test.toString())
        assert test.toString() == expected

class TestComponent():
    def test_toString_id(self):
        test = Component("c1")
        expected = "Component c1\n   scale 0.00\n   cmptype base\n   synthtype testtone\n   syntharg \nend\n"
        assert test.toString() == expected

    def test_toString_all(self):
        test = Component("c1", scale=1, gain=2, cmp_type=CmpType.base, synth_type=SynthType.wave, key_value_pairs={"key": "value"}, wav_file="test.wav")
        expected = "Component c1\n   scale 1.00\n   cmptype base\n   synthtype wave\n   syntharg test.wav\nend\n"
        assert test.toString() == expected

class TestSource():
    def test_toString_id(self):
        test = Source("s1")
        expected = "source s1\n   components \n   traj None vec6 0.00\nend\n\n\ntraj None\n   StationaryVec6 0.00 0.00 0.00 0.00 0.00 0.00\nend\n\n"
        assert test.toString() == expected

    def test_toString_trajectory(self):
        traj = Trajectory("t1")
        test = Source("s1", traj=traj)
        expected = "source s1\n   components \n   traj t1 vec6 0.00\nend\n\n\ntraj t1\n   StationaryVec6 0.00 0.00 0.00 0.00 0.00 0.00\nend\n\n"
        assert test.toString() == expected

    def test_toString_all(self):
        componentOne = Component("c1")
        componentTwo = Component("c2")
        traj = Trajectory("t1")
        test = Source("s1", traj=traj, components=[componentOne, componentTwo], seconds_offset=1)
        expected = "source s1\n   components c1 c2\n   traj t1 vec6 1.00\nend\n\nComponent c1\n   scale 0.00\n   cmptype base\n   synthtype testtone\n   syntharg \nend\n\nComponent c2\n   scale 0.00\n   cmptype base\n   synthtype testtone\n   syntharg \nend\n\ntraj t1\n   StationaryVec6 0.00 0.00 0.00 0.00 0.00 0.00\nend\n\n"
        assert test.toString() == expected

class TestReceiver():
    def test_toString_id(self):
        test = Receiver("r1")
        expected = "receiver r1\n   sinks \n   traj None vec6 0.00\nend\n\n\ntraj None\n   StationaryVec6 0.00 0.00 0.00 0.00 0.00 0.00\nend\n\n"
        assert test.toString() == expected

    def test_toString_sinks(self):
        sinkOne = Sink("s1")
        sinkTwo = Sink("s2")
        test = Receiver("r1", sinks=[sinkOne, sinkTwo])
        expected = "receiver r1\n   sinks s1 s2\n   traj None vec6 0.00\nend\n\nsink s1\n    traj None vec6 0.00\nend\n\ntraj None\n   StationaryVec6 0.00 0.00 0.00 0.00 0.00 0.00\nend\n\n\nsink s2\n    traj None vec6 0.00\nend\n\ntraj None\n   StationaryVec6 0.00 0.00 0.00 0.00 0.00 0.00\nend\n\n\ntraj None\n   StationaryVec6 0.00 0.00 0.00 0.00 0.00 0.00\nend\n\n"
        assert test.toString() == expected

    def test_toString_all(self):
        sinkOne = Sink("s1")
        sinkTwo = Sink("s2")
        traj = Trajectory("t1")
        test = Receiver("r1", sinks=[sinkOne, sinkTwo], traj=traj, seconds_offset=1)
        expected = "receiver r1\n   sinks s1 s2\n   traj t1 vec6 1.00\nend\n\nsink s1\n    traj None vec6 0.00\nend\n\ntraj None\n   StationaryVec6 0.00 0.00 0.00 0.00 0.00 0.00\nend\n\n\nsink s2\n    traj None vec6 0.00\nend\n\ntraj None\n   StationaryVec6 0.00 0.00 0.00 0.00 0.00 0.00\nend\n\n\ntraj t1\n   StationaryVec6 0.00 0.00 0.00 0.00 0.00 0.00\nend\n\n"
        assert test.toString() == expected

class TestEnvironment():
    def test_extract_files_empty(self):
        source = SourceFrame("s1")
        receiver = Receiver("r1")
        test = Environment(source_frames=[source], receivers=[receiver])
        files = test.extract_files(test.source_frames, test.receivers)
        assert not files

    def test_extract_files_all(self):
        sourceOne = Source("s1", traj=Trajectory("t1", file="1.csv"), components=[Component("c1", wav_file="2.csv"), Component("c2", wav_file="3.csv")])
        sourceTwo = Source("s2", traj=Trajectory("t2", file="1.2.csv"), components=[Component("c3", wav_file="2.2.csv"), Component("c4", wav_file="3.2.csv")])
        frameOne = SourceFrame("sf1", sources=[sourceOne, sourceTwo], traj=Trajectory("t3", file="1.3.csv"))

        sourceThree = Source("s3", traj=Trajectory("t4", file="1.4.csv"), components=[Component("c5", wav_file="2.4.csv"), Component("c6", wav_file="3.4.csv")])
        sourceFour = Source("s4", traj=Trajectory("t5", file="1.5.csv"), components=[Component("c7", wav_file="2.5.csv"), Component("c8", wav_file="3.5.csv")])
        frameTwo = SourceFrame("sf2", sources=[sourceThree, sourceFour], traj=Trajectory("t6", file="1.6.csv"))

        sinkOne = Sink("s1", traj=Trajectory("t7", file="1.7.csv"))
        sinkTwo = Sink("s2", traj=Trajectory("t8", file="1.8.csv"))
        receiverOne = Receiver("r1", sinks=[sinkOne, sinkTwo], traj=Trajectory("t9", file="1.9.csv"))

        sinkThree = Sink("s3", traj=Trajectory("t10", file="1.10.csv"))
        sinkFour = Sink("s4", traj=Trajectory("t11", file="1.11.csv"))
        receiverTwo = Receiver("r2", sinks=[sinkThree, sinkFour], traj=Trajectory("t11", file="1.12.csv"))

        test = Environment(source_frames=[frameOne, frameTwo], receivers=[receiverOne, receiverTwo])
        files = {'1.2.csv', '1.8.csv', '1.11.csv', '2.5.csv', '3.5.csv', '2.csv', '3.4.csv', '1.7.csv', 
        '1.9.csv', '1.6.csv', '1.csv', '1.4.csv', '1.10.csv', '3.2.csv', '1.5.csv', '3.csv', '2.4.csv', '1.3.csv', '2.2.csv'}

        assert len(test.files) == 20
        assert files.issubset(test.files)

    def test_extract_files_duplicates(self):
        sourceOne = Source("s1", traj=Trajectory("t1", file="1.csv"), components=[Component("c1", wav_file="2.csv"), Component("c2", wav_file="3.csv")])
        sourceTwo = Source("s2", traj=Trajectory("t2", file="1.2.csv"), components=[Component("c3", wav_file="2.2.csv"), Component("c4", wav_file="3.2.csv")])
        frameOne = SourceFrame("sf1", sources=[sourceOne, sourceTwo], traj=Trajectory("t3", file="1.3.csv"))

        sourceThree = Source("s3", traj=Trajectory("t4", file="1.csv"), components=[Component("c5", wav_file="2.csv"), Component("c6", wav_file="3.csv")])
        sourceFour = Source("s4", traj=Trajectory("t5", file="1.5.csv"), components=[Component("c7", wav_file="2.5.csv"), Component("c8", wav_file="3.5.csv")])
        frameTwo = SourceFrame("sf2", sources=[sourceThree, sourceFour], traj=Trajectory("t6", file="1.6.csv"))

        sinkOne = Sink("s1", traj=Trajectory("t7", file="1.7.csv"))
        sinkTwo = Sink("s2", traj=Trajectory("t8", file="1.8.csv"))
        receiverOne = Receiver("r1", sinks=[sinkOne, sinkTwo], traj=Trajectory("t9", file="1.9.csv"))

        sinkThree = Sink("s3", traj=Trajectory("t10", file="1.10.csv"))
        sinkFour = Sink("s4", traj=Trajectory("t11", file="1.10.csv"))
        receiverTwo = Receiver("r2", sinks=[sinkThree, sinkFour], traj=Trajectory("t11", file="1.9.csv"))

        test = Environment(source_frames=[frameOne, frameTwo], receivers=[receiverOne, receiverTwo])
        files = {'3.2.csv', '1.10.csv', '1.8.csv', '2.csv', '3.5.csv', '1.csv', '2.5.csv', '1.3.csv', 
        '1.9.csv', '2.2.csv', '1.7.csv', '3.csv', '1.6.csv', '1.2.csv', '1.5.csv'}

        print(test.files)
        assert len(test.files) == 15
        assert files.issubset(test.files)

    def test_toString_full(self):
        sourceOne = Source("s1", traj=Trajectory("t1", file="1.csv"), components=[Component("c1", wav_file="2.csv"), Component("c2", wav_file="3.csv")])
        sourceTwo = Source("s2", traj=Trajectory("t2", file="1.2.csv"), components=[Component("c3", wav_file="2.2.csv"), Component("c4", wav_file="3.2.csv")])
        frameOne = SourceFrame("sf1", sources=[sourceOne, sourceTwo], traj=Trajectory("t3", file="1.3.csv"))

        sourceThree = Source("s3", traj=Trajectory("t4", file="1.4.csv"), components=[Component("c5", wav_file="2.4.csv"), Component("c6", wav_file="3.4.csv")])
        sourceFour = Source("s4", traj=Trajectory("t5", file="1.5.csv"), components=[Component("c7", wav_file="2.5.csv"), Component("c8", wav_file="3.5.csv")])
        frameTwo = SourceFrame("sf2", sources=[sourceThree, sourceFour], traj=Trajectory("t6", file="1.6.csv"))

        sinkOne = Sink("s1", traj=Trajectory("t7", file="1.7.csv"))
        sinkTwo = Sink("s2", traj=Trajectory("t8", file="1.8.csv"))
        receiverOne = Receiver("r1", sinks=[sinkOne, sinkTwo], traj=Trajectory("t9", file="1.9.csv"))

        sinkThree = Sink("s3", traj=Trajectory("t10", file="1.10.csv"))
        sinkFour = Sink("s4", traj=Trajectory("t11", file="1.11.csv"))
        receiverTwo = Receiver("r2", sinks=[sinkThree, sinkFour], traj=Trajectory("t11", file="1.12.csv"))

        test = Environment(source_frames=[frameOne, frameTwo], receivers=[receiverOne, receiverTwo])

        expected = """Atmospec default
Terrain SimpleGround

sourceframes sf1 sf2
sourceframe sf1
   sources s1 s2
   traj t3 vec6 0.00
end

source s1
   components c1 c2
   traj t1 vec6 0.00
end

Component c1
   scale 0.00
   cmptype base
   synthtype testtone
   syntharg 2.csv
end

Component c2
   scale 0.00
   cmptype base
   synthtype testtone
   syntharg 3.csv
end

traj t1
   file 1.csv
end


source s2
   components c3 c4
   traj t2 vec6 0.00
end

Component c3
   scale 0.00
   cmptype base
   synthtype testtone
   syntharg 2.2.csv
end

Component c4
   scale 0.00
   cmptype base
   synthtype testtone
   syntharg 3.2.csv
end

traj t2
   file 1.2.csv
end


traj t3
   file 1.3.csv
end


sourceframe sf2
   sources s3 s4
   traj t6 vec6 0.00
end

source s3
   components c5 c6
   traj t4 vec6 0.00
end

Component c5
   scale 0.00
   cmptype base
   synthtype testtone
   syntharg 2.4.csv
end

Component c6
   scale 0.00
   cmptype base
   synthtype testtone
   syntharg 3.4.csv
end

traj t4
   file 1.4.csv
end


source s4
   components c7 c8
   traj t5 vec6 0.00
end

Component c7
   scale 0.00
   cmptype base
   synthtype testtone
   syntharg 2.5.csv
end

Component c8
   scale 0.00
   cmptype base
   synthtype testtone
   syntharg 3.5.csv
end

traj t5
   file 1.5.csv
end


traj t6
   file 1.6.csv
end



receivers r1 r2
receiver r1
   sinks s1 s2
   traj t9 vec6 0.00
end

sink s1
    traj t7 vec6 0.00
end

traj t7
   file 1.7.csv
end


sink s2
    traj t8 vec6 0.00
end

traj t8
   file 1.8.csv
end


traj t9
   file 1.9.csv
end


receiver r2
   sinks s3 s4
   traj t11 vec6 0.00
end

sink s3
    traj t10 vec6 0.00
end

traj t10
   file 1.10.csv
end


sink s4
    traj t11 vec6 0.00
end

traj t11
   file 1.11.csv
end


traj t11
   file 1.12.csv
end


"""
        assert test.toString() == expected


    def test_toString_source_frames(self):
        sourceOne = Source("s1", traj=Trajectory("t1", file="1.csv"), components=[Component("c1", wav_file="2.csv"), Component("c2", wav_file="3.csv")])
        sourceTwo = Source("s2", traj=Trajectory("t2", file="1.2.csv"), components=[Component("c3", wav_file="2.2.csv"), Component("c4", wav_file="3.2.csv")])
        frameOne = SourceFrame("sf1", sources=[sourceOne, sourceTwo], traj=Trajectory("t3", file="1.3.csv"))

        sourceThree = Source("s3", traj=Trajectory("t4", file="1.4.csv"), components=[Component("c5", wav_file="2.4.csv"), Component("c6", wav_file="3.4.csv")])
        sourceFour = Source("s4", traj=Trajectory("t5", file="1.5.csv"), components=[Component("c7", wav_file="2.5.csv"), Component("c8", wav_file="3.5.csv")])
        frameTwo = SourceFrame("sf2", sources=[sourceThree, sourceFour], traj=Trajectory("t6", file="1.6.csv"))

        test = Environment(source_frames=[frameOne, frameTwo])

        expected = """Atmospec default
Terrain SimpleGround

sourceframes sf1 sf2
sourceframe sf1
   sources s1 s2
   traj t3 vec6 0.00
end

source s1
   components c1 c2
   traj t1 vec6 0.00
end

Component c1
   scale 0.00
   cmptype base
   synthtype testtone
   syntharg 2.csv
end

Component c2
   scale 0.00
   cmptype base
   synthtype testtone
   syntharg 3.csv
end

traj t1
   file 1.csv
end


source s2
   components c3 c4
   traj t2 vec6 0.00
end

Component c3
   scale 0.00
   cmptype base
   synthtype testtone
   syntharg 2.2.csv
end

Component c4
   scale 0.00
   cmptype base
   synthtype testtone
   syntharg 3.2.csv
end

traj t2
   file 1.2.csv
end


traj t3
   file 1.3.csv
end


sourceframe sf2
   sources s3 s4
   traj t6 vec6 0.00
end

source s3
   components c5 c6
   traj t4 vec6 0.00
end

Component c5
   scale 0.00
   cmptype base
   synthtype testtone
   syntharg 2.4.csv
end

Component c6
   scale 0.00
   cmptype base
   synthtype testtone
   syntharg 3.4.csv
end

traj t4
   file 1.4.csv
end


source s4
   components c7 c8
   traj t5 vec6 0.00
end

Component c7
   scale 0.00
   cmptype base
   synthtype testtone
   syntharg 2.5.csv
end

Component c8
   scale 0.00
   cmptype base
   synthtype testtone
   syntharg 3.5.csv
end

traj t5
   file 1.5.csv
end


traj t6
   file 1.6.csv
end



receivers 

"""
        assert test.toString() == expected
        
    
    def test_toString_receivers(self):
        sinkOne = Sink("s1", traj=Trajectory("t7", file="1.7.csv"))
        sinkTwo = Sink("s2", traj=Trajectory("t8", file="1.8.csv"))
        receiverOne = Receiver("r1", sinks=[sinkOne, sinkTwo], traj=Trajectory("t9", file="1.9.csv"))

        sinkThree = Sink("s3", traj=Trajectory("t10", file="1.10.csv"))
        sinkFour = Sink("s4", traj=Trajectory("t11", file="1.11.csv"))
        receiverTwo = Receiver("r2", sinks=[sinkThree, sinkFour], traj=Trajectory("t11", file="1.12.csv"))

        test = Environment(receivers=[receiverOne, receiverTwo])

        expected = """Atmospec default
Terrain SimpleGround

sourceframes 


receivers r1 r2
receiver r1
   sinks s1 s2
   traj t9 vec6 0.00
end

sink s1
    traj t7 vec6 0.00
end

traj t7
   file 1.7.csv
end


sink s2
    traj t8 vec6 0.00
end

traj t8
   file 1.8.csv
end


traj t9
   file 1.9.csv
end


receiver r2
   sinks s3 s4
   traj t11 vec6 0.00
end

sink s3
    traj t10 vec6 0.00
end

traj t10
   file 1.10.csv
end


sink s4
    traj t11 vec6 0.00
end

traj t11
   file 1.11.csv
end


traj t11
   file 1.12.csv
end


"""
        assert test.toString() == expected