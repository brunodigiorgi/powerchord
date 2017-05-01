power chord
-----------

A python library for parsing chord annotations from the format described in [1], based on a regular expressions.
Other utilities for chords that do not comply with the afore mentioned syntax are also provided.

[1] Harte, Christopher, et al. "Symbolic Representation of Musical Chords: A Proposed Syntax for Text Annotations." ISMIR. Vol. 5. 2005.

Installation
------------

	python3 setup.py install

Usage
-----

Syntactic split of the chord label:

    >>> chord_label = 'Abb:maj(7, *3)/b2'
    >>> c = powerchord.chord_regex.parse_chord(chord_label)
    >>>> print(c)
    ParsedChordLabel(root='Abb', shorthand='maj', degree_list_include=['7'], degree_list_omit=['3'], bass='b2', is_nochord=False)

Parse chord label to pitch class representation:

    >>> cpc = powerchord.chord_regex.chord_to_pitch_classes_repr(chord_label)
    >>> print(cpc)
    ChordPitchClassStruct(root=7, bass=8, pitch_classes=[8, 2, 6, 7], is_nochord=False)

Extended grammar, for chord labels that do not comply with [1].

    >>> unique_types = powerchord.unique_types(labels)
    >>> new_labels = powerchord.bass_to_degree(labels)
    >>> new_labels = powerchord.map_types(labels, types_map)

ParsedChordLabel and ChordPitchClassStruct are collections.namedtuple, therefore their attributes are available in autocompletion
