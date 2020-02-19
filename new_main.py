import os
import textx as tx

NOTE = {'bd': 60}


class Model(object):
    def __init__(self, sections):
        self.sections = sections

    def __str__(self):
        out = ''
        for section in self.sections:
            out += '\n' + str(section)
        return out


class Section(object):
    def __init__(self, parent, name, bars):
        self.parent = parent
        self.name = name
        self.bars = bars

    def __str__(self):
        print('toto')
        return self.name + '\n'.join([str(bar) for bar in self.bars])


class Bar(object):

    def __init__(self, parent, ticks, note):
        self.parent = parent
        self.ticks = ticks
        self.note = note
        self.current_tick = 0

    def __str__(self):
        # TODO put midi code inside stp
        out = ''
        for tick in self.ticks:
            out += '\n' + tick
            self.current_tick += 1
        out += ' ' + self.note
        return out




class toto(object):
    def __init__(self, parent, name, pattern, beats):
        self.parent = parent
        self.name = name
        self.pattern = pattern
        self.beats = beats

    def get_bpm(self):
        return self.parent.get_bpm()

    def generate_beat_patterns(self):
        return '\n'.join([str(beat_pattern) for beat_pattern in self.beat_patterns])

    def __str__(self):
        out = self.generate_beat_patterns()
        return out


class BeatPattern(object):
    def __init__(self, parent, beats, pattern):
        self.parent = parent
        self.beats = beats
        self.size = [len(token) for token in ''.join([str(beat) for beat in self.beats]).split('|')]

    def is_beatPattern_matching_with_pattern(self,pattern):

        base_pattern_size = len(pattern.beats)

        if (len(self.beats) != base_pattern_size):
            return False

        for beat_index in range(base_pattern_size):
            if (not self.beats[0].is_beat_size_equals(pattern.beats[beat_index])):
                return False

        return True

    def generate_beats(self):

        if (not self.is_beatPattern_matching_with_pattern(self.parent.pattern)):
            return "Beat pattern is not matching with bar pattern"
        return '\n'.join([str(beat) for beat in self.beats])

    def __str__(self):
        return str(self.size)


class Track(object):
    def __init__(self, parent, name, sections):
        self.parent = parent
        self.name = name
        self.sections = sections

    def generate_sections(self):
        return '\n'.join([str(section) for section in self.sections])

    def __str__(self):
        out = self.generate_sections()
        return out

class Pattern(object):
    def __init__(self, parent, name, beatPattern):
        self.parent = parent
        self.name = name
        self.beatPattern = BeatPattern(self, beatPattern)


if __name__ == '__main__':

    classes = [Model, Bar]

    meta_model = tx.metamodel_from_file('grammar_bars.tx', classes=classes)
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
