class Model(object):
    def __init__(self, parent, name, bpm, bar_list, section_list, track):
        self.parent = parent
        self.name = name
        self.bpm = bpm
        self.bar_list = bar_list
        self.section_list = section_list
        self.track = track

class Section(object):
    def __init__(self, parent, name, bar_list):
        self.parent = parent
        self.name = name
        self.bar_list = bar_list


class Track(object):
    def __init__(self, parent, name, section_list):
        self.parent = parent
        self.name = name
        self.section_list = section_list


class Bar(object):
    def __init__(self, parent, name, pattern, beats):
        self.parent = parent
        self.name = name
        self.pattern = pattern
        self.beats = beats


class Pattern(object):
    def __init__(self, parent, name, list):
        self.parent = parent
        self.name = name
        self.list = list  # liste d'entiers

class Tick(object):
    def __init__(self, parent, value):
        self.parent = parent
        self.value.value


class Beat(object):
    def __init__(self, parent, ticks, note):
        self.parent = parent
        self.ticks = ticks
        self.note = note


class Separator(object):
    def __init__(self, parent, value):
        self.parent = parent
        self.value = value

class Note(object):
    def __init__(self, parent, value):
        self.parent = parent
        self.value = value
