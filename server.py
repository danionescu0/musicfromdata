import datetime
import subprocess
import os

import pandas as pd
import pygame
from audiolazy import str2midi, midi2str
from scipy.signal import savgol_filter
from midiutil import MIDIFile
import paho.mqtt.client as mqtt

import config
from utils.music import midi_to_wav, join_wavs
from utils.numeric_utils import map_value


pygame.init()



def music_from_bulk_data(rawdata: str):
    filename = 'heart_' + str(datetime.datetime.now())
    lines = rawdata.strip().split("\n")
    df = pd.DataFrame({"intensity": lines})
    df['time'] = df.index
    df['intensity'] = pd.to_numeric(df['intensity'], errors='coerce')
    # Drop NaN values from that column
    df.dropna(subset=['intensity'], inplace=True)
    time = df['time'].values
    intensity = df['intensity'].values

    #smooth data
    window_length = 7  # Adjust this value to your needs, must be odd
    poly_order = 4  # Polynomial order. You can play around with this value
    intensity = savgol_filter(intensity, window_length, poly_order)

    millis_per_beat = 930
    times_millis = max(time) - time
    t_data = times_millis/millis_per_beat #rescale time from millis to beats
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

    vel_min,vel_max = 20,127   #minimum and maximum note velocity
    vel_data = []
    for i in range(len(y_data)):
        note_velocity = round(map_value(y_data[i],0,1,vel_min, vel_max))
        vel_data.append(note_velocity)

    bpm = 60  #beats per minute, if bpm = 60, 1 beat = 1 sec
    duration_sec = duration_beats*60/bpm #duration in seconds
    print('Duration:', duration_sec, 'seconds')

    # Determine the threshold for the top 10% of velocities
    sorted_velocity_data = sorted(vel_data)
    threshold_index = int(0.9 * len(sorted_velocity_data))
    threshold_velocity = sorted_velocity_data[threshold_index]
    print("Threshold velocity:", threshold_velocity)

    bpm = 60
    duration_sec = duration_beats * 60 / bpm
    print('Duration:', duration_sec, 'seconds')

    # Create 2 MIDI files for smooth and percussion
    low_midi = MIDIFile(1)
    high_midi = MIDIFile(1)

    # Add tempo for both MIDI files
    low_midi.addTempo(track=0, time=0, tempo=bpm)
    high_midi.addTempo(track=0, time=0, tempo=bpm)

    # Add notes based on the threshold condition
    for i in range(len(t_data)):
        if vel_data[i] > threshold_velocity:
            high_midi.addNote(track=0, channel=0, time=t_data[i], pitch=midi_data[i], volume=vel_data[i], duration=2)
        else:
            low_midi.addNote(track=0, channel=0, time=t_data[i], pitch=midi_data[i], volume=vel_data[i], duration=2)

    # Save the low instrument (smooth) MIDI file
    with open(filename + '_low.mid', "wb") as f:
        low_midi.writeFile(f)

    # Save the high instrument (percussion) MIDI file
    with open(filename + '_high.mid', "wb") as f:
        high_midi.writeFile(f)

    midi_to_wav(filename + '_low.mid', filename + '_low.wav', config.soundfont_low)
    midi_to_wav(filename + '_high.mid', filename + '_high.wav', config.soundfont_high)
    join_wavs(filename + '_low.wav', filename + '_high.wav', filename + '_final.wav')

    # # Play sound
    # my_sound = pygame.mixer.Sound(filename + "_final.wav")
    # my_sound.play()


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
