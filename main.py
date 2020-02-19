import os
import textx as tx

NOTE = {'bd':'BASSDRUM'}

class Model(object):
    def __init__(self, parent, bpm, bar_list, section_list, track):
        self.parent = parent
        self.bpm = bpm
        self.bar_list = bar_list
        self.section_list = section_list
        self.track = track

    def generate_rtmidiout_and_port(self):
        return 'midiout = rtmidi.MidiOut()\navailable_ports = midiout.get_ports()\n'.format()

    def generate_track(self):
        return '\n'.join(self.track)

    def __str__(self):
        out = self.generate_rtmidiout_and_port()
        out += self.generate_track()
        return out

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
        self.beatPattern = beatPattern # liste d'entiers

class Tick(object):
    def __init__(self, parent, value):
        self.parent = parent
        self.value = value


class Beat(object):
    def __init__(self, parent, ticks, note):
        self.parent = parent
        self.ticks = ticks
        self.note = note
        self.bpm = parent.get_bpm()
        self.number_of_ticks = (len(self.ticks)+1)

    def is_beat_size_equals(self, beat):
        return len(self.ticks) == len(beat.ticks)

    def generate(self):
        for tick in self.ticks:
            if(tick.value == '.'):
                return '\n'.join('time.sleep('+str(60/(self.bpm*self.number_of_ticks))+')')
            else :
                note = Note(self,self.note)
                return '\n'.join(str(note))

    def __str__(self):
        out = self.generate()
        return out

class Separator(object):
    def __init__(self, parent, value):
        self.parent = parent
        self.value = value

class Note(object):
    def __init__(self, parent, value):
        self.parent = parent
        self.value = value

    def generate(self):
        out = ''
        out += '\nnote_on = [0x90',NOTE[self.value],'112]'
        out += '\nnote_on = [0x80', NOTE[self.value], '112]'
        out += '\nmidiout.send_message(note_on)'
        out += '\n'.join('time.sleep('+str(60/(self.parent.bpm*self.parent.number_of_ticks))+')')
        return out

    def __str__(self):
        out = self.generate()
        return out

class BeatPattern(object):
    def __init__(self, parent, beats):
        self.parent = parent
        self.beats = beats

    def get_bpm(self):
        return self.parent.get_bpm()

    def is_beatPattern_matching_with_pattern(self,pattern):

        base_pattern_size = len(pattern.beats)

        if(len(self.beats) != base_pattern_size):
            return False

        for beat_index in range(base_pattern_size) :
            if(not self.beats[0].is_beat_size_equals(pattern.beats[beat_index])):
                return False

        return True

    def generate_beats(self):

        if(not self.is_beatPattern_matching_with_pattern(self.parent.pattern)):
            return "Beat pattern is not matching with bar pattern"
        return '\n'.join([str(beat) for beat in self.beats])


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