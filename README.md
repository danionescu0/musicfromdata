# musicfromdata
From data to YouTube Live streams: Create music streams from various types of data for example EMG or EKG

A project made possbile with the work of SYSTEMSounds: https://github.com/SYSTEMSounds/sonification-tutorials

## Setup jupyter notebook to play with data visualization techniques that enable data to wav conversion
````shell
conda create --name musicfromdatajupyter python=3.9.17
conda activate musicfromdatajupyter
pip install jupyter
````

To run
````shell
jupyter notebook
````


## Setup the python server
Goals:
- recive data from MQTT server
- convert data to MIDI then to WAV

Create anaconda environment:
````shell
conda create --name musicfromdata python=3.9.17
conda activate musicfromdata
pip install -r requirements.txt
````

Install fluidsynth:

````shell
sudo apt-get install -y fluidsynth
````
Run the project:

````shell
python server.py
````

## Setup the esp32 data acquisition board

Components:

- ESP32 board
- AD8232 heart monitor sensor: Setup the esp32 data acuisition board
- 3 pads
- a power supply that runs on batteries (to eliminate electrical noise), when using the laptop please disconnect the power

Steps:

- replace ssid, password, mqtt_server to your own values
- upload the esp32 code to the board
- monitor the board has connected succesfully to the mqtt server 
- test if you're receiving the data for example:

````shell
mosquitto_sub -h your_mqtt_host -p 1883 -t /datatomusic
````