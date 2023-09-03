# musicfromdata
From Data to Melody: Sonifying Bio-signals for YouTube Live Streams and Direct Playback

Imagine crafting a tune from the very rhythm of a human heartbeat. This is precisely what we are achieving in our innovative venture: converting bio-signal data, such as EMG and EKG, into melodies. I often describe this magical transformation as "making music from the heart."

Overview of the Project:
We utilize EKG and EMG sensors to capture bio-signals from the human body. This data is then converted into a musical format. The process unfolds in several steps:

Data Acquisition: For capturing data, we employ an ESP32 board integrated with sensor pads, complemented by the ESP32 development board. The prime tasks are to extract signals from the human body, preprocess them for noise reduction, and then relay this data over the internet through an MQTT connection.

Data Sonification: On the receiving end, a dedicated Python server actively listens to the incoming MQTT data stream. This data is then transformed into a MIDI (Musical Instrument Digital Interface) file utilizing a sonification method inspired by SYSTEMSounds.

Audio Conversion:

Once the data is sonified into a MIDI format, our Python script further converts it into a WAV file – a standard audio format suitable for playback.
For this transformation, we harness a software named "fluidsynth." Fluidsynth requires a "soundfont" – essentially a virtual musical instrument – to map MIDI data into perceptible sound. Soundfonts are available for download online and can be customized or created using software. Find more about soundfonts here.
Streaming & Playback: The culminating step involves either playing the WAV file locally or uploading it to a streaming platform, such as YouTube Music.

Acknowledgements:
My project owes much to the pioneering work of SYSTEMSounds. For more information, check out their sonification tutorials on GitHub: https://github.com/SYSTEMSounds/sonification-tutorials


## Develop the project 
Note: we're using an ubuntu based system

Goals:
- receive data from MQTT server
- convert data to MIDI then to WAV
- play music / upload to YouTube Music

1) Create anaconda environment:
````shell
conda create --name musicfromdata python=3.9.17
conda activate musicfromdata
pip install -r requirements.txt
````

2) Install fluidsynth:

````shell
sudo apt-get install -y fluidsynth
````

3) Install mosquitto and mosquitto client, if you don't have other mqtt broker

````shell
sudo apt update
sudo apt install mosquitto mosquitto-clients
sudo systemctl status mosquitto
````
Then bind it to all interfaces and allow no password connections
````shell
sudo vi /etc/mosquitto/mosquitto.conf
````
then add the lines:

````shell
allow_anonymous true
listener 1883
````
then restart:
````shell
sudo systemctl restart mosquitto
````

4) Run the project:

````shell
python server.py
````

5) Emulate ESP32 EKG data [OPTIONAL]:

````shell
./emulateESP32.sh localhost /datatomusic
````
This will push data from the heart.csv sample into MQTT
![EKG](https://github.com/danionescu0/musicfromdata/blob/main/resources/ekg1.png)

6) Display EKG or EMG graph on screen

````shell
python plot.py
````


## Setup the ESP32 data acquisition board

Components:

- ESP32 board
- AD8232 heart monitor sensor: Setup the esp32 data acuisition board
- 3 pads
- a power supply that runs on batteries (to eliminate electrical noise), when using the laptop please disconnect the power

Steps:

- replace ssid, password, mqtt_server to your own values
- upload the esp32 code to the board
- monitor the board has connected succesfully to the mqtt server 
- test if you're receiving the data for example using mosquitto_sub:

````shell
mosquitto_sub -h your_mqtt_host -p 1883 -t /datatomusic
````

## Setup jupyter notebook to play with data visualization techniques that enable data to wav conversion
````shell
conda create --name musicfromdatajupyter python=3.9.17
conda activate musicfromdatajupyter
pip install jupyter
````

To run
````shell
jupyter notebook processing_music.ipynb
````
