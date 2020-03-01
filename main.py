import os
import sys
import time
def blockPrint():
    sys.stdout = open(os.devnull, 'w')
def enablePrint():
    sys.stdout = sys.__stdout__

blockPrint()
import pygame
import pygame.midi
enablePrint()

import textx as tx
from midiutil import MIDIFile
from copy import copy
from pathlib import Path
import argparse
# note and instrument binds


def parse(filepath):
    dico = {}
    with open(filepath) as fh:
        for line in fh:
            if len(line.strip().split(' ', 1)) == 2:
                key, value = line.strip().split(' ', 1)
            else:
                key, value = line.strip().split('\t', 1)
            value = ''.join(value.split(' '))
            dico[value] = key.strip()
    return dico


def parse_drum(filepath):
    dico = {}
    with open(filepath) as fh:
        for line in fh:
            key, note, value = line.strip().split(' ', 2)
            value = ''.join(value.split(' '))
            dico[value] = key.strip()
    return dico


drum_notes = parse_drum('note binder/drumNoteFile')
notes = parse('note binder/notes')
instruments = parse('note binder/all_instrument_number')


class Model(object):
    def __init__(self, binds,notePatterns, sections, track, bpm, patterns):
        self.sections = sections
        self.binds = binds
        self.track = track
        self.bpm = bpm
        self.patterns = patterns
        self.notePatterns = notePatterns
        self.name = None

    def validate(self):
        for section in self.sections:
            section.validate()

    def __str__(self):
        out = ""
        out += str(self.bpm) + "\n\n"
        out += "\n".join([str(pattern) for pattern in self.patterns])
        out += "\n".join([str(section) for section in self.sections])
        out += str(self.track)
        return out

    def build_midi(self, output_name):
        sections_config = [e.get_notes(self.notePatterns) for e in self.track.sections_config]
        instruments_set = list()

        for section_config in sections_config:
            for value in section_config.values():
                if type(value) is list:
                    instruments_set += value
        instruments_set = set(list(map(lambda e: e.instrument, instruments_set)))

        midi_tracks = dict()

        time = 0  # In beats
        duration = 1  # In beats
        volume = 100

        i = 0
        for instrument in instruments_set:
            midi_tracks[instrument] = i
            i = i + 1

        MyMIDI = MIDIFile(
            len(instruments_set)
        )  # One track, defaults to format 1 (tempo track is created
        # automatically)

        channels = {}
        channel_number = 0
        for instrument in instruments_set:
            if channel_number > 15: # only 16 channels from 0 to 15
                return
            if instrument == 'drum': # channel 9 reserved for drum
                channels[instrument] = 9
            else:
                if channel_number == 9:
                    channel_number += 1
                channels[instrument] = channel_number
            channel_number += 1

        for track in midi_tracks.values():
            MyMIDI.addTempo(track, time, self.bpm)

        for section_config in sections_config:
            for key in section_config.keys():
                if type(key) is int or type(key) is float:
                    for note_list in section_config[key]:
                        for note in note_list.notes:
                            track = midi_tracks[note_list.instrument]
                            channel = channels[note_list.instrument]
                            midi_number = drum_notes[note] if note_list.instrument == 'drum' else notes[note]
                            if not note_list.instrument == 'drum':
                                program = instruments[note_list.instrument]
                                MyMIDI.addProgramChange(int(track), int(channel), 0, int(program))

                            MyMIDI.addNote(int(track),
                                           int(channel),
                                           int(midi_number),
                                           key,
                                           note_list.duration,
                                           volume)

        self.name = output_name.replace('.rml', '')
        with open("out/{}.mid".format(self.name), "wb") as output_file:
            MyMIDI.writeFile(output_file)
        print("Midi file saved in out/{}.mid".format(self.name))

    def play(self):
        pygame.init()
        pygame.display.init()
        pygame.display.set_mode((250, 250))
        pygame.display.set_caption(self.name)
        pygame.mixer.music.load("out/{}.mid".format(self.name))
        pygame.mixer.music.play()
        clock = pygame.time.Clock()

        pygame.midi.init()
        player = pygame.midi.Output(pygame.midi.get_default_output_id())
        keys = dict()
        while pygame.mixer.music.get_busy():
            # check if playback has finished
            if len(self.binds) > 0:
                for e in pygame.event.get():
                    # Exit program on pygame window close
                    if e.type == pygame.QUIT:
                        sys.exit(0)

                    # Add note on keydown
                    if e.type == pygame.KEYDOWN:
                        keys[e.key] = e.unicode
                        for bind in self.binds:
                            if bind.key == e.unicode:
                                print('ON', bind)
                                for note in bind.notes:
                                    player.set_instrument(int(instruments[bind.instrument]))
                                    midi_number = drum_notes[note] if bind.instrument == 'drum' else notes[note]
                                    player.note_on(int(midi_number), 127)

                    # mute note on release
                    if e.type == pygame.KEYUP:
                        for bind in self.binds:
                            if bind.key == keys[e.key]:
                                print('OFF', bind)
                                for note in bind.notes:
                                    player.set_instrument(int(instruments[bind.instrument]))
                                    midi_number = drum_notes[note] if bind.instrument == 'drum' else notes[note]
                                    player.note_off(int(midi_number), 127)
            clock.tick(30)

class Pattern(object):
    def __init__(self, parent, name, beat_pattern):
        self.parent = parent
        self.name = name
        self.beat_pattern = beat_pattern

    def get_beats_size(self):
        return [len(beat) for beat in repr(self).split("|")]

    def __repr__(self):
        return "".join(str(token) for token in self.beat_pattern)

    def __str__(self):
        return self.name + " " + str(self.beat_pattern) + "\n\n"


class Track(object):
    def __init__(self, parent, name, sections_config):
        self.parent = parent
        self.name = name
        self.sections_config = sections_config

    def __str__(self):

        return (
            "\nTrack "
            + self.name
            + "\n"
            + "\n".join(
                [str(section_config) for section_config in self.sections_config]
            )
            + "\n"
        )


class Section:
    def __init__(self, parent, pattern, name, bars):
        self.parent = parent
        self.name = name
        self.bars = bars
        self.pattern = pattern

    def validate(self):
        size_tab = self.pattern.get_beats_size()
        for bar in self.bars:
            if bar.get_beats_size() != size_tab:
                raise SyntaxError(
                    "Bar {} mismatch with pattern {} = {}".format(
                        repr(bar), self.pattern.name, repr(self.pattern)
                    )
                )

    def __str__(self):
        return (
            "Pattern "
            + str(self.pattern)
            + repr(self.pattern)
            + "Section "
            + self.name
            + "\n"
            + "\n".join([str(bar) for bar in self.bars])
            + "\n"
        )


class SectionConfig:
    def __init__(self, parent, startTime, repeatCount, section):
        self.parent = parent
        self.startTime = startTime
        self.repeatCount = repeatCount
        self.section = section

    def get_bars(self):
        return self.section.bars

    def get_notes(self, notes_patterns):
        out = dict()
        out["startTime"] = self.startTime * 4
        notes = dict()
        for e in notes_patterns:
            notes[e.token] = e.duration_multiplier
        if self.repeatCount > 0:
            for bar in self.get_bars():
                tick_offset = self.startTime * 4

                for i in range(self.repeatCount):

                    bars = bar.ticks[0].split("|")
                    bars_size = [len(bar) for bar in bars]

                    for i in range(len(bars)):
                        for tick in bars[i]:
                            if tick in notes.keys():
                                bar.note.set_duration(notes[tick] * 4 / bars_size[i])
                                if tick_offset not in out:
                                    out[tick_offset] = [copy(bar.note)]
                                else:
                                    out[tick_offset].append(copy(bar.note))
                            else:
                                if tick != '.':
                                    raise ValueError('Note "{}" not defined'.format(tick))
                            tick_offset += 4 / bars_size[i]

        else:
            for bar in self.get_bars():
                tick_offset = self.startTime * 4
                bars = bar.ticks[0].split("|")
                bars_size = [len(bar) for bar in bars]

                for i in range(len(bars)):
                    for tick in bars[i]:
                        if tick in notes.keys():
                            bar.note.set_duration(notes[tick] * 4 / bars_size[i])
                            if tick_offset not in out:
                                out[tick_offset] = [copy(bar.note)]
                            else:
                                out[tick_offset].append(copy(bar.note))
                        else:
                            if tick != '.':
                                raise ValueError('Note "{}" not defined'.format(tick))
                        tick_offset += 4 / bars_size[i]
        return out

    def __str__(self):
        if self.startTime < 0:
            raise SyntaxError("Start time can't be lower than 0")
        return (
            "section modifier : "
            + str(self.startTime)
            + " : "
            + str(self.repeatCount)
            + " section "
            + str(self.section)
        )


class Note:
    def __init__(self, parent, instrument, notes):
        self.parent = parent
        self.instrument = instrument
        self.notes = notes
        self.duration = -1

    def set_duration(self, duration):
        self.duration = duration

    def __repr__(self):
        return "<Notes {} {}>".format(self.instrument, self.notes)

    def __str__(self):
        return "<Notes {} {}>".format(self.instrument, self.notes)


class Bar(object):
    def __init__(self, parent, ticks, note):
        self.parent = parent
        self.ticks = ticks
        self.note = note
        self.current_tick = 0

    def get_beats_size(self):
        return [len(beat) for beat in repr(self).split("|")]

    def __repr__(self):
        return "".join(str(tick) for tick in self.ticks)

    def __str__(self):
        # TODO put midi code inside stp
        return "\n".join([tick for tick in self.ticks]) + " " + repr(self.note)


class Bind(object):
    def __init__(self, parent, key, instrument, notes):
        self.parent = parent
        self.key = key
        self.instrument = instrument
        self.notes = notes

    def __str__(self):
        return "<Bind key={} instrument={} notes={}>".format(self.key, self.instrument, self.notes)


class NotePattern(object):
    def __init__(self, parent, token, duration_multiplier):
        self.parent = parent
        self.token = token
        self.duration_multiplier = duration_multiplier

    def __str__(self):
        return "<NotePattern token={} duration_multiplier={}>".format(self.token, self.duration_multiplier)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="Input .rml file",
                        type=str)
    parser.add_argument('--play', '-p', help="Input .rml file", action='store_true')

    return parser.parse_args()

if __name__ == "__main__":
    Path("./out").mkdir(parents=True, exist_ok=True)

    classes = [Model,Bind,NotePattern, Bar, SectionConfig, Track, Pattern, Section, Note]

    meta_model = tx.metamodel_from_file("grammar.tx", classes=classes)

    args = parse_args()
    if args.input is not None:
        if os.path.isfile(args.input):
            print("Translating {}".format(args.input))
            model = meta_model.model_from_file(args.input)
            model.validate()
            model.build_midi(args.input.split('/')[-1])
            if args.play :
                model.play()
        else:
            print("ERROR - file {} not found".format(args.input))
    else:
        for file_name in os.listdir("./samples"):
            print("Translating {}".format(file_name))
            model = meta_model.model_from_file("samples/{}".format(file_name))

            model.validate()

            model.build_midi(file_name)
            model.play()
