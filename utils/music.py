from midi2audio import FluidSynth
from pydub import AudioSegment


def midi_to_wav(input_midi: str, output_wav: str, sf2_path: str):
    fs = FluidSynth(sf2_path)
    fs.midi_to_audio(input_midi, output_wav)
    print(f'Audio saved to {output_wav}')


def join_wavs(filename_1: str, filename_2:str, result: str):
    #Load the two audio files
    file1 = AudioSegment.from_wav(filename_1)
    file2 = AudioSegment.from_wav(filename_2)
    # Overlay the two files
    combined_audio = file1.overlay(file2)
    # Export the combined audio to a new file
    combined_audio.export(result, format="wav")