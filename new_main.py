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
        return 'Section ' + self.name + '\n' + '\n'.join([str(bar) for bar in self.bars]) + '\n'


class Bar(object):

    def __init__(self, parent, ticks, note):
        self.parent = parent
        self.ticks = ticks
        self.note = note
        self.current_tick = 0

    def __str__(self):
        # TODO put midi code inside stp
        return '\n'.join([tick for tick in self.ticks]) + ' ' + self.note


if __name__ == '__main__':

    classes = [Model, Bar, Section]

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
