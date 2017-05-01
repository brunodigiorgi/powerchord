import powerchord


def test_unique_types_dataset():
    import json
    chords = json.load(open('./chords_set.json', 'r'))
    powerchord.extended_grammar.unique_types(chords)


def test_parse_chord_ext():
    label = 'ASTRANGE_TYPE/B'
    c = powerchord.extended_grammar.ChordLabelExt(label)
    assert(c.type == 'STRANGE_TYPE')


def test_unique_types():
    labels = ['N', 'A/B', 'Amin/b2', 'A#maj/C', 'A#augggg/8']
    types = powerchord.extended_grammar.unique_types(labels)
    assert(types == {None, '', 'min', 'maj', 'augggg'})


def test_bass_to_degree():
    labels = ['A/B', 'Amin/C', 'Amaj/C#', 'Amaj', 'A/b2']
    expected_results = ['A/2', 'Amin/b3', 'Amaj/3', 'Amaj', 'A/b2']
    new_labels = powerchord.extended_grammar.bass_to_degree(labels)
    for nl, er in zip(new_labels, expected_results):
        assert(nl == er)


def test_map_types():
    labels = ['N', 'A/B', 'Amin/C', 'Amaj/C#']
    types_map = {'': ':maj', 'min': ':min', 'maj': ':maj'}
    expected_results = ['N', 'A:maj/B', 'A:min/C', 'A:maj/C#']
    new_labels = powerchord.extended_grammar.map_types(labels, types_map)
    for nl, er in zip(new_labels, expected_results):
        assert (nl == er)
