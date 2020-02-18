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
    def __init__(self, parent, name, pattern, note_lines):
        self.parent = parent
        self.name = name
        self.pattern = pattern
        self.note_lines = note_lines


class Pattern(object):
    def __init__(self, parent, name, list):
        self.parent = parent
        self.name = name
        self.list = list  # liste d'entiers


class NotePattern(object):
    def __init__(self, parent, name, ticks):
        self.parent = parent
        self.name = name
        self.ticks = ticks


class Tick(object):
    def __init__(self, parent, value):
        self.parent = parent
        self.value.value

class NoteList(object):
    def __init__(self, parent, note_pattern, note):
        self.parent = parent
        self.note_pattern = note_pattern
        self.note = note


class Note(object):
    def __init__(self, parent, value):
        self.parent = parent
        self.value = value
