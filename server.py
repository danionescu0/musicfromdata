import datetime
import subprocess
import os

import pandas as pd
from audiolazy import str2midi, midi2str
from midiutil import MIDIFile
import paho.mqtt.client as mqtt

import config


def map_value(value, min_value, max_value, min_result, max_result):
    result = min_result + (value - min_value)/(max_value - min_value)*(max_result - min_result)
    return result


def music_from_bulk_data(rawdata: str):
    filename = 'heart_' + str(datetime.datetime.now())
    lines = rawdata.strip().split("\n")
    df = pd.DataFrame({"intensity": lines})
    df['time'] = df.index
    df['intensity'] = pd.to_numeric(df['intensity'], errors='coerce')
    # Drop NaN values from that column
    df.dropna(subset=['intensity'], inplace=True)
    print(df.head(16))

    time = df['time'].values    #this is a numpy array (not a list), you can do mathematical operations directly on the object
    intensity = df['intensity'].values
    millis_per_beat = 930
    times_millis = max(time) - time
    t_data = times_millis/millis_per_beat #rescale time from Myrs to beats
    duration_beats = max(t_data)  #duration in beats (actually, onset of last note)

    y_data = map_value(intensity, min(intensity), max(intensity), 0, 1)
    note_names = ['C1','C2','G2',
                 'C3','E3','G3','A3','B3',
                 'D4','E4','G4','A4','B4',
                 'D5','E5','G5','A5','B5',
                 'D6','E6','F#6','G6','A6']

    note_midis = [str2midi(n) for n in note_names]
    n_notes = len(note_midis)

    midi_data = []
    for i in range(len(y_data)):
        note_index = round(map_value(y_data[i], 0, 1, n_notes-1, 0))
        midi_data.append(note_midis[note_index])


    vel_min,vel_max = 35,127   #minimum and maximum note velocity
    vel_data = []
    for i in range(len(y_data)):
        note_velocity = round(map_value(y_data[i],0,1,vel_min, vel_max))
        vel_data.append(note_velocity)

    bpm = 60  #beats per minute, if bpm = 60, 1 beat = 1 sec
    duration_sec = duration_beats*60/bpm #duration in seconds
    print('Duration:', duration_sec, 'seconds')

    #create midi file object, add tempo
    my_midi_file = MIDIFile(1) #one track
    my_midi_file.addTempo(track=0, time=0, tempo=bpm)
    #add midi notes
    for i in range(len(t_data)):
        my_midi_file.addNote(track=0, channel=0, time=t_data[i], pitch=midi_data[i], volume=vel_data[i], duration=2)
    #create and save the midi file itself
    with open(filename + '.mid', "wb") as f:
        my_midi_file.writeFile(f)

    command = [
        "fluidsynth",
        "-ni",
        config.soundfont_name,
        filename + '.mid',
        "-F",
        filename + '.wav',
        "-r",
        "44100"
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Error:", e)
    try:
        os.remove(filename + '.mid')
    except FileNotFoundError:
        print("The mid file does not exist.")
    print("done rendering")


nr_messages = 0
buffered_result = ""


def buffer_data_chunks(rawdata: str):
    global nr_messages, buffered_result
    nr_messages += 1
    buffered_result += rawdata + "\n"
    if nr_messages >= config.number_messages_once:
        music_from_bulk_data(buffered_result)
        nr_messages = 0
        buffered_result = ""


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT server with result code: {0}, subscribing to topic: {1}".format(str(rc), config.mqtt_topic))
    client.subscribe(config.mqtt_topic)


def on_message(client, userdata, msg):
    buffer_data_chunks(msg.payload.decode('utf-8'))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(config.mqtt_host, 1883, 60)
client.loop_forever()
