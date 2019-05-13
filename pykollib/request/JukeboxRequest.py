from aiohttp import ClientResponse



#def parseEffectsGained(text):
#    effects = []
#    effectPattern = PatternManager.getOrCompilePattern("gainEffect")
#    for match in effectPattern.finditer(text):
#        eff = {}
#        eff["name"] = match.group(1)
#        eff["turns"] = int(match.group(2).replace(",", ""))
#        effects.append(eff)
#    return effects

#def parse(html: str, **kwargs) -> Dict[str, Any]:

def jukeboxRequest(session: "Session") -> ClientResponse:
    "Uses the jukebox in the clan rumpus room."

    params["action"] = "click"
    params["spot"] = 3
    params["furni"] = 2

    return session.request("clan_rumpus.php", params=params)
