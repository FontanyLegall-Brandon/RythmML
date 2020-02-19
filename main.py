import os
import textx as tx

import time
import rtmidi
from mido import MidiFile, MidiTrack

NOTE = {'bd' : 60}

class Model(object):
    def __init__(self, bpm, patterns, bars, sections, track):
        self.bpm = bpm
        self.patterns = patterns
        self.bars = bars
        self.sections = sections
        self.track = track
        self.beats = beats
        self.mid = MidiFile()

    def generate_code(self):
        return '\n'.join([str(beat) for beat in self.beats])

    def generate_track(self):
        return '\n'.join(self.track)

    def __str__(self):
        res = ''
        res += self.setup()
        res += self.generate_code()
        return res


class Section(object):
    def __init__(self, parent, name, bars):
        self.parent = parent
        self.name = name
        self.bars = bars

    def generate_bar_list(self):
        return '\n'.join([str(bar) for bar in self.bars])

    def __str__(self):
        out = self.name
        out += "\n"+self.generate_bar_list()
        return out

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

class Bar(object):
    def __init__(self, parent, name, pattern, beat_patterns):
        self.parent = parent
        self.name = name
        self.pattern = pattern
        self.beat_patterns = beat_patterns

    def get_bpm(self):
        return self.parent.get_bpm()

    def generate_beat_patterns(self):
        return '\n'.join([str(beat_pattern) for beat_pattern in self.beat_patterns])

    def __str__(self):
        out = self.generate_beat_patterns()
        return out


class Pattern(object):
    def __init__(self, parent, name, beatPattern):
        self.parent = parent
        self.name = name
        self.beatPattern = BeatPattern(self, beatPattern)


class Beat(object):

    def __init__(self, parent, ticks, note):
        self.parent = parent
        self.ticks = ticks[0]
        self.note = note
        self.track = MidiTrack()
        self.mid = parent.mid
        self.mid.append(self.track)
        self.current_tick = 0

    def __str__(self):
        # TODO put midi code inside stp
        out = ''
        for tick in self.ticks:
            if tick == 'x':
                self.play_note()
            self.current_tick += 1
        return out

    def play_note(self):
        note_on = [0x90, NOTE[self.note], 112]
        time.sleep(60 / (120 * 4))  # TODO 60 / bpm * tick_number
        note_off = [0x80, NOTE[self.note], 112]
        self.track.append(self.mid.Message('note_on', note=NOTE[self.note], velocity=self.volume[i], time=self.time[i]))
        midiout.send_message(note_on)

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

if __name__ == '__main__':

    classes = [Model, BeatPattern, Pattern, Track, Section]

    meta_model = tx.metamodel_from_file('grammar_pattern.tx', classes=classes)
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
