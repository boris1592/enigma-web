from random import shuffle, randint, sample
from itertools import permutations


def random_pairs(data):
    result = []
    data = list(data)
    shuffle(data)

    for i in range(0, len(data), 2):
        if i + 1 >= len(data):
            break

        result.append((data[i], data[i + 1]))

    return result


def random_config(rotors_count, alphabet):
    # TODO : Replace with something a bit more efficient
    rotors = sample(
        list(map(lambda x: ''.join(x), permutations(alphabet))),
        rotors_count,
    )
    reflector = random_pairs(alphabet)
    plugs = random_pairs(alphabet)
    positions = [randint(0, len(alphabet)) for _ in range(rotors_count)]
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
        # TODO : Validate this crap
        self.rotors = rotors
        self.reflector = reflector
        self.plugs = plugs
        self.positions = positions
        self.alphabet = alphabet
