from django.test import TestCase
from random import sample
from string import ascii_uppercase

from .config import EnigmaConfig, random_config
from .emulator import EnigmaEmulator


class EnigmaEmulationTests(TestCase):
    def test_random_configs(self):
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

    def test_martha_config(self):
        config = EnigmaConfig(['ОБАГ', 'БГОА'], 'ГОБА', ['АГ'], [0, 0], 'АБОГ')
        message = 'АБОБА'
        expected = 'ГОБОБ'
        encrypted = EnigmaEmulator(config).process(message)
        self.assertEqual(encrypted, expected)

    def test_sabaton_config(self):
        config = EnigmaConfig(
            rotors=[
                'NVTDFMXHQPWIESJZLCAUKRGYBO',
                'RNKXALDZIOBHTWYJEVCQMPFGSU',
                'HXOIRGSBVLTEQPAMDKWFCZNUJY',
            ],
            reflector='VSFJHCWEYDNXQKUZMTBROAGLIP',
            plugs=[
                'BT',
                'IS',
                'PC',
                'YH',
                'ZR',
                'GD',
                'XN',
                'UW',
                'LO',
                'MJ',
                'QE',
                'AF',
                'KV',
            ],
            positions=[24, 4, 9],
            alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        )
        message = (
            'INTOTHEMOTHERLANDTHEGERMANARMYMARCH'
            'COMRADESSTANDSIDEBYSIDETOSTOPTHENAZICHARGE'
            'PANZERSONRUSSIANSOILATHUNDERINTHEEAST'
            'ONEMILLIONMENATWARTHESOVIETWRATHUNLEASHED'
        )
        expected = (
            'DUGGDXPSXILBORXAMNZCMPYFFFGDXKEINAG'
            'VMECFGKJNCDKPXZRWMNYMMTXSVWIIGQFIIXGQYMBRJ'
            'YSPLUDIQGKXZFPOYXVNRRZIAAVPEZWGBUNFXK'
            'BTWRLDMDWSKUFELOJAAJYQVSDYZKPYZUYFOQKWRMH'
        )

        encrypted = EnigmaEmulator(config).process(message)
        self.assertEqual(encrypted, expected)
