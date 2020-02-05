import textx as tx

type_builtins = {}

if __name__ == '__main__':

    classes = []
    meta_model = tx.metamodel_from_file('grammar.tx', classes=classes, builtins=type_builtins)