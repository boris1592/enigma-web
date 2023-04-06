from string import ascii_uppercase


class EnigmaConfig:
    def __init__(
        self,
        rotors: list[str],
        reflector: list[str],
        plugs: list[str],
        positions: list[int],
        alphabet=ascii_uppercase,
    ):
        # TODO : Validate this crap
        self.rotors = rotors
        self.reflector = reflector
        self.plugs = plugs
        self.positions = positions
        self.alphabet = alphabet
