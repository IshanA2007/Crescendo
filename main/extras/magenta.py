from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
from magenta.music import DEFAULT_QUARTERS_PER_MINUTE
from magenta.protobuf import generator_pb2
from magenta.protobuf import music_pb2


def generate_notes(mood):
    # Load the melody RNN model bundle
    bundle = sequence_generator_bundle.read_bundle_file("path/to/melody_rnn.mag")

    # Initialize the melody RNN sequence generator
    generator_map = melody_rnn_sequence_generator.get_generator_map()
    melody_rnn = generator_map["melody_rnn"](checkpoint=None, bundle=bundle)

    # Set the generator options based on mood and instrument
    generator_options = generator_pb2.GeneratorOptions()
    generator_options.args["temperature"].float_value = 1.0

    if mood == "happy":
        # Set the mood-specific tempo and chord progression
        tempo = DEFAULT_QUARTERS_PER_MINUTE
        chord_progression = ["C", "G", "Am", "F"]

    elif mood == "sad":
        # Set the mood-specific tempo and chord progression
        tempo = DEFAULT_QUARTERS_PER_MINUTE / 2
        chord_progression = ["Am", "Em", "F", "C"]

    else:
        return None

    # Create a MusicSequence for each instrument
    instruments = ["guitar", "piano", "drums", "trumpet", "bass"]
    notes_with_durations = {}

    for instrument in instruments:
        # Generate melody with Magenta
        melody = music_pb2.Melody()
        melody.from_sequence(generator_options, melody_rnn, chord_progression, tempo)

        # Convert melody to note names and durations
        notes = []
        durations = []

        for note in melody.notes:
            notes.append(note.pitch_name)
            durations.append(note.end_time - note.start_time)

        # Store the notes and durations for the instrument
        notes_with_durations[instrument] = list(zip(notes, durations))

    return notes_with_durations
