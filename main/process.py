import librosa
import numpy as np
import soundfile as sf


def process(file, instructions):
    # determine starting pitch
    audio_file = file
    y, sr = librosa.load(audio_file, sr=None)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch = np.mean(pitches)
    # process instructions

    # for each instruction, change note pitch and/or length

    # compile all the new notes into a SONG
    return


def change_note_pitch(file, note):
    return


def change_note_len(file, len):
    return
