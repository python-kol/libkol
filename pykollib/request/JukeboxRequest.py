from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


# def parseEffectsGained(text):
#    effects = []
#    effectPattern = PatternManager.getOrCompilePattern("gainEffect")
#    for match in effectPattern.finditer(text):
#        eff = {}
#        eff["name"] = match.group(1)
#        eff["turns"] = int(match.group(2).replace(",", ""))
#        effects.append(eff)
#    return effects

# def parse(html: str, **kwargs) -> Dict[str, Any]:


def jukeboxRequest(session: "Session") -> ClientResponse:
    "Uses the jukebox in the clan rumpus room."

    params = {"action": "click", "spot": 3, "furni": 2}
    return session.request("clan_rumpus.php", params=params)
