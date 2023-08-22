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


## Setup the project
Goals:
- recive data from MQTT server
- convert data to MIDI then to WAV

Create anaconda environment:
````shell
conda create --name musicfromdata python=3.11.4
conda activate musicfromdata
pip install -r requirements.txt
````