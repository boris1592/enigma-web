from emulator_config import EnigmaConfig
from emulator import EnigmaEmulator


class EnigmaEmulatorsFactory:
    def __init__(self, config: EnigmaConfig):
        self.__config = config

    def new_emulator(self):
        return EnigmaEmulator(self.__config)
