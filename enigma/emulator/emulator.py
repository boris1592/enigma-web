from emulator.config import EnigmaConfig


def pairs_to_dict(pairs):
    answer = {}

    for pair in pairs:
        answer[pair[0]] = pair[1]
        answer[pair[1]] = pair[0]

    return answer


class Rotor:
    def __init__(self, pos, str1, str2):
        self.pos = pos
        self.__str1 = str1
        self.__str2 = str2
        self.__normal_dict = {str1[i]: str2[i] for i in range(len(str1))}
        self.__reverse_dict = {str2[i]: str1[i] for i in range(len(str2))}

    def pass_through(self, letter, reverse):
        source = self.__str1 if not reverse else self.__str2
        index = (
            source.find(letter) + (self.pos if not reverse else -self.pos)
        ) % len(source)
        cycled = source[index]
        return (
            self.__normal_dict[cycled]
            if not reverse
            else self.__reverse_dict[cycled]
        )


class EnigmaEmulator:
    def __init__(self, config: EnigmaConfig):
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
        encrypted = ''.join(map(lambda l: self.__press_key(l), text))
        return encrypted
