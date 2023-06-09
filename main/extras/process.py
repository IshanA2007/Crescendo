import librosa
import numpy as np
import soundfile as sf
import openai
import math
import os
from dotenv import dotenv_values

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# figure out how to make this so not everyone can see my api key
env_vars = dotenv_values(".env")
openai.api_key = env_vars["api_key"]
notes = {
    "C0": 16.35,
    "C#0": 17.32,
    "Db0": 17.32,
    "D0": 18.35,
    "D#0": 19.45,
    "Eb0": 19.45,
    "E0": 20.60,
    "F0": 21.83,
    "F#0": 23.12,
    "Gb0": 23.12,
    "G0": 24.50,
    "G#0": 25.96,
    "Ab0": 25.96,
    "A0": 27.50,
    "A#0": 29.14,
    "Bb0": 29.14,
    "B0": 30.87,
    "C1": 32.70,
    "C#1": 34.65,
    "Db1": 34.65,
    "D1": 36.71,
    "D#1": 38.89,
    "Eb1": 38.89,
    "E1": 41.20,
    "F1": 43.65,
    "F#1": 46.25,
    "Gb1": 46.25,
    "G1": 49.00,
    "G#1": 51.91,
    "Ab1": 51.91,
    "A1": 55.00,
    "A#1": 58.27,
    "Bb1": 58.27,
    "B1": 61.74,
    "C2": 65.41,
    "C#2": 69.30,
    "Db2": 69.30,
    "D2": 73.42,
    "D#2": 77.78,
    "Eb2": 77.78,
    "E2": 82.41,
    "F2": 87.31,
    "F#2": 92.50,
    "Gb2": 92.50,
    "G2": 98.00,
    "G#2": 103.83,
    "Ab2": 103.83,
    "A2": 110.00,
    "A#2": 116.54,
    "Bb2": 116.54,
    "B2": 123.47,
    "C3": 130.81,
    "C#3": 138.59,
    "Db3": 138.59,
    "D3": 146.83,
    "D#3": 155.56,
    "Eb3": 155.56,
    "E3": 164.81,
    "F3": 174.61,
    "F#3": 185.00,
    "Gb3": 185.00,
    "G3": 196.00,
    "G#3": 207.65,
    "Ab3": 207.65,
    "A3": 220.00,
    "A#3": 233.08,
    "Bb3": 233.08,
    "B3": 246.94,
    "C4": 261.63,
    "C#4": 277.18,
    "Db4": 277.18,
    "D4": 293.66,
    "D#4": 311.13,
    "Eb4": 311.13,
    "E4": 329.63,
    "F4": 349.23,
    "F#4": 369.99,
    "Gb4": 369.99,
    "G4": 392.00,
    "G#4": 415.30,
    "Ab4": 415.30,
    "A4": 440.00,
    "A#4": 466.16,
    "Bb4": 466.16,
    "B4": 493.88,
    "C5": 523.25,
    "C#5": 554.37,
    "Db5": 554.37,
    "D5": 587.33,
    "D#5": 622.25,
    "Eb5": 622.25,
    "E5": 659.25,
    "F5": 698.46,
    "F#5": 739.99,
    "Gb5": 739.99,
    "G5": 783.99,
    "G#5": 830.61,
    "Ab5": 830.61,
    "A5": 880.00,
    "A#5": 932.33,
    "Bb5": 932.33,
    "B5": 987.77,
    "C6": 1046.50,
    "C#6": 1108.73,
    "Db6": 1108.73,
    "D6": 1174.66,
    "D#6": 1244.51,
    "Eb6": 1244.51,
    "E6": 1318.51,
    "F6": 1396.91,
    "F#6": 1479.98,
    "Gb6": 1479.98,
    "G6": 1567.98,
    "G#6": 1661.22,
    "Ab6": 1661.22,
    "A6": 1760.00,
    "A#6": 1864.66,
    "Bb6": 1864.66,
    "B6": 1975.53,
    "C7": 2093.00,
    "C#7": 2217.46,
    "Db7": 2217.46,
    "D7": 2349.32,
    "D#7": 2489.02,
    "Eb7": 2489.02,
    "E7": 2637.02,
    "F7": 2793.83,
    "F#7": 2959.96,
    "Gb7": 2959.96,
    "G7": 3135.96,
    "G#7": 3322.44,
    "Ab7": 3322.44,
    "A7": 3520.00,
    "A#7": 3729.31,
    "Bb7": 3729.31,
    "B7": 3951.07,
    "C8": 4186.01,
    "C#8": 4434.92,
    "Db8": 4434.92,
    "D8": 4698.63,
    "D#8": 4978.03,
    "Eb8": 4978.03,
    "E8": 5274.04,
    "F8": 5587.65,
    "F#8": 5919.91,
    "Gb8": 5919.91,
    "G8": 6271.93,
    "G#8": 6644.88,
    "Ab8": 6644.88,
    "A8": 7040.00,
    "A#8": 7458.62,
    "Bb8": 7458.62,
    "B8": 7902.13,
    "C9": 8372.02,
    "C#9": 8869.84,
    "Db9": 8869.84,
    "D9": 9397.27,
    "D#9": 9956.06,
    "Eb9": 9956.06,
    "E9": 10548.08,
    "F9": 11175.30,
    "F#9": 11839.82,
    "Gb9": 11839.82,
    "G9": 12543.85,
    "G#9": 13289.75,
    "Ab9": 13289.75,
    "A9": 14080.00,
    "A#9": 14917.24,
    "Bb9": 14917.24,
    "B9": 15804.26,
}


# gpt prompt-response
def query(theme):
    # create a prompt that can be fed to chatgpt to produce instructions personalized by theme
    prompt = f"""Create a song by outputting a list of notes. This song should fit the theme: {theme}. Output the song in one line strictly, and insert a dash with the time in seconds the note should be afterwards. Make sure there is variance in the times for added complexity. For an example format (the song should be much longer than this): C0-1 E1-4 G#0-2 A1-2

    After this, generate 2 more lists like this to harmonize perfectly with the first generated notes. Each line must last the same number of seconds. Here are the notes you can use:
    {notes.keys()}
    The same rules apply. Output these lines directly below the first line, and NOTHING ELSE. Your output should not look like:
    ---
    Here's a song with a list of notes:

    C4-1 E4-2 G4-1 E4-1 C4-1 E4-2 G4-1 E4-1 C4-1 E4-1 C4-1 G3-2 A3-1 G3-1 C4-1 E4-2 G4-1 E4-1 C4-1 E4-2 G4-1 E4-1 C4-1 E4-1 C4-1 G3-2 A3-1 G3-1

    And here are two harmonized lines that fit perfectly with the first line:

    E4-1 G4-2 B4-1 G4-1 E4-1 G4-2 B4-1 G4-1 E4-1 G4-1 E4-1 E4-1 B3-2 C4-1 B3-1 E4-1 G4-2 B4-1 G4-1 E4-1 G4-2 B4-1 G4-1 E4-1 G4-1 E4-1 B3-2 C4-1 B3-1

    G3-1 B3-2 D4-1 B3-1 G3-1 B3-2 D4-1 B3-1 G3-1 B3-1 G3-1 G3-1 D3-2 E3-1 D3-1 G3-1 B3-2 D4-1 B3-1 G3-1 B3-2 D4-1 B3-1 G3-1 B3-1 G3-1 G3-1 D3-2 E3-1 D3-1

    I hope you enjoy this harmonious song!
    ---
    It should instead look like:
    C4-1 E4-2 G4-1 E4-1 C4-1 E4-2 G4-1 E4-1 C4-1 E4-1 C4-1 G3-2 A3-1 G3-1 C4-1 E4-2 G4-1 E4-1 C4-1 E4-2 G4-1 E4-1 C4-1 E4-1 C4-1 G3-2 A3-1 G3-1
    E4-1 G4-2 B4-1 G4-1 E4-1 G4-2 B4-1 G4-1 E4-1 G4-1 E4-1 E4-1 B3-2 C4-1 B3-1 E4-1 G4-2 B4-1 G4-1 E4-1 G4-2 B4-1 G4-1 E4-1 G4-1 E4-1 B3-2 C4-1 B3-1
    G3-1 B3-2 D4-1 B3-1 G3-1 B3-2 D4-1 B3-1 G3-1 B3-1 G3-1 G3-1 D3-2 E3-1 D3-1 G3-1 B3-2 D4-1 B3-1 G3-1 B3-2 D4-1 B3-1 G3-1 B3-1 G3-1 G3-1 D3-2 E3-1 D3-1"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    print(response["choices"][0]["message"]["content"])
    return response["choices"][0]["message"]["content"]


def process(file, instructions):
    songdata = []
    harmonizeIndex = 0
    for line in instructions.split("\n"):
        # store this part of the song
        harmonizeIndex += 1
        thispart = BASE_DIR + f"/extras/audios/part{harmonizeIndex}.wav"
        songdata.append(thispart)
        # determine starting pitch
        audio_file = file
        y, sr = librosa.load(audio_file, sr=None)
        y, _ = librosa.effects.trim(y)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch = np.mean(pitches)
        # process instructions
        allnotes = line.split(" ")
        instructions = process_instructions([], [], allnotes)
        instructnotes = instructions[0]
        instructlength = instructions[1]
        # for each instruction, change note pitch and/or length
        song = []
        create_song(instructnotes, instructlength, thispart, y, sr, pitch)

    finalfile = BASE_DIR + "/extras/audios/final.wav"
    harmonize(songdata, finalfile)  # these need to layer on top of each other
    return finalfile


def harmonize(harmonies, filename):
    # given a list of music files, layer on top of each other
    y, sr = librosa.load(harmonies[0], sr=None)
    common_sr = 44100  # just in case the files are different
    y = librosa.resample(y, orig_sr=sr, target_sr=common_sr)
    mix = y
    for i in range(1, len(harmonies)):
        y, sr = librosa.load(harmonies[i], sr=None)
        y = librosa.resample(y, orig_sr=sr, target_sr=common_sr)
        # pad the shorter array
        if len(mix) < len(y):
            mix = np.pad(mix, (0, len(y) - len(mix)))
        elif len(y) < len(mix):
            y = np.pad(y, (0, len(mix) - len(y)))

        mix = np.add(mix, y)
    mix = librosa.util.normalize(
        mix
    )  # we don't want a value over 1 or things will break
    sf.write(filename, mix, common_sr)


def combine_notes(song, filename):
    # given a list of music files, combine one after the other
    # load first audio file to add everything to
    audio, sr = librosa.load(song[0], sr=None)
    # loop and append everything else
    for file in song[1:]:
        thispart, _ = librosa.load(file, sr=None)
        audio = np.concatenate((audio, thispart))
    sf.write(filename, audio, sr)


def change_note_pitch(file, original, note):
    y, sr = librosa.load(file)
    # determine target and original frequencies
    target_freq = notes[note]
    original_freq = original
    # change it into number of steps needed to shift pitch
    n_steps = 12 * math.log2(target_freq / original_freq)
    # generate new pitches by pitch shifting
    y_pitch_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)
    # create new audio with the new pitches
    sf.write(file, y_pitch_shifted, sr)
    # return the audio
    return file


def change_note_len(file, length):
    y, sr = librosa.load(file)

    # figure out how much to stretch/squish by
    original_length = librosa.get_duration(y=y, sr=sr)
    stretch_factor = original_length / length

    # apply change
    length_adj_file = librosa.effects.time_stretch(y, rate=stretch_factor)

    # save to new file
    sf.write(file, length_adj_file, sr)
    return file


def process_instructions(instructnotes, instructlength, allnotes):
    for note in allnotes:
        if len(note.split("-")) != 2:
            print("uhhhhh")
            continue
        if note.split("-")[0] in notes:
            instructnotes.append(note.split("-")[0])
            try:
                instructlength.append(float(note.split("-")[1]))
            except:  # in case a period was added at the end, for example, "A1-1."
                instructlength.append(float(note.split("-")[1][0]))
        else:
            print("oh no")

    return instructnotes, instructlength


def create_song(instructnotes, instructlength, thispart, y, sr, pitch):
    for i in range(len(instructnotes)):
        print(i)
        tempfile = BASE_DIR + "/extras/audios/temp.wav"
        sf.write(tempfile, y, sr)
        # change length
        change_note_len(tempfile, instructlength[i])
        # change pitch
        change_note_pitch(tempfile, pitch, instructnotes[i])
        # append temp to final
        if i == 0:
            combine_notes([tempfile], thispart)
        else:
            combine_notes([thispart, tempfile], thispart)
        # pseudo for new process
        # for each instruction, change note length of original, save to another audio file (temp)
        # then feed this temp audio file into the change pitch and overwrite temp
        # then combine temp to a final audio file which is returned at the end
        # repeat by overriding temp (this method uses only 3 files instead of having a bunch created)
