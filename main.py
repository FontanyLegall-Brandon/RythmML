import textx as tx
import time
import rtmidi

class Track(object):
    def __init__(self,name):
        self.name = name

class Bar(object):
    def __init__(self,name):
        self.name = name

class Beat(object):
    def __init__(self,name):
        self.name = name

    model = meta_model.model_from_file('samples/old_basic_scenario_1.rml')

class Note(object):
    def __init__(self, value, tick_pos, duration):
        self.value = value
        self.tick_pos = tick_pos
        self.duration = duration