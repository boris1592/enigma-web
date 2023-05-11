from random import sample, randint
from dataclasses import asdict, dataclass
from yaml import safe_load, dump
from dacite import from_dict
from base64 import b64decode, b64encode


def random_pairs(data):
    data = sample(data, len(data))
    return [f'{data[i]}{data[i + 1]}' for i in range(0, len(data) - 1, 2)]


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


@dataclass
class EnigmaConfig:
    rotors: list[str]
    reflector: str
    plugs: list[str]
    positions: list[int]
    alphabet: str

    def validate(self):
        alphabet_len = len(self.alphabet)

        assert alphabet_len % 2 == 0, 'Alphabet length should be even'

        assert (
            len(set(self.alphabet)) == alphabet_len
        ), 'Alphabet should contain each letter only once'

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

    def dump_yaml(self):
        return dump(asdict(self))

    @staticmethod
    def load_yaml(yaml):
        data = safe_load(yaml)
        return from_dict(data_class=EnigmaConfig, data=data)

    def encode(self):
        return b64encode(self.dump_yaml().encode()).decode().replace('/', '-')

    @staticmethod
    def decode(string):
        return EnigmaConfig.load_yaml(
            b64decode(string.replace('-', '/')).decode()
        )

    # Templates crap
    def get_positions(self):
        return ' '.join(map(str, self.positions))
