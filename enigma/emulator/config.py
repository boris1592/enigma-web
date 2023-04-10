from random import sample, randint
from dataclasses import dataclass


def random_pairs(data):
    data = sample(data, len(data))
    return [(data[i], data[i + 1]) for i in range(0, len(data) - 1, 2)]


def random_config(rotors_count, alphabet):
    rotors = [
        ''.join(sample(alphabet, len(alphabet))) for _ in range(rotors_count)
    ]
    reflector_pairs = random_pairs(alphabet)
    reflector_map = {k: v for k, v in reflector_pairs} | {
        k: v for v, k in reflector_pairs
    }
    reflector = ''.join([reflector_map[letter] for letter in alphabet])
    plugs = random_pairs(alphabet)
    positions = [randint(0, len(alphabet) - 1) for _ in range(rotors_count)]
    return EnigmaConfig(rotors, reflector, plugs, positions, alphabet)


def encode_config(config):
    # rotor1,rotor2;reflector;plug1,plug2;positions;alphabet
    return ';'.join(
        [
            ','.join(config.rotors),
            config.reflector,
            ','.join([l1 + l2 for l1, l2 in config.plugs]),
            ','.join(map(str, config.positions)),
            config.alphabet,
        ]
    )


def decode_config(string):
    params = string.split(';')
    assert len(params) == 5, 'Params count should be 5'
    assert all(
        [p.isnumeric() for p in params[3].split(',')]
    ), 'Positions should be integers'

    return EnigmaConfig(
        params[0].split(','),
        params[1],
        [tuple(p) for p in params[2].split(',')],
        [int(p) for p in params[3].split(',')],
        params[4],
    )


@dataclass
class EnigmaConfig:
    rotors: list[str]
    reflector: str
    plugs: list[tuple[str, str]]
    positions: list[int]
    alphabet: str

    def validate(self):
        alphabet_len = len(self.alphabet)

        assert alphabet_len % 2 == 0, 'Alphabet length should be even'

        assert (
            len(set(self.alphabet)) == alphabet_len
        ), 'Alphabet shouldn contain each letter only once'

        for rotor in self.rotors:
            assert set(rotor) == set(
                self.alphabet
            ), 'Rotor should contain every letter'

        assert set(self.reflector) == set(
            self.alphabet
        ), 'Reflector should contain every letter'

        reflector_map = {}

        for i in range(alphabet_len):
            assert (
                self.reflector[i] not in reflector_map
                or reflector_map[self.reflector[i]] == self.alphabet[i]
            ), 'Reflector should be a product of independent transpositions'
            reflector_map[self.alphabet[i]] = self.reflector[i]

        letters_used = set()

        for l1, l2 in self.plugs:
            assert (
                l1 not in letters_used and l2 not in letters_used
            ), 'Plugs should contain each letter once'
            letters_used.add(l1)
            letters_used.add(l2)

        assert len(self.positions) == len(
            self.rotors
        ), 'Number of positions and rotors should be same'

        for pos in self.positions:
            assert (
                pos >= 0 and pos < alphabet_len
            ), 'Rotor position should be between zero and the alphabet length'
