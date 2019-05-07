from aiohttp import ClientResponse


"""
Unequips the equipment in the designated slot.  HAT, WEAPON, OFFHAND,
SHIRT, PANTS, SLOT1, SLOT2, SLOT3, and FAMILIAR may be used to de-equip
certain things, or ALL will de-equip everything.
"""

HAT = "hat"
WEAPON = "weapon"
OFFHAND = "offhand"
SHIRT = "shirt"
PANTS = "pants"
SLOT1 = "acc1"
SLOT2 = "acc2"
SLOT3 = "acc3"
FAMILIAR = "familiarequip"
ALL = 999

async def unequipRequest(session: "Session" slot: str ) -> ClientResponse:

    if slot == "ALL":
        params["action"] = "unequipall"
    else:
        params["action"] = "unequip"
        params["type"] = slot

    return await session.post("inv_equip.php", params=params)
