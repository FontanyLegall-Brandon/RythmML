import os
import textx as tx
import mido 

NOTE = {'bd': 60}


class Model(object):
    def __init__(self, sections, tracks, bpm, patterns):
        self.sections = sections
        self.tracks = tracks
        self.bpm = bpm
        self.patterns = patterns

    def validate(self):
        for section in self.sections :
            section.validate()

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
        self.beat_pattern = beat_pattern

    def get_beats_size(self):
        return [len(beat) for beat in repr(self).split('|')]
    
    def __repr__(self):
        return ''.join(str(token) for token in self.beat_pattern)

    def __str__(self):
        return self.name + ' ' + str(self.beat_pattern) + '\n\n'


class Track(object):
    def __init__(self, parent, name, sections):
        self.parent = parent
        self.name = name
        self.sections = sections

    def __str__(self):
        return '\nTrack ' + self.name + '\n' + '\n'.join([section.name for section in self.sections]) + '\n'


class Section(object):
    def __init__(self, parent, pattern, name, bars):
        self.parent = parent
        self.name = name
        self.bars = bars
        self.pattern = pattern

    def validate(self):
        size_tab = self.pattern.get_beats_size()
        print(size_tab)
        for bar in self.bars :
            if(bar.get_beats_size() != size_tab):
                raise SyntaxError("Bar {} mismatch with pattern {} = {}".format(repr(bar),
                                                                                self.pattern.name,
                                                                                repr(self.pattern)))
                
    def __str__(self):
        return 'Pattern' + str(self.pattern) +'Section ' + self.name + '\n' + '\n'.join([str(bar) for bar in self.bars]) + '\n'


class Bar(object):

    def __init__(self, parent, ticks, note):
        self.parent = parent
        self.ticks = ticks
        self.note = note
        self.current_tick = 0

    def get_beats_size(self):
        return [len(beat) for beat in repr(self).split('|')]

    def __repr__(self):
        return ''.join(str(tick) for tick in self.ticks)
    
    def __str__(self):
        # TODO put midi code inside stp
        return '\n'.join([tick for tick in self.ticks]) + ' ' + self.note


if __name__ == '__main__':

    classes = [Model, Bar, Section, Track, Pattern]

    meta_model = tx.metamodel_from_file('grammar.tx', classes=classes)
    for file_name in os.listdir("./samples"):
        print("Translating {}".format(file_name))
        model = meta_model.model_from_file('samples/{}'.format(file_name))

        model.validate()

        out = open('out/{}'.format(file_name.replace('.rml', '.py')), 'w')
        print(model, file=out)
        print(model)
        out.close()