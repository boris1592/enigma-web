from emulator.config import EnigmaConfig


def pairs_to_dict(pairs):
    answer = {}

    for pair in pairs:
        answer[pair[0]] = pair[1]
        answer[pair[1]] = pair[0]

    return answer


class Rotor:
    def __init__(self, pos, alphabet, permutation):
        self.pos = pos
        self.__alphabet = alphabet
        self.__permutation = permutation

    # The hardest part of the emulation
    def pass_through(self, letter, reverse):
        # Shift the letter
        index = (self.__alphabet.find(letter) - self.pos) % len(
            self.__alphabet
        )
        letter = self.__alphabet[index]

        # Do the permutation
        source = self.__alphabet if not reverse else self.__permutation
        dest = self.__alphabet if reverse else self.__permutation

        index = source.find(letter)
        letter = dest[index]

        # Shift the letter back
        index = (self.__alphabet.find(letter) + self.pos) % len(
            self.__alphabet
        )
        letter = self.__alphabet[index]

        return letter


class EnigmaEmulator:
    def __init__(self, config: EnigmaConfig):
        config.validate()

        self.__alphabet = config.alphabet
        self.__rotors = [
            Rotor(config.positions[i], config.alphabet, rotor)
            for i, rotor in enumerate(config.rotors)
        ]
        self.__reflector = pairs_to_dict(config.reflector)
        self.__plugs = pairs_to_dict(
            [(letter, letter) for letter in config.alphabet] + config.plugs
        )

    def __rotate_rotors(self):
        self.__rotors[0].pos += 1

        for i in range(0, len(self.__rotors)):
            if self.__rotors[i].pos < len(self.__alphabet):
                break

            self.__rotors[i].pos %= len(self.__alphabet)

            if i < len(self.__rotors) - 1:
                self.__rotors[i + 1].pos += 1

    def __pass_through_rotors(self, letter):
        for rotor in self.__rotors:
            letter = rotor.pass_through(letter, False)

        letter = self.__reflector[letter]

        for rotor in self.__rotors[::-1]:
            letter = rotor.pass_through(letter, True)

        return letter

    def __press_key(self, letter):
        self.__rotate_rotors()
        letter = self.__plugs[letter]
        letter = self.__pass_through_rotors(letter)
        letter = self.__plugs[letter]
        return letter

    def process(self, text):
        encrypted = ''.join(map(lambda letter: self.__press_key(letter), text))
        return encrypted
