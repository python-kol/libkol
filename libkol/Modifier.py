from typing import List, Union
from enum import Enum
import libkol

from .Stat import Stat


class WeightedModifier:
    def __init__(self, modifier: "Modifier", weight: int = 1):
        self.modifier = modifier
        self.weight = weight

    def __eq__(self, thing):
        return self.modifier is thing


class Modifier(Enum):
    AbsorbAdventures = "Absorb Adventures"
    AbsorbStats = "Absorb Stats"
    AccessoryDrop = "Accessory Drop"
    AdditionalSong = "Additional Song"
    Adventures = "Adventures"
    AdventureUnderwater = "Adventure Underwater"
    AttacksCanTMiss = "Attacks Can't Miss"
    Avatar = "Avatar"
    BaseRestingHp = "Base Resting HP"
    BaseRestingMp = "Base Resting MP"
    BonusRestingHp = "Bonus Resting HP"
    BonusRestingMp = "Bonus Resting MP"
    BoozeDrop = "Booze Drop"
    Breakable = "Breakable"
    Brimstone = "Brimstone"
    CandyDrop = "Candy Drop"
    Class = "Class"  # @TODO turn into expression?
    Cloathing = "Cloathing"
    Clowniness = "Clowniness"
    ColdDamage = "Cold Damage"
    ColdImmunity = "Cold Immunity"
    ColdResistance = "Cold Resistance"
    ColdSpellDamage = "Cold Spell Damage"
    ColdVulnerability = "Cold Vulnerability"
    CombatRate = "Combat Rate"
    CrimbotOutfitPower = "Crimbot Outfit Power"
    CriticalHit = "Critical Hit"
    DamageAbsorption = "Damage Absorption"
    DamageReduction = "Damage Reduction"
    DbCombatDamage = "DB Combat Damage"
    DiscoStyle = "Disco Style"
    DropsItems = "Drops Items"
    DropsMeat = "Drops Meat"
    Effect = "Effect"
    EffectDuration = "Effect Duration"
    Equalize = "Equalize"
    EquipsOn = "Equips On"  # Equips on specific familiar
    Experience = "Experience"
    Fairy = "Fairy"
    FamiliarDamage = "Familiar Damage"
    FamiliarEffect = "Familiar Effect"
    FamiliarWeight = "Familiar Weight"
    FishingSkill = "Fishing Skill"
    FloorBuffedMoxie = "Floor Buffed Moxie"
    FloorBuffedMuscle = "Floor Buffed Muscle"
    FoodDrop = "Food Drop"
    FourSongs = "Four Songs"
    FreePull = "Free Pull"  # @todo Put on Item?
    Fumble = "Fumble"
    GearDrop = "Gear Drop"
    Generic = "Generic"  # Equios on any familiar
    HatDrop = "Hat Drop"
    HoboPower = "Hobo Power"
    HotDamage = "Hot Damage"
    HotImmunity = "Hot Immunity"
    HotResistance = "Hot Resistance"
    HotSpellDamage = "Hot Spell Damage"
    HotVulnerability = "Hot Vulnerability"
    HpRegenMax = "HP Regen Max"
    HpRegenMin = "HP Regen Min"
    Initiative = "Initiative"
    InitiativePenalty = "Initiative Penalty"
    ItemDrop = "Item Drop"
    ItemDropPenalty = "Item Drop Penalty"
    Jiggle = "Jiggle"
    KruegerandDrop = "Kruegerand Drop"
    LastsUntilRollover = "Lasts Until Rollover"
    Leprechaun = "Leprechaun"
    LookLikeAPirate = "Look like a Pirate"
    Luck = "Luck"
    ManaCost = "Mana Cost"
    MaximumHooch = "Maximum Hooch"
    MaximumHp = "Maximum HP"
    MaximumMp = "Maximum MP"
    MeatBonus = "Meat Bonus"
    MeatDrop = "Meat Drop"
    MeatDropPenalty = "Meat Drop Penalty"
    MinstrelLevel = "Minstrel Level"
    MonsterLevel = "Monster Level"
    Moxie = "Moxie"
    MoxieControlsMp = "Moxie Controls MP"
    MoxieLimit = "Moxie Limit"
    MoxieMayControlMp = "Moxie May Control MP"
    MpRegenMax = "MP Regen Max"
    MpRegenMin = "MP Regen Min"
    Muscle = "Muscle"
    MuscleLimit = "Muscle Limit"
    Mysticality = "Mysticality"
    MysticalityLimit = "Mysticality Limit"
    NeverFumble = "Never Fumble"
    NonstackableWatch = "Nonstackable Watch"
    NoPull = "No Pull"
    OffhandDrop = "Offhand Drop"
    OthelloSkill = "Othello Skill"
    PantsDrop = "Pants Drop"
    PickpocketChance = "Pickpocket Chance"
    PoolSkill = "Pool Skill"
    PvPFights = "PvP Fights"
    RandomMonsterModifiers = "Random Monster Modifiers"
    RangedDamage = "Ranged Damage"
    Raveosity = "Raveosity"
    ReduceEnemyDefense = "Reduce Enemy Defense"
    RestingHp = "Resting HP"
    RestingMp = "Resting MP"
    RolloverEffect = "Rollover Effect"
    RolloverEffectDuration = "Rollover Effect Duration"
    RubeeDrop = "Rubee Drop"
    ShirtDrop = "Shirt Drop"
    SingleEquip = "Single Equip"
    SixgunDamage = "Sixgun Damage"
    Skill = "Skill"
    SleazeDamage = "Sleaze Damage"
    SleazeImmunity = "Sleaze Immunity"
    SleazeResistance = "Sleaze Resistance"
    SleazeSpellDamage = "Sleaze Spell Damage"
    SleazeVulnerability = "Sleaze Vulnerability"
    SlimeHatesIt = "Slime Hates It"
    SlimeResistance = "Slime Resistance"
    Smithsness = "Smithsness"
    SoftcoreOnly = "Softcore Only"
    Sombrero = "Sombrero"
    SombreroBonus = "Sombrero Bonus"
    SongDuration = "Song Duration"
    SpellCritical = "Spell Critical"
    SpellDamage = "Spell Damage"
    SpookyDamage = "Spooky Damage"
    SpookyImmunity = "Spooky Immunity"
    SpookyResistance = "Spooky Resistance"
    SpookySpellDamage = "Spooky Spell Damage"
    SpookyVulnerability = "Spooky Vulnerability"
    SprinkleDrop = "Sprinkle Drop"
    StatTuning = "Stat Tuning"
    StenchDamage = "Stench Damage"
    StenchImmunity = "Stench Immunity"
    StenchResistance = "Stench Resistance"
    StenchSpellDamage = "Stench Spell Damage"
    StenchVulnerability = "Stench Vulnerability"
    SupercoldResistance = "Supercold Resistance"
    Surgeonosity = "Surgeonosity"
    Synergetic = "Synergetic"
    Unarmed = "Unarmed"
    UnderwaterFamiliar = "Underwater Familiar"
    Variable = "Variable"
    Volleyball = "Volleyball"
    WarBearArmorPenetration = "WarBear Armor Penetration"
    WaterLevel = "Water Level"
    WeakensMonster = "Weakens Monster"
    WeaponDamage = "Weapon Damage"
    WeaponDrop = "Weapon Drop"
    WikiName = "Wiki Name"

    def __mul__(self, weight: int) -> "WeightedModifier":
        return WeightedModifier(self, weight)

    def __init__(self, name: str, weight: int = 1):
        self.weight = weight

    def apply_percentage(self, session: "libkol.Session", multiplier: float) -> float:
        if self is Modifier.MaximumHp:
            base = session.get_stat(Stat.Muscle, buffed=True) + 3
            multiplier += 1.5 if session.get_character_class() in Stat.Muscle else 1
        elif self is Modifier.MaximumMp:
            base = session.get_stat(Stat.Mysticality, buffed=True) + 3
            multiplier = 1.5 if session.get_character_class() in Stat.Mysticality else 1
        elif self is Modifier.Muscle:
            base = session.get_stat(Stat.Muscle)
        elif self is Modifier.Mysticality:
            base = session.get_stat(Stat.Mysticality)
        elif self is Modifier.Moxie:
            base = session.get_stat(Stat.Moxie)
        else:
            base = 1

        return multiplier * base

    def sum(self, values: List[Union[int, float]]) -> float:
        """
        Sums a set of these modifiers to apply maxima, diminishing returns, mutex etc
        """
        if self is Modifier.CombatRate:
            total = sum(values)
            if -25 <= total <= 25:
                return total

            return (-20 if total <= 0 else 20) + (total // 5)
        elif self is Modifier.ManaCost:
            return max(-3, sum(values))
        elif self is Modifier.FamiliarWeight:
            flat_total = sum([v for v in values if isinstance(v, int)])
            return flat_total + max(0, *[v for v in values if isinstance(v, float)])
        elif self in [
            Modifier.MuscleLimit,
            Modifier.MoxieLimit,
            Modifier.MysticalityLimit,
        ]:
            return min(values)
        else:
            return sum(values)

    def normalise(self, value: float) -> float:
        return value
