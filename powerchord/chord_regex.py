"""
[1] Harte, Christopher, et al. "Symbolic Representation of Musical Chords: A Proposed Syntax for Text Annotations." ISMIR. Vol. 5. 2005.
"""
import re
from collections import namedtuple
import itertools


def opt(x):  # optional
    return x + r'?'


def noncg(x):  # noncapturing group
    return r'(?:' + x + r')'


# chord regex:
rg_natural = r'[A-G]'
rg_modifier = r'#*b*'
rg_interval = r'1|2|3|4|5|6|7|8|9|10|11|12|13'
rg_note = noncg(rg_natural + rg_modifier)
rg_degree = noncg(rg_modifier + noncg(rg_interval))
opt_deg = r'\*?'  # optional modifier for omitting a degree
rg_degree_list = r'(?P<degree_list>\((?:' + opt_deg + rg_degree + r', ?)*' + opt_deg + rg_degree + r'\))'
rg_shorthand = '(?P<shorthand>maj|min|dim|aug|maj7|min7|7|dim7|hdim7|minmaj7|maj6|min6|9|maj9|min9|sus4)'
rg_root = r'(?P<root>' + rg_note + r')'
rg_bass = r'(?:/(?P<bass>' + rg_degree + r'))'

NATURALS = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
INTERVALS = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11,
             8: 12, 9: 14, 10: 16, 11: 17, 12: 19, 13: 21}
SHORTHANDS = {'maj': [0, 4, 7],
              'min': [0, 3, 7],
              'dim': [0, 3, 6],
              'aug': [0, 4, 8],
              # sevenths
              'maj7': [0, 4, 7, 11],
              'min7': [0, 3, 7, 10],
              '7': [0, 4, 7, 10],
              'dim7': [0, 3, 6, 9],
              'hdim7': [0, 3, 6, 10],
              'minmaj7': [0, 3, 7, 11],
              # sixths
              'maj6': [0, 4, 7, 9],
              'min6': [0, 3, 7, 9],
              # ninth
              '9': [0, 4, 7, 10, 14],
              'maj9': [0, 4, 7, 11, 14],
              'min9': [0, 3, 7, 10, 14],
              # sus
              'sus4': [0, 5, 7],
              'sus2': [0, 2, 7],
              }


def degree_to_semitones(x):
    if x is None:
        return None
    interval_std = x.replace('b', '').replace('#', '')
    return INTERVALS[int(interval_std)] + x.count('#') - x.count('b')


def degree_list_to_semitones_list(x):
    if x is None:
        return []
    return [degree_to_semitones(x_) for x_ in x]


def note_to_pitchclass(x):
    if x is None:
        return None
    x_nat = x.replace('b', '').replace('#', '')
    x = NATURALS[x_nat] + x.count('#') - x.count('b')
    x = x % 12
    return x


def shorthand_to_semitones_list(x):
    if x is None:
        return []
    return SHORTHANDS[x]


chord1 = rg_root + r':' + rg_shorthand + opt(rg_degree_list) + opt(rg_bass)
chord2 = rg_root + r':' + rg_degree_list + opt(rg_bass)
chord3 = rg_root + opt(rg_bass)
chord4 = r'N'
chord = [chord1, chord2, chord3, chord4]


def match(in_str, pattern):
    s = in_str.lstrip(' ').rstrip(' ')
    m = re.fullmatch(pattern, s)
    return m


def is_match(in_str, pattern):
    return match(in_str, pattern) is not None


def is_chord(in_str):
    for c in chord:
        if is_match(in_str, c):
            return True
    return False


def chord_pattern(in_str):
    for c in chord:
        if is_match(in_str, c):
            return c
    raise ValueError('input is not recognized as a valid chord')


def chord_match(in_str):
    for c in chord:
        m = match(in_str, c)
        if m is not None:
            return m
    raise ValueError('input is not recognized as a valid chord')


def is_note(in_str):
    return is_match(in_str, rg_note)


def is_degree(in_str):
    return is_match(in_str, rg_degree)


def is_shorthand(in_str):
    return is_match(in_str, rg_shorthand)


def parse_degree_list(in_str):
    # parse the optional omit modifier and return (include_list, omit_list) with degree labels

    if in_str is None:
        return [], []
    in_str = in_str.replace('(', '').replace(')', '')
    dl = re.split(r' ?,', in_str)
    include_list = []
    omit_list = []
    for d in dl:
        if '*' in d:
            omit_list.append(d.replace('*', '').lstrip(' ').rstrip(' '))
        else:
            include_list.append(d.lstrip(' ').rstrip(' '))
    return include_list, omit_list


ParsedChordLabel = namedtuple('ParsedChordLabel',
                              ['root',
                               'shorthand',
                               'degree_list_include',
                               'degree_list_omit',
                               'bass',
                               'is_nochord'])


def parse_chord(in_str):
    """
    Parse a chord label and returns its structure in terms of sub labels
    All the returned fields are string or lists of strings
    
    :param in_str: chord label
    :return: ParsedChordLabel
        attributes: root, shorthand, degree_list_include, degree_list_omit, bass, is_nochord
    """
    m = chord_match(in_str)
    mdict = m.groupdict()
    root_l = mdict.get('root', None)
    shorthand_l = mdict.get('shorthand', None)
    di, do = parse_degree_list(mdict.get('degree_list', None))
    degree_list_include = di
    degree_list_omit = do
    bass_l = mdict.get('bass', None)

    is_nochord = False
    if root_l is None:
        is_nochord = True

    return ParsedChordLabel(root_l, shorthand_l,
                            degree_list_include, degree_list_omit,
                            bass_l, is_nochord)


ChordPitchClassStruct = namedtuple('ChordPitchClassStruct',
                                   ['root',
                                    'bass',
                                    'pitch_classes',
                                    'is_nochord'])


def chord_to_pitch_classes_repr(in_str):
    """
    Parse a chord label and returns its structure in terms of pitch classes
    
    :param in_str: chord label 
    :return: ChordPitchStruct
      contains the pitch classes of root, bass
      a field pitch_class, including all pitch classes in the chord (including root and bass)
      a bool is_nochord for 'N'
    """
    c = parse_chord(in_str)
    if c.is_nochord:
        return ChordPitchClassStruct(None, None, [], True)

    root_pc = note_to_pitchclass(c.root)
    st_sht = shorthand_to_semitones_list(c.shorthand)
    st_list_include = degree_list_to_semitones_list(c.degree_list_include)
    st_list_omit = degree_list_to_semitones_list(c.degree_list_omit)
    st_bass = degree_to_semitones(c.bass)

    bass_pc = None
    if st_bass is not None:
        bass_pc = (root_pc + st_bass) % 12

    pitch_classes = {root_pc}
    for i in itertools.chain(st_sht, st_list_include, [st_bass]):
        if i is not None:
            pitch_classes.add((root_pc + i) % 12)

    for i in st_list_omit:
        pitch_classes.discard((root_pc + i) % 12)

    return ChordPitchClassStruct(root_pc, bass_pc, list(pitch_classes), False)
