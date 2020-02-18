import os
import textx as tx

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
    def __init__(self, parent, name, pattern, beat_patterns):
        self.parent = parent
        self.name = name
        self.pattern = pattern
        self.beat_patterns = beat_patterns


class Pattern(object):
    def __init__(self, parent, name, list):
        self.parent = parent
        self.name = name
        self.list = list  # liste d'entiers

class Tick(object):
    def __init__(self, parent, value):
        self.parent = parent
        self.value = value


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

class BeatPattern(object):
    def __init__(self, parent, beats):
        self.parent = parent
        self.beats = beats

if __name__ == "__main__":

    if __name__ == '__main__':

        classes = [Model, Section, Track]

        meta_model = tx.metamodel_from_file('grammar.tx', classes=classes)
        try:
            os.mkdir('out')
        except FileExistsError:
            pass

        for file_name in os.listdir('samples'):
            ID_REGISTRY = dict()
            READABLE_BRICK = dict()
            print("Translating {}".format(file_name))
            model = meta_model.model_from_file('samples/{}'.format(file_name))

            out = open('out/{}'.format(file_name.replace('.rml', '.midi')), 'w')
            print(model, file=out)
            out.close()