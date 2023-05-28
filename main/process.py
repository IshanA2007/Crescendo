import librosa
import numpy as np
import soundfile as sf
import openai
import math
import magenta.music as mm
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
import random

# figure out how to make this so not everyone can see my api key

openai.api_key = "blahblah"
notes = {
    "C0": 16.35,
    "C#0/Db0": 17.32,
    "D0": 18.35,
    "D#0/Eb0": 19.45,
    "E0": 20.60,
    "F0": 21.83,
    "F#0/Gb0": 23.12,
    "G0": 24.50,
    "G#0/Ab0": 25.96,
    "A0": 27.50,
    "A#0/Bb0": 29.14,
    "B0": 30.87,
    "C1": 32.70,
    "C#1/Db1": 34.65,
    "D1": 36.71,
    "D#1/Eb1": 38.89,
    "E1": 41.20,
    "F1": 43.65,
    "F#1/Gb1": 46.25,
    "G1": 49.00,
    "G#1/Ab1": 51.91,
    "A1": 55.00,
    "A#1/Bb1": 58.27,
    "B1": 61.74,
    "C2": 65.41,
    "C#2/Db2": 69.30,
    "D2": 73.42,
    "D#2/Eb2": 77.78,
    "E2": 82.41,
    "F2": 87.31,
    "F#2/Gb2": 92.50,
    "G2": 98.00,
    "G#2/Ab2": 103.83,
    "A2": 110.00,
    "A#2/Bb2": 116.54,
    "B2": 123.47,
    "C3": 130.81,
    "C#3/Db3": 138.59,
    "D3": 146.83,
    "D#3/Eb3": 155.56,
    "E3": 164.81,
    "F3": 174.61,
    "F#3/Gb3": 185.00,
    "G3": 196.00,
    "G#3/Ab3": 207.65,
    "A3": 220.00,
    "A#3/Bb3": 233.08,
    "B3": 246.94,
    "C4": 261.63,
    "C#4/Db4": 277.18,
    "D4": 293.66,
    "D#4/Eb4": 311.13,
    "E4": 329.63,
    "F4": 349.23,
    "F#4/Gb4": 369.99,
    "G4": 392.00,
    "G#4/Ab4": 415.30,
    "A4": 440.00,
    "A#4/Bb4": 466.16,
    "B4": 493.88,
    "C5": 523.25,
    "C#5/Db5": 554.37,
    "D5": 587.33,
    "D#5/Eb5": 622.25,
    "E5": 659.25,
    "F5": 698.46,
    "F#5/Gb5": 739.99,
    "G5": 783.99,
    "G#5/Ab5": 830.61,
    "A5": 880.00,
    "A#5/Bb5": 932.33,
    "B5": 987.77,
    "C6": 1046.50,
    "C#6/Db6": 1108.73,
    "D6": 1174.66,
    "D#6/Eb6": 1244.51,
    "E6": 1318.51,
    "F6": 1396.91,
    "F#6/Gb6": 1479.98,
    "G6": 1567.98,
    "G#6/Ab6": 1661.22,
    "A6": 1760.00,
    "A#6/Bb6": 1864.66,
    "B6": 1975.53,
    "C7": 2093.00,
    "C#7/Db7": 2217.46,
    "D7": 2349.32,
    "D#7/Eb7": 2489.02,
    "E7": 2637.02,
    "F7": 2793.83,
    "F#7/Gb7": 2959.96,
    "G7": 3135.96,
    "G#7/Ab7": 3322.44,
    "A7": 3520.00,
    "A#7/Bb7": 3729.31,
    "B7": 3951.07,
    "C8": 4186.01,
    "C#8/Db8": 4434.92,
    "D8": 4698.63,
    "D#8/Eb8": 4978.03,
    "E8": 5274.04,
    "F8": 5587.65,
    "F#8/Gb8": 5919.91,
    "G8": 6271.93,
    "G#8/Ab8": 6644.88,
    "A8": 7040.00,
    "A#8/Bb8": 7458.62,
    "B8": 7902.13,
    "C9": 8372.02,
    "C#9/Db9": 8869.84,
    "D9": 9397.27,
    "D#9/Eb9": 9956.06,
    "E9": 10548.08,
    "F9": 11175.30,
    "F#9/Gb9": 11839.82,
    "G9": 12543.85,
    "G#9/Ab9": 13289.75,
    "A9": 14080.00,
    "A#9/Bb9": 14917.24,
    "B9": 15804.26,
}


# gpt prompt-response
def query(theme):
    # create a prompt that can be fed to chatgpt to produce instructions personalized by theme
    prompt = "Create a song by outputting a list of notes. This song should fit the theme: happy. Output the song in one line strictly, and insert a dash with the time in seconds the note should be afterwards. Make sure there is variance in the times for added complexity. For an example format (the song should be much longer than this): C0-1 E1-4 G#0-2 A1-2 After this, generate 2 more lists like this to harmonize perfectly with the first generated notes. The same rules apply."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]


def process(file, instructions):
    # determine starting pitch
    audio_file = file
    y, sr = librosa.load(audio_file, sr=None)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch = np.mean(pitches)
    # process instructions
    allnotes = instructions.split(" ")
    instructnotes = []
    instructlength = []
    for note in allnotes:
        instructnotes = note.split("-")[0]
        instructlength = note.split("-")[1]
    # for each instruction, change note pitch and/or length
    song = []
    for i in range(len(instructnotes)):
        song.append(change_note_pitch(change_note_len(audio_file)))
    # compile all the new notes into a SONG
    return combine_notes(song)


def combine_notes(song):
    # given a list of music files, concatenate together
    # load first audio file to add everything to
    audio, sr = librosa.load(song[0], sr=None)
    # loop and append everything else
    for file in song[1:]:
        thispart, _ = librosa.load(file, sr=None)
        audio = np.concatenate((audio, thispart))
    return audio


def change_note_pitch(file, y, sr, original, note):
    # determine target and original frequencies
    target_freq = notes[note]
    original_freq = original
    # change it into number of steps needed to shift pitch
    n_steps = 12 * math.log2(target_freq / original_freq)
    # generate new pitches by pitch shifting
    y_pitch_shifted = librosa.effects.pitch_shift(y, sr, n_steps=n_steps)

    # create new audio with the new pitches

    # return the audio
    return


def change_note_len(file, len):
    return


def test():
    # Load the pre-trained model
    bundle_path = "path/to/melody_rnn.mag"
    bundle = sequence_generator_bundle.read_bundle_file(bundle_path)
    generator_map = melody_rnn_sequence_generator.get_generator_map()
    generator = generator_map["melody_rnn"](checkpoint=None, bundle=bundle)

    # Set the desired generation parameters
    temperature = 1.0  # Controls the randomness of the generated output
    num_steps = 128  # Length of the generated sequence in steps (16 steps per bar)
    min_duration = 0.25  # Minimum duration for a note in beats
    max_duration = 2.0  # Maximum duration for a note in beats
    quantization_steps = 4  # Number of steps per quarter note

    # Generate a melody
    input_sequence = mm.Melody()
    input_sequence.from_event_list([(60, 100, 1.0)])  # Start with a C4 note
    generate_args = (
        melody_rnn_sequence_generator.MelodyRnnSequenceGenerator.generate_args(
            num_steps, temperature
        )
    )
    generated_sequence = generator.generate(input_sequence, generate_args)

    # Extract the notes from the generated sequence with quantized timings
    notes = []
    current_step = 0
    for note in generated_sequence.notes:
        if note.is_drum:  # Skip drum notes
            continue
        pitch = mm.constants.MIDI_NOTE_NUMBER_TO_PITCH_NAME[note.pitch]
        duration = random.uniform(min_duration, max_duration)
        quantized_start_step = mm.quantize_to_step(note.start_time, quantization_steps)
        quantized_end_step = mm.quantize_to_step(note.end_time, quantization_steps)
        start_time = quantized_start_step * (4.0 / quantization_steps)
        end_time = quantized_end_step * (4.0 / quantization_steps)
        notes.append((pitch, start_time, end_time))
        current_step += note.quantized_end_step - note.quantized_start_step

    # Print the generated notes
    for note in notes:
        print(note)
