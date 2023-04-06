from string import ascii_uppercase


class EnigmaEmulator:
    def __init__(
        self,
        rotors: list[str],
        reflector: str,
        plugs: list[tuple[str, str]],
        positions: list[int],
        alphabet=ascii_uppercase,
    ):
        self.__alphabet = alphabet
        self.__positions = positions
        self.__reflector = {
            letter: reflector[i] for i, letter in enumerate(alphabet)
        }
        self.__rotors = list(
            map(
                lambda rotor: {
                    letter: rotor[i] for i, letter in enumerate(alphabet)
                },
                rotors,
            )
        )
        self.__plugs = {}

        for letter in alphabet:
            plug = next((p for p in plugs if letter in p), None)
            self.__plugs[letter] = (
                letter
                if plug is None
                else plug[0]
                if letter == plug[1]
                else plug[1]
            )

    def __rotate_rotors(self):
        self.__positions[0] += 1

        for i in range(0, len(self.__positions)):
            if self.__positions[i] < len(self.__alphabet):
                break

            self.__positions[i] %= len(self.__alphabet)

            if i < len(self.__positions) - 1:
                self.__positions[i + 1] += 1

    def __pass_through_rotors(self, letter):
        for rotor in self.__rotors:
            letter = rotor[letter]

        letter = self.__reflector[letter]

        for rotor in self.__rotors[::-1]:
            letter = rotor[letter]

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
