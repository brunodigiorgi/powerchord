import importlib
from . import chord_regex as _cr

_cr = importlib.reload(_cr)

# More general syntax with NOTE TYPE / BASS, where BASS can be note or degree
re_chord2 = _cr.re_root + _cr.nm('type', r'.*?') + _cr.opt(r'/' + _cr.nm('bass', _cr.re_note + r'|' + _cr.re_degree))
re_chord3 = 'N'
re_chord_list = [re_chord2, re_chord3]


class ChordLabelExt:

    def __init__(self, label):
        m = _cr.chord_match(label, re_chord_list)
        mdict = m.groupdict()
        self.root = mdict.get('root', None)
        self.type = mdict.get('type', None)
        self.bass = mdict.get('bass', None)

    @property
    def label(self):
        if self.is_nochord:
            return 'N'
        out = self.root + self.type
        if self.bass is not None:
            out += '/' + self.bass
        return out

    @property
    def is_nochord(self):
        if self.root is None:
            return True
        return False

    def bass_to_degree(self):
        if (self.bass is not None) and _cr.is_note(self.bass):
            self.bass = _cr.interval_to_degree(self.root, self.bass)
        return self

    def map_type(self, types_map):
        self.type = types_map.get(self.type, self.type)
        return self

    def __repr__(self):
        out = '{root: ' + str(self.root) + ', '
        out += 'type: ' + str(self.type) + ', '
        out += 'bass: ' + str(self.bass) + '}'
        return out


def unique_types(labels):
    types = set()
    for l in labels:
        t = ChordLabelExt(l).type
        types.add(t)
    return types


def bass_to_degree(labels):
    return [ChordLabelExt(l).bass_to_degree().label for l in labels]


def map_types(labels, types_map):
    return [ChordLabelExt(l).map_type(types_map).label for l in labels]
