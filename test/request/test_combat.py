from yarl import URL

from libkol.request import combat
from .test_base import TestCase


class CombatTestCase(TestCase):
    request = "combat"

    def test_combat_parse_damage(self):
        logs = [
            (
                "Scary Death Orb drills into your skull and siphons out some of your blood, to the tune of 10 damage.",
                0,
            ),
            (
                '1234 shambles up to your opponent with a "Graaaaagh," and bites him on the head. He seems a little dazed by the experience.',
                0,
            ),
            (
                "You hand the 33398 scroll to your opponent. It unrolls it, reads it, and looks slightly confused by it. Then it tears it up and throws the bits into the wind.",
                0,
            ),
            (
                "You induct it into the clubbed club, clubbing it for 189 (<font color=red><b>+11</b></font>) damage.",
                200,
            ),
        ]

        for message, damage in logs:
            self.assertEqual(combat.parse_damage(message), damage)
