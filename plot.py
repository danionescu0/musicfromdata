import datetime
import subprocess
import os
import threading

import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import signal
import sys

import config

nr_messages = 0
buffered_result = ""
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

stop_threads = False


# Define a signal handler function for Ctrl+C
def signal_handler(sig, frame):
    global stop_threads
    print("Ctrl+C captured. Stopping threads and exiting gracefully.")
    stop_threads = True
    client.disconnect()

    sys.exit(0)


# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)


def animate(i):
    global xs, ys
    if stop_threads:
        return
    with data_lock:
        ax.clear()
        ax.plot(xs, ys)
        # Calculate indices for tick positions
        total_ticks = len(xs)
        desired_ticks = 15
        step = max(total_ticks // desired_ticks, 1)
        tick_indices = np.arange(0, total_ticks, step)
        # Extract numerical indices for tick positions
        tick_positions = [tick_indices[i] for i in range(len(tick_indices))]
        # Set x-axis tick positions and labels
        ax.set_xticks(tick_positions)
        ax.set_xticklabels([xs[i] for i in tick_indices])
        # Rotate x-axis tick labels for better visibility (optional)
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('Heart signal over time')
        plt.ylabel('mV')


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(config.mqtt_topic)


data_lock = threading.Lock()


def on_message(client, userdata, msg):
    global xs, ys, nr_messages
    rawdata = msg.payload.decode('utf-8')
    if rawdata == "!":
        return
    nr_messages += 1
    try:
        float(rawdata)
    except:
        return
    with data_lock:  # Acquire the lock before modifying xs and ys
        xs.append(datetime.datetime.now().strftime('%M:%S.%f'))
        ys.append(float(rawdata))
        xs = xs[-900:]
        ys = ys[-900:]


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(config.mqtt_host, 1883, 60)
mqtt_thread = threading.Thread(target=client.loop_forever)
mqtt_thread.start()

ani = FuncAnimation(fig, animate, interval=250)
plt.show()

mqtt_thread.join()
client.disconnect()
