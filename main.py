import os
import textx as tx
from midiutil import MIDIFile

NOTE = {"drum": {"bd": 35, "sd": 38, "rc": 51, "xH": 64},
        "piano": {"B2":47,"B3":59,"B4":71,"B5":83,"e2":28,"e4":52,"e5":64,"G2":43,"G4":67,"G6":91,}}


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

        channel = 11
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
            MyMIDI.addTempo(track, time, self.bpm)



        for section_config in sections_config:
            for key in section_config.keys():
                if type(key) is int:
                    for note_list in section_config[key]:
                        for note in note_list.notes:
                            MyMIDI.addNote(
                                midi_tracks[note_list.instrument],
                                channel,
                                NOTE[note_list.instrument][note],
                                key,
                                duration,
                                volume,
                            )
            print(section_config)

        with open("major-scale.mid", "wb") as output_file:
            MyMIDI.writeFile(output_file)

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
        out["startTime"] = self.startTime
        if self.repeatCount > 0:
            for bar in self.get_bars():
                tick_offset = 0

                for i in range(self.repeatCount):
                    for beats in bar.ticks[0].split("|"):
                        for tick in beats:
                            if tick in ["x"]:
                                if tick_offset not in out:
                                    out[tick_offset] = [bar.note]
                                else:
                                    out[tick_offset].append(bar.note)
                            tick_offset += 1
        else:
            for bar in self.get_bars():
                tick_offset = 0
                for beats in bar.ticks[0].split("|"):
                    for tick in beats:
                        if tick in ["x"]:
                            if tick_offset not in out:
                                out[tick_offset] = [bar.note]
                            else:
                                out[tick_offset].append(bar.note)
                        tick_offset += 1
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
