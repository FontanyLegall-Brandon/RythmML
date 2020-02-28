import json
import re


if __name__ == "__main__":

    f = open("notefile", "r")
    f_drum = open("drumNoteFile", "r")
    f_all_instrument = open("all_instrument_number", "r")


    note_input = [line.strip() for line in f]
    note_drum_input = [line.strip() for line in f_drum]
    all_instrument = [line.strip() for line in f_all_instrument]
    outfile = open("jsonMidiBind.txt", "w")

    notes = dict()

    for instrument in all_instrument :
        tmp = instrument.split()
        instrument_name = ""
        notes[instrument_name.join([x for x in tmp[1:]])] = dict()

    piano_note_association = dict()
    drum_note_association = dict()

    for note in note_input :
        tmp = re.split(r'\t+', note)
        piano_note_association[tmp[3] if tmp[3].find("/") == -1 else tmp[3].split("/")[1]] = tmp[0]

    for note in note_drum_input:
        tmp = note.split()
        tmp_note_to_string = ""
        drum_note_association[tmp_note_to_string.join([x for x in tmp[2:]])] = tmp[0]

    notes["drum"] = drum_note_association
    notes["piano"] = piano_note_association

    print(notes)
    outfile.write(str(notes))

    # Close the file
    f.close()


