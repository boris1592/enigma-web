from random import sample, randint


def random_pairs(data):
    data = sample(data, len(data))
    return [(data[i], data[i + 1]) for i in range(0, len(data) - 1, 2)]


def random_config(rotors_count, alphabet):
    rotors = [
        ''.join(sample(alphabet, len(alphabet))) for _ in range(rotors_count)
    ]
    reflector = random_pairs(alphabet)
    plugs = random_pairs(alphabet)
    positions = [randint(0, len(alphabet) - 1) for _ in range(rotors_count)]
    return EnigmaConfig(rotors, reflector, plugs, positions, alphabet)


class EnigmaConfig:
    def __init__(
        self,
        rotors: list[str],
        reflector: list[tuple[str, str]],
        plugs: list[tuple[str, str]],
        positions: list[int],
        alphabet,
    ):
        self.rotors = rotors
        self.reflector = reflector
        self.plugs = plugs
        self.positions = positions
        self.alphabet = alphabet

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

        letters_used = set()

        for l1, l2 in self.reflector:
            assert (
                l1 not in letters_used and l2 not in letters_used
            ), 'Reflector should contain each letter once'
            letters_used.add(l1)
            letters_used.add(l2)

        assert (
            len(letters_used) == alphabet_len
        ), 'Reflector should contain every letter from'

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
