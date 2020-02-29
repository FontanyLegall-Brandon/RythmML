# RythmML

## Install

Required python3. To install dependencies, please run the following command :

```shell script
pip3 install -r requirements.txt
```

## Run
Create your rml(Rythm language) into samples folder and then run main.py
After run, it is possible to retrieve your work to the format mid directly into the working directory.

## Usage 

```shell script
usage: main.py [-h] [--input INPUT] [--play]

optional arguments:
  -h, --help     show this help message and exit
  --input INPUT  Input .rml file
  --play, -p     Input .rml file
```

#### Compile .rml file to .mid

```shell script
$ python3 main.py --input samples/BillieJean.rml
Translating samples/BillieJean.rml
Midi file saved in out/BillieJean.mid
```

#### Compile & play live

Simply add `--play` flag in command as follow :

```shell script
python3 main.py --input samples/BillieJean.rml --play
```
