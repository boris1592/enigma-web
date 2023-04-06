from string import ascii_uppercase


def pairs_to_dict(pairs):
    answer = {}

    for pair in pairs:
        answer[pair[0]] = pair[1]
        answer[pair[1]] = pair[0]

    return answer


class EnigmaEmulator:
    def __init__(
        self,
        rotors: list[str],
        reflector: list[str],
        plugs: list[str],
        positions: list[int],
        alphabet=ascii_uppercase,
    ):
        self.__alphabet = alphabet
        self.__positions = positions
        self.__rotors = [pairs_to_dict(rotor) for rotor in rotors]
        self.__reflector = pairs_to_dict(reflector)
        self.__plugs = pairs_to_dict(
            [(letter, letter) for letter in alphabet] + plugs
        )

    def __rotate_rotors(self):
        self.__positions[0] += 1

        for i in range(0, len(self.__positions)):
            if self.__positions[i] < len(self.__alphabet):
                break

            self.__positions[i] %= len(self.__alphabet)

            if i < len(self.__positions) - 1:
                self.__positions[i + 1] += 1

    def __pass_through_rotor(self, rotor_index, letter):
        letter_index = (
            self.__alphabet.find(letter) + self.__positions[rotor_index]
        ) % len(self.__alphabet)
        return self.__rotors[rotor_index][self.__alphabet[letter_index]]

    def __pass_through_rotors(self, letter):
        for i in range(len(self.__rotors)):
            letter = self.__pass_through_rotor(i, letter)

        letter = self.__reflector[letter]

        for i in range(len(self.__rotors) - 1, -1, -1):
            letter = self.__pass_through_rotor(i, letter)

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
