import os
import textx as tx

class Model(object):
    def __init__(self, bpm, bars, sections, track):
        self.bpm = bpm
        self.bars = bars
        self.sections = sections
        self.track = track

    def __str__(self):
        return "BPM = {}".format(self.bpm) + str(self.track)


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

class Bar(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def get_bpm(self):
        return self.parent.get_bpm()

    def __str__(self):
        out ="BAR" +self.name
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

if __name__ == "__main__":


    classes = [Model, Section,Track,Bar]

    meta_model = tx.metamodel_from_file('grammar2.tx', classes=classes)
    try:
        os.mkdir('out')
    except FileExistsError:
        pass

    for file_name in os.listdir('samples2'):

        print("Translating {}".format(file_name))
        model = meta_model.model_from_file('samples2/{}'.format(file_name))

        out = open('out/{}'.format(file_name.replace('.rml', '.alt_midi')), 'w')
        print(model, file=out)
        print(model)
        out.close()