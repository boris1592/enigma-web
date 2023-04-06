from django.test import TestCase
from emulator.config import random_config
from emulator.emulator import EnigmaEmulator
from random import sample


class EnigmaEmulationTests(TestCase):
    def test_emulation(self):
        for _ in range(5):
            config = random_config(3, 'abcdefgh')
            encrypter = EnigmaEmulator(config)
            decrypter = EnigmaEmulator(config)

            message = ''.join(
                [sample(config.alphabet, 1)[0] for _ in range(20)]
            )
            encrypted = encrypter.process(message)
            decrypted = decrypter.process(encrypted)

            self.assertEqual(message, decrypted)
            self.assertNotEqual(message, encrypted)
