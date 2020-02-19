import os
import textx as tx

NOTE = {'bd':'BASSDRUM'}

class Model(object):
    def __init__(self, bpm, patterns):
        self.bpm = bpm
        self.patterns = patterns

    def generate_rtmidiout_and_port(self):
        return 'midiout = rtmidi.MidiOut()\navailable_ports = midiout.get_ports()\n'.format()

    #def generate_track(self):
     #   return '\n'.join(self.track)

    def __str__(self):
     #   out = self.generate_rtmidiout_and_port()
      #  out += self.generate_track()
        return '\n'.join([str(e) for e in self.patterns])

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
        self.size = [len(token) for token in ''.join([str(beat) for beat in self.beats]).split('|')]

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

    def __str__(self):
        return str(self.size)


if __name__ == "__main__":

    classes = [Model, BeatPattern, Pattern]

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

        out = open('out/{}'.format(file_name.replace('.rml', '.midi')), 'w')
        print(model, file=out)
        out.close()
        print(model)