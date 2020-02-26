import os
import textx as tx
from midiutil import MIDIFile
from copy import copy
import pygame
from pathlib import Path


NOTE = {
        "drum": {"bd": 35, "sd": 38, "rc": 51, "xH": 64, "sh": 70},
        "piano": {"A3": 57, "Db4": 61, "Gb4": 66, "B3": 59, "Eb4": 63, "Ab4": 68,  "E4": 64, "A4": 69,
                  "A6": 93, "A3": 57, "D4": 62},
        "bass": {"Gb1": 30, "Db2": 37, "E2": 40, "Gb2": 42, "B1": 35}
        }

CHANNEL = {"drum": 9, "piano": 0, "bass": 1}


class Model(object):
    def __init__(self, sections, track, bpm, patterns):
        self.sections = sections
        self.track = track
        self.bpm = bpm
        self.patterns = patterns

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

    def __repr__(self):

        sections_config = [e.get_notes() for e in self.track.sections_config]
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

        for track in midi_tracks.values():
            MyMIDI.addProgramChange(0, 1, 0, 39)
            MyMIDI.addProgramChange(0, 0, 0, 5)
            MyMIDI.addProgramChange(0, 9, 0, 35)
            MyMIDI.addTempo(track, time, self.bpm)

        for section_config in sections_config:
            for key in section_config.keys():
                print(key)
                if type(key) is int or type(key) is float:
                    for note_list in section_config[key]:
                        print(note_list.duration)
                        for note in note_list.notes:
                            print(note)
                            MyMIDI.addNote(
                                midi_tracks[note_list.instrument],
                                CHANNEL[note_list.instrument],
                                NOTE[note_list.instrument][note],
                                key,
                                note_list.duration,
                                volume,
                            )
            print(section_config)

        with open("major-scale.mid", "wb") as output_file:
            MyMIDI.writeFile(output_file)
        pygame.init()
        pygame.mixer.music.load("major-scale.mid")
        pygame.mixer.music.play()
        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            # check if playback has finished
            clock.tick(30)

        return str(instruments_set)


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

    def get_notes(self):
        out = dict()
        out["startTime"] = self.startTime * 4
        if self.repeatCount > 0:
            for bar in self.get_bars():
                tick_offset = self.startTime * 4

                for i in range(self.repeatCount):

                    bars = bar.ticks[0].split("|")
                    bars_size = [len(bar) for bar in bars]

                    for i in range(len(bars)):
                        for tick in bars[i]:
                            if tick in ["x"]:
                                bar.note.set_duration(4 / bars_size[i])
                                if tick_offset not in out:
                                    out[tick_offset] = [copy(bar.note)]
                                else:
                                    out[tick_offset].append(copy(bar.note))
                            tick_offset += 4 / bars_size[i]
        else:
            for bar in self.get_bars():
                tick_offset = self.startTime * 4
                bars = bar.ticks[0].split("|")
                bars_size = [len(bar) for bar in bars]

                for i in range(len(bars)):
                    for tick in bars[i]:
                        if tick in ["x"]:
                            bar.note.set_duration(4 / bars_size[i])
                            if tick_offset not in out:
                                out[tick_offset] = [copy(bar.note)]
                            else:
                                out[tick_offset].append(copy(bar.note))
                        tick_offset += 4 / bars_size[i]
        return out

    def __repr__(self):
        return str(self.get_notes())

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


if __name__ == "__main__":
    Path("./out").mkdir(parents=True, exist_ok=True)

    classes = [Model, Bar, SectionConfig, Track, Pattern, Section, Note]

    meta_model = tx.metamodel_from_file("grammar.tx", classes=classes)
    for file_name in os.listdir("./samples"):
        print("Translating {}".format(file_name))
        model = meta_model.model_from_file("samples/{}".format(file_name))

        model.validate()

        out = open("out/{}".format(file_name.replace(".rml", ".py")), "w")
        print(model, file=out)
        print(model)
        print("REPR OF MODEL")
        print(repr(model))
        out.close()
