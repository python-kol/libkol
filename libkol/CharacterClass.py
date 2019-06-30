from enum import Enum
from typing import Optional

import libkol
from .Error import UnknownError


class CharacterClass(Enum):
    SealClubber = "Seal Clubber"
    TurtleTamer = "Turtle Tamer"
    Sauceror = "Sauceror"
    Pastamancer = "Pastamancer"
    DiscoBandit = "Disco Bandit"
    AccordionThief = "Accordion Thief"
    AstralSpirit = "Astral Spirit"
    ZombieMaster = "Zombie Master"
    Vampyre = "Vampyre"

    @property
    def stat(self) -> Optional["libkol.Stat"]:
        from .Stat import Stat

        if self in [CharacterClass.SealClubber, CharacterClass.TurtleTamer]:
            return Stat.Muscle
        if self in [CharacterClass.Sauceror, CharacterClass.Pastamancer]:
            return Stat.Mysticality
        if self in [CharacterClass.DiscoBandit, CharacterClass.AccordionThief]:
            return Stat.Moxie
        if self in [CharacterClass.AstralSpirit]:
            return None

        raise UnknownError("Unrecognised character class")

    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in set(item.value for item in cls)

    @classmethod
    def from_title(cls, title: str) -> "CharacterClass":
        if cls.has_value(title):
            return cls(title)

        if title in [
            "Lemming Trampler",
            "Tern Slapper",
            "Puffin Intimidator",
            "Ermine Thumper",
            "Penguin Frightener",
            "Malamute Basher",
            "Narwhal Pummeler",
            "Otter Crusher",
            "Caribou Smacker",
            "Moose Harasser",
            "Reindeer Threatener",
            "Ox Wrestler",
            "Walrus Bludgeoner",
            "Whale Boxer",
        ]:
            return CharacterClass.SealClubber

        if title in [
            "Toad Coach",
            "Skink Trainer",
            "Frog Director",
            "Gecko Supervisor",
            "Newt Herder",
            "Frog Boss",
            "Iguana Driver",
            "Salamander Subduer",
            "Bullfrog Overseer",
            "Rattlesnake Chief",
            "Crocodile Lord",
            "Cobra Commander",
            "Alligator Subjugator",
            "Asp Master",
        ]:
            return CharacterClass.TurtleTamer

        if title in [
            "Dough Acolyte",
            "Yeast Scholar",
            "Noodle Neophyte",
            "Starch Savant",
            "Carbohydrate Cognoscenti",
            "Spaghetti Sage",
            "Macaroni Magician",
            "Vermicelli Enchanter",
            "Linguini Thaumaturge",
            "Ravioli Sorcerer",
            "Manicotti Magus",
            "Spaghetti Spellbinder",
            "Cannelloni Conjurer",
            "Angel-Hair Archmage",
        ]:
            return CharacterClass.Pastamancer

        if title in [
            "Allspice Acolyte",
            "Cilantro Seer",
            "Parsley Enchanter",
            "Sage Sage",
            "Rosemary Diviner",
            "Thyme Wizard",
            "Tarragon Thaumaturge",
            "Oreganoccultist",
            "Basillusionist",
            "Coriander Conjurer",
            "Bay Leaf Brujo",
            "Sesame Soothsayer",
            "Marinara Mage",
            "Alfredo Archmage",
        ]:
            return CharacterClass.Sauceror

        if title in [
            "Funk Footpad",
            "Rhythm Rogue",
            "Chill Crook",
            "Jiggy Grifter",
            "Beat Snatcher",
            "Sample Swindler",
            "Move Buster",
            "Jam Horker",
            "Groove Filcher",
            "Vibe Robber",
            "Boogie Brigand",
            "Flow Purloiner",
            "Jive Pillager",
            "Rhymer And Stealer",
        ]:
            return CharacterClass.DiscoBandit

        if title in [
            "Polka Criminal",
            "Mariachi Larcenist",
            "Zydeco Rogue",
            "Chord Horker",
            "Chromatic Crook",
            "Squeezebox Scoundrel",
            "Concertina Con Artist",
            "Button Box Burglar",
            "Hurdy-Gurdy Hooligan",
            "Sub-Sub-Apprentice Accordion Thief",
            "Sub-Apprentice Accordion Thief",
            "Pseudo-Apprentice Accordion Thief",
            "Hemi-Apprentice Accordion Thief",
            "Apprentice Accordion Thief",
        ]:
            return CharacterClass.AccordionThief

        raise UnknownError("Did not recognise player class from title {}".format(title))
