from emulator_implementation import EnigmaEmulator
from emulator_config import EnigmaConfig


class EnigmaEmulatorsFactory:
    def __init__(self, config: EnigmaConfig):
        self.__config = config

    def new_emulator(self):
        return EnigmaEmulator(self.__config)
