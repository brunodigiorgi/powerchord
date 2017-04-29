import powerchord


def test_nochord():
    chord = 'N'
    c = powerchord.chord_regex.parse_chord(chord)
    assert(c.is_nochord is True)


def test_chord_to_pitch_classes_rep():
    chord = 'G#:maj'
    cpc = powerchord.chord_regex.chord_to_pitch_classes_repr(chord)
    assert(cpc.is_nochord is False)
    assert(cpc.bass is None)
    assert(cpc.root is 8)
    assert(set(cpc.pitch_classes) == {3, 0, 8})


def test_chord_types():
    chords = ['A:maj(7)/2', 'A:(1, 4, *5)/4', 'A/3', 'N']
    for c in chords:
        powerchord.chord_regex.parse_chord(c)
        powerchord.chord_regex.chord_to_pitch_classes_repr(c)


def test_chords_set():
    import json
    chords = json.load(open('./chords_set.json', 'r'))
    for c in chords:
        powerchord.chord_regex.parse_chord(c)
        cpc = powerchord.chord_regex.chord_to_pitch_classes_repr(c)
        print(c, cpc)