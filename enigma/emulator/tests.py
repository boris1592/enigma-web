from django.test import TestCase
from .config import random_config
from .emulator import EnigmaEmulator
from random import sample
from string import ascii_uppercase


class EnigmaEmulationTests(TestCase):
    def test_emulation(self):
        for _ in range(10):
            config = random_config(5, ascii_uppercase)
            encrypter = EnigmaEmulator(config)
            decrypter = EnigmaEmulator(config)

            message = ''.join(
                [sample(config.alphabet, 1)[0] for _ in range(20)]
            )
            encrypted = encrypter.process(message)
            decrypted = decrypter.process(encrypted)

            self.assertEqual(message, decrypted)
            self.assertNotEqual(message, encrypted)
