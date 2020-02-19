import os
import textx as tx

import time
import rtmidi
from mido import MidiFile, MidiTrack

NOTE = {'bd' : 60}

class Model(object):
    def __init__(self, beats):
        self.beats = beats
        self.mid = MidiFile()

    def generate_code(self):
        return '\n'.join([str(beat) for beat in self.beats])

    def __str__(self):
        res = ''
        res += self.setup()
        res += self.generate_code()
        return res


class Section(object):
    def __init__(self, parent, name, bar_list):
        self.parent = parent
        self.name = name
        self.bar_list = bar_list

    def generate_bar_list(self):
        return '\n'.join([str(bar) for bar in self.bar_list])

    def __str__(self):
        out = self.generate_bar_list()
        return out


class Track(object):
    def __init__(self, parent, name, section_list):
        self.parent = parent
        self.name = name
        self.section_list = section_list

    def generate_section_list(self):
        return '\n'.join([str(section) for section in self.section_list])

    def __str__(self):
        out = self.generate_section_list()
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
        self.beatPattern = beatPattern  # liste d'entiers


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
        self.pattern = pattern

    def is_beatPattern_matching_with_pattern(self, pattern):

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


if __name__ == '__main__':

    classes = [Model, Beat]

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
