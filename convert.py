from midi2audio import FluidSynth

import fluidsynth
import soundfile as sf



# Path to the SoundFont file (replace with the actual path)
soundfont_path = "./Timpani v2.0.sf2"

# Input MIDI file
input_midi = "heart.mid"

# Output WAV file
output_wav = "output.wav"




# Initialize FluidSynth with the custom SoundFont
fs = fluidsynth.Synth()
fs.start(driver="alsa")

sfid = fs.sfload(soundfont_path)
fs.program_select(0, sfid, 0, 0)

# Create an audio driver to capture the audio output
adriver = fluidsynth.AudioDriver()

# Load the MIDI file and play it while capturing the audio
fs.midifile_load(input_midi)
audio_data = adriver.get_samples()

# Save the captured audio data as a WAV file
sf.write(output_wav, audio_data, adriver.samplerate)

# Clean up
adriver.close()
fs.delete()

print("Conversion complete!")
