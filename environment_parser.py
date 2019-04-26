# python 3
# an environmet data parser 
from pathlib import Path
from environment import Environment, SourceFrame, Reciever, Source, Component, Sink, Trajectory
from typing import List, Dict
import re


class EnvironmentParser():
    def __init__(self):
        self.__file = None
        self._source_frames = {}
        self._source_map = {}
        self._components_map = {}
        self._recievers = {}
        self._sink_map = {}
        self._trajectories = {}
        self._env = Environment()
        pass

    # should be a vid path to file with data
    def parse_from_path(self, path_to_data: Path) -> Environment:
        # open and read file
        with path_to_data.open() as self.__file:

            line = self.__file.readline()
            # skip_to_struct_end = False
            # is_inside_struct = False
            while line:
                line = line.strip()
                
                if self.__startswith(line, "end") or len(line) is 0:
                    #is_inside_struct = False
                    line = self.__file.readline()
                    continue
                    
                # awesome switch ... case
                if self.__startswith(line, "sourceframes"):
                    # split line into a list by space separator 
                    # fill dict with keys and empty values
                    self._source_frames = self.__parse_line_with_names(line)
                
                elif self.__startswith(line, "sourceframe"):                    
                    self.__parse_source_frame(line)

                elif self.__startswith(line, "source"):
                    self.__parse_source(line)
                
                elif self.__startswith(line, "component"):
                    self.__parse_component(line)
                
                elif self.__startswith(line, "receivers"):
                    self._recievers = self.__parse_line_with_names(line)
                
                elif self.__startswith(line, "receiver"):
                    self.__parse_reciever(line)

                elif self.__startswith(line, "sink"):
                    self.__parse_sink(line)
                    
                elif self.__startswith(line, "traj"):
                    self.__parse_and_fill_trajectory(line)
                        
                else:
                    print("How to parse the line? : ", len(line), line)

                line = self.__file.readline()
                
            # all lines are parsed 
            # map source frames
            self._env.source_frames = [self._source_frames[key] for key in self._source_frames]
            # map recievers
            self._env.recievers = [self._recievers[key] for key in self._recievers]
        return self._env

    def __parse_source_frame(self, line: str):
        # get source frame by name 
        lst = line.split()
        # skip source frame if it is not in list
        if len(lst) < 2 or lst[1] not in self._source_frames:
            return

        source_frame = SourceFrame(lst[1])
        self._source_frames[source_frame.id] = source_frame

        line = self.__file.readline()
        while line: 
            line = line.strip()
            if self.__startswith(line, "end"):
                break
            elif self.__startswith(line, "sources"):
                the_list = line.split()
                if len(the_list) > 1:
                    self._source_map = { item:[source_frame] for item in the_list[1:len(the_list)] }

            elif self.__startswith(line, "traj"):
                self.__parse_trajectory_and_offset(line, source_frame)
            else:
                pass

            line = self.__file.readline()

    # parse source
    def __parse_source(self, line: str):
        lst = line.split()
        if len(lst) < 2 or lst[1] not in self._source_map:
            return
        
        source = Source(lst[1])
        for source_frame in self._source_map[source.id]:
            source_frame.sources.append(source)
        
        line = self.__file.readline()
        while line: 
            line = line.strip()
            if self.__startswith(line, "end"):
                break

            elif self.__startswith(line, "components"):
                the_list = line.split()                    
                if len(the_list) > 1:
                    # NOTE: change logic if you need more sources
                    self._components_map = { item:[source] for item in the_list[1:len(the_list)] }

            elif self.__startswith(line, "traj"):
                self.__parse_trajectory_and_offset(line, source)
            
            else:
                pass
            
            line = self.__file.readline()
        pass

    # parse component
    def __parse_component(self, line: str):
        lst = line.split()
        if len(lst) < 2 or lst[1] not in self._components_map:
            return

        component = Component(lst[1])
        for source in self._components_map[component.id]:
            source.components.append(component)

        line = self.__file.readline()
        while line: 
            line = line.strip()
            if self.__startswith(line, "end"):
                break

            elif self.__startswith(line, "scale") or self.__startswith(line, "scalefactor") or self.__startswith(line, "linearscale"):
                the_list = line.split()
                if len(the_list) > 1:
                    component.scale = float(the_list[1])
            elif self.__startswith(line, "gain") or self.__startswith(line, "dbgain") or self.__startswith(line, "db"):
                the_list = line.split()
                if len(the_list) > 1:
                    component.gain = float(the_list[1])
            elif self.__startswith(line, "cmptype"):
                the_list = line.split()
                if len(the_list) > 1:
                    component.cmp_type = the_list[1]
            elif self.__startswith(line, "synthtype"):
                the_list = line.split()
                if len(the_list) > 1:
                    component.synth_type = the_list[1]
            elif self.__startswith(line, "syntharg"):
                the_list = line.split()
                if len(the_list) > 1:
                    # split args 
                    args = the_list[1].split("=")
                    component.synth_arg = {args[i]: args[i+1] for i in range(0, len(args), 2)}
            else:
                pass

            line = self.__file.readline()
        pass

    # parse trajectory and offset
    def __parse_trajectory_and_offset(self, line: str, parent_obj):
        lst = line.split()
        if len(lst) < 4:
            raise Exception("Not enought data for trajectory. Source: ", parent_obj.id)

        traj = None 
        if lst[1] not in self._trajectories: 
            traj = Trajectory(lst[1]) 
            self._trajectories[traj.id] = traj
        else:
            traj = self._trajectories[lst[1]]

        if isinstance(parent_obj, SourceFrame):
            if self.__startswith(lst[2], "vec6") is False:
                raise Exception("For sourceframes, only a vec6 trajectory is relevant. Source frame:", parent_obj.id)
        
        if self.__startswith(lst[2], "vec6"):
            traj.is_vec6 = True

        parent_obj.traj = traj
        # latest is seconds offset value
        parent_obj.seconds_offset = float(lst[len(lst)-1])
        pass

    # parse reciever 
    def __parse_reciever(self, line: str):
        lst = line.split()
        if len(lst) < 2 or lst[1] not in self._recievers:
            return

        reciever = Reciever(lst[1])
        self._recievers[reciever.id] = reciever

        line = self.__file.readline()
        while line: 
            line = line.strip()
            if self.__startswith(line, "end"):
                break
            elif self.__startswith(line, "sinks"):
                the_list = line.split()                    
                if len(the_list) > 1:
                    # NOTE: change logic if you need more 
                    self._sink_map = { item:[reciever] for item in the_list[1:len(the_list)]}

            elif self.__startswith(line, "traj"):
                self.__parse_trajectory_and_offset(line, reciever)
            else:
                pass
            line = self.__file.readline()
        pass
    
    # parse sink
    def __parse_sink(self, line: str):
        lst = line.split()
        if len(lst) < 2 or lst[1] not in self._sink_map:
            return 
        sink = Sink(lst[1])
        for reciever in self._sink_map[sink.id]:
            reciever.sinks.append(sink)

        line = self.__file.readline()
        while line: 
            line = line.strip()
            if self.__startswith(line, "end"):
                break
            elif self.__startswith(line, "traj"):
                self.__parse_trajectory_and_offset(line, sink)
            else:
                pass
            line = self.__file.readline()
        pass
    
    # parse and fill trajectory
    def __parse_and_fill_trajectory(self, line: str):
        lst = line.split()
        if len(lst) < 2 or lst[1] not in self._trajectories:
            return
        trajectory = self._trajectories[lst[1]]
        line = self.__file.readline()
        while line: 
            line = line.strip()
            if self.__startswith(line, "end"):
                break
            elif self.__startswith(line, "file"):
                the_list = line.split()                    
                if len(the_list) > 1:
                    path = Path(the_list[1])
                    if path.exists() and path.is_file():
                        # TODO: read file, fill data
                        pass
                    else:
                        # temporary disabled error
                        # raise FileNotFoundError(the_list[1])
                        pass

            elif self.__startswith(line, "stationaryvec6"):
                the_list = line.split()                    
                if len(the_list) > 1:
                    trajectory.is_stationary = True
                    trajectory.x = float(the_list[1])
                    trajectory.y = float(the_list[2])
                    trajectory.z = float(the_list[3])
                    trajectory.heading = float(the_list[4])
                    trajectory.pitch = float(the_list[5])
                    trajectory.roll = float(the_list[6])
            else:
                pass
            line = self.__file.readline()
        pass  

    def __parse_line_with_names(self, line: str) -> dict:
        the_list = line.split()
        if len(the_list) > 1:
            return { item:None for item in the_list[1:len(the_list)] }
        else:
            return {}

    def __startswith(self, line: str, pattern: str) -> bool:
        return bool(re.match(pattern, line, re.I))