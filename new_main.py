import os
import textx as tx

NOTE = {'bd': 60}


class Model(object):
    def __init__(self, sections, tracks, bpm, patterns):
        self.sections = sections
        self.tracks = tracks
        self.bpm = bpm
        self.patterns = patterns

    def __str__(self):
        out = ''
        out += str(self.bpm) + '\n\n'
        out += '\n'.join([str(pattern) for pattern in self.patterns])
        out += '\n'.join([str(section) for section in self.sections])
        out += '\n'.join([str(track) for track in self.tracks])
        return out


class Pattern(object):
    def __init__(self, parent, name, beat_pattern):
        self.parent = parent
        self.name = name
        self.beat_pattern = BeatPattern(self, beat_pattern)

    def __str__(self):
        return self.name + ' ' + str(self.beat_pattern) + '\n\n'


class BeatPattern(object):
    def __init__(self, parent, beats):
        self.parent = parent
        self.beats = beats
        self.size = [len(token) for token in ''.join([str(beat) for beat in self.beats]).split('|')]

    def is_beat_pattern_matching_with_pattern(self, pattern):

        base_pattern_size = len(pattern.beats)

        if len(self.beats) != base_pattern_size:
            return False

        for beat_index in range(base_pattern_size):
            if not self.beats[0].is_beat_size_equals(pattern.beats[beat_index]):
                return False

        return True

    def generate_beats(self):

        if not self.is_beatPattern_matching_with_pattern(self.parent.pattern):
            return "Beat pattern is not matching with bar pattern"
        return '\n'.join([str(beat) for beat in self.beats])

    def __str__(self):
        return str(self.size)


class Track(object):
    def __init__(self, parent, name, sections):
        self.parent = parent
        self.name = name
        self.sections = sections

    def __str__(self):
        return '\nTrack ' + self.name + '\n' + '\n'.join([section.name for section in self.sections]) + '\n'


class Section(object):
    def __init__(self, parent, name, bars):
        self.parent = parent
        self.name = name
        self.bars = bars

    def __str__(self):
        return 'Section ' + self.name + '\n' + '\n'.join([str(bar) for bar in self.bars]) + '\n'


class Bar(object):

    def __init__(self, parent, ticks, note):
        self.parent = parent
        self.ticks = ticks
        self.note = note
        self.current_tick = 0

    def __str__(self):
        # TODO put midi code inside stp
        return '\n'.join([tick for tick in self.ticks]) + ' ' + self.note


if __name__ == '__main__':

    classes = [Model, Bar, Section, Track, Pattern, BeatPattern]

    meta_model = tx.metamodel_from_file('new_grammar.tx', classes=classes)

    try:
        os.mkdir('out')
    except FileExistsError:
        pass

    for file_name in os.listdir('samples'):
        ID_REGISTRY = dict()
        READABLE_BRICK = dict()
        print("Translating {}".format(file_name))
        model = meta_model.model_from_file('samples/{}'.format(file_name))

        out = open('out/{}'.format(file_name.replace('.rml', '.py')), 'w')
        print(model, file=out)
        print(model)
        out.close()
