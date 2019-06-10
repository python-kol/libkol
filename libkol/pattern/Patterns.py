"""
This module holds all of the regular expression patterns that kollib uses. It makes sense
to store them all in the same place since many patterns are used by multiple requests.
The 'patterns' data object is a dictionary mapping patternId to pattern. If pattern is a tuple,
then the first element of the tuple should be the pattern while the second element is a flag
to pass to re.compile (like re.DOTALL).
"""

patterns = {
    # General patterns.
    "whitespace": r"([\t ]+)",
    "results": r"<b>Results:<\/b><\/td><\/tr><tr><td[^<>]*><center><table><tr><td>(.*?)</td></tr></table></center></td></tr>",
    "htmlComment": r"<!--.*?-->",
    "htmlTag": r"<[^>]*?>",
    # Item-related patterns.
    "menuItem": r'<input type=radio name=whichitem value="?(-?[0-9]+)"?></td><td><img .*? onclick=\'descitem\("?([^"]+)"?\);\'>',
    "isCocktailcraftingIngredient": (r"<br>\(Cocktailcrafting ingredient\)<br>"),
    "isCookingIngredient": r"<br>\(Cooking ingredient\)<br>",
    "isJewelrymakingComponent": r"<br>\(Jewelrymaking component\)<br>",
    "isMeatsmithingComponent": r"<br>\(Meatsmithing component\)<br>",
    "inventorySingleItem": r"<img [^>]*descitem\(([0-9]+)[^>]*></td><td[^>]*><b[^>]*>([^<>]+)</b>&nbsp;<span><\/span>",
    "inventoryMultipleItems": r"<img [^>]*descitem\(([0-9]+)[^>]*></td><td[^>]*><b[^>]*>([^<>]+)</b>&nbsp;<span>\(([0-9]+)\)<\/span>",
    "itemAutosell": r"<br>Selling Price: <b>(\d*) Meat\.<\/b>",
    "itemImage": r'\/images\.kingdomofloathing\.com\/itemimages\/(.*?)"',
    "itemName": r"<b>(.+?)<\/b>",
    "itemType": r"<br>Type: <b>([^<]*)<.*\/b><br>",
    # Error patterns.
    "notEnoughItems": r"(?:<td>You haven't got that many\.<\/td>)|(?:You don't have the item you're trying to use\.)|(?:You don't have the item you're trying to equip\.)",
    # Chat patterns.
    "chatChannel": r'^<font color="?#?\w+"?>\[([^<>]+)\]<\/font> ',
    "chatMessage": r'<b><a target="?mainpane"? href="showplayer\.php\?who=(-?[0-9]+)"><font color="?#?\w+"?>([^<>]+)<\/font>(?:<\/b>|<\/a>|:)* (.*)$',
    "chatEmote": r'<b><i><a target="?mainpane"? href="showplayer\.php\?who=([0-9]+)"><font color="?#?\w+"?>([^<>]+)<\/b><\/font><\/a> (.*)<\/i>$',
    "privateChat": r'<a target="?mainpane"? href="showplayer\.php\?who=([0-9]+)"><font color="?blue"?><b>([^)]+) \(private\):<\/b><\/font><\/a> <font color="?blue"?>(.*)</font>$',
    "chatNewKmailNotification": r'<a target="?mainpane"? href="messages\.php"><font color="?green"?>New message received from <a target="?mainpane"? href=\'showplayer\.php\?who=([0-9]+)\'><font color="?green"?>([^<>]+)<\/font><\/a>\.<\/font><\/a>$',
    "chatLink": r'<a target="?_blank"? href="([^"]+)"><font color="?blue"?>\[link\]<\/font><\/a> ',
    "chatWhoResponse": r"<table><tr><td class=tiny><center><b>Players in (?:this channel|channel \w+):",
    "chatWhoPerson": r'<a (?:class="([^"]+)" )?target="?mainpane"? href="showplayer\.php\?who=([0-9]+)"><font color="?#?\w+"?>([^<>]+)<\/font><\/a>',
    "chatLinkedPlayer": r"<a style='color: #?\w+' href='showplayer\.php\?who=([0-9]+)' target=mainpane>([^<]+)<\/a>",
    "newChatChannel": r"<font color=[^>]+>You are now talking in channel: ([^\,]+?)\.<p><p>(.*?)</font>",
    "chatListenResponse": r"<font color=[^>]+>Currently listening to channels:(.*?<b>.*?</b>.*?)</font>",
    "chatListenCurrent": r"<br>&nbsp;&nbsp;<b>(.*?)</b>",
    "chatListenOthers": r"&nbsp;&nbsp;([^<>]*?)<br>",
    "chatStartListen": r"<font color=[^>]+>Now listening to channel: ([^>]+)</font>",
    "chatStopListen": r"<font color=[^>]+>No longer listening to channel: ([^>]+)</font>",
    "chatMultiLineStart": r'<b><a target="?mainpane"? href="showplayer\.php\?who=(-?[0-9]+)"><font color="?#?\w+"?>([^<>]+)<\/font><\/b><\/a>:$',
    "chatMultiLineEmote": r'<b><i><a target="?mainpane"? href="showplayer\.php\?who=(-?[0-9]+)"><font color="?#?\w+"?>([^<>]+)<\/b><\/font><\/a>$',
    "outgoingPrivate": r'<font color="?blue"?><b>private to <a class=nounder target="?mainpane"? href="?showplayer.php\?who=([0-9]+)"?><font color="?blue"?>(.*?)</font></a></b>:(.*?)</font></br>',
    "chatPlayerLoggedOn": r"<font color=green><a target=mainpane href=\'showplayer\.php\?who=([0-9]+)\'><font color=green><b>([^<>]+)<\/b><\/font><\/a> logged on\.<\/font>$",
    "chatPlayerLoggedOff": r"<font color=green><a target=mainpane href=\'showplayer\.php\?who=([0-9]+)\'><font color=green><b>([^<>]+)<\/b><\/font><\/a> logged off\.<\/font>$",
    "chatTalkieFrequency": r"<font color=green>The frequency is (.*?), Mr. Rather\.<\/font>",
    "chatCarnival": r'<font color="?green"?>(?:.*?)testlove=([0-9]+)\'>consult Madame Zatara about your relationship<\/a> with ([^<>]+?)\.<\/font>',
    # Clan dungeon patterns.
    "dungeonActivity": r"(?:^|<blockquote>|<br>|<br><b>|<b>)([^<>]+) \(#([0-9,]+)\) ((?:[^<>](?!(?:\([0-9]+ turns?\))))+)(?: \(([0-9,]+) turns?\))?",
    "dungeonLootDistribution": r"(?:<blockquote>|<br>)([^<>]+) \(#([0-9,]+)\) distributed <b>([^<>]+)</b> to ([^<>]+) \(#([0-9,]+)\)<br>",
    "dungeonPreviousRun": r'<tr><td class="?small"?>([^<>]+)&nbsp;&nbsp;<\/td><td class="?small"?>([^<>]+)&nbsp;&nbsp;<\/td><td class="?small"?>([^<>]+)&nbsp;&nbsp;<\/td><td class="?small"?>([0-9,]+)<\/td><td class="?tiny"?>\[<a href="clan_raidlogs\.php\?viewlog=([0-9]+)">view logs<\/a>\]<\/td><\/tr>',
    "dungeonLogType": r"<div id=[^>]+><center><b>([^:]+):<!--[^:]+:([0-9]+)--></b><p><table[^>]+><tr><td[^>]+>(.*?)</table></div>",
    "dungeonLogStatus": r"<center>(.*?)<b>([0-9]+)<\/b> (.*?).</center>",
    "dungeonLogCategory": r"<b>([^<>]+):?<\/b><blockquote>(.*?)<\/blockquote>",
    "imprisonedByChums": r"^(.*) has been imprisoned by the C\. H\. U\. M\.s!$",
    "freedFromChums": r"^(.*) has rescued (.*) from the C\. H\. U\. M\.s\.$",
    "chefExplosion": r"Smoke begins to pour from the head of your chef-in-the-box. It begins to vibrate noisily, spits out a few dishes at random, and then explodes\.",
    # Stat, Substat, Leveling, HP, and MP patterns. Will fail in Haiku Dungeon.
    "muscleGainLoss": r"You (gain|lose) ([0-9,]+) (?:Beefiness|Fortitude|Muscleboundness|Strengthliness|Strongness)",
    "mysticalityGainLoss": r"You (gain|lose) ([0-9,]+) (?:Enchantedness|Magicalness|Mysteriousness|Wizardliness)",
    "moxieGainLoss": r"You (gain|lose) ([0-9,]+) (?:Cheek|Chutzpah|Roguishness|Sarcasm|Smarm)",
    "musclePointGainLoss": r"You (gain|lose) (a|some) Muscle points?",
    "mystPointGainLoss": r"You (gain|lose) (a|some) Mysticality points?",
    "moxiePointGainLoss": r"You (gain|lose) (a|some) Moxie points?",
    "levelGain": r"You gain (a|some) (?:L|l)evels?",
    "hpGainLoss": r"You (gain|lose) ([0-9,]+) hit points?",
    "mpGainLoss": r"You (gain|lose) ([0-9,]+) (?:Muscularity|Mana|Mojo) (?:P|p)oints?",
    # Drunkenness, Adventures, and Effect patterns.
    "gainDrunk": r"You gain ([0-9]+) Drunkenness",
    "gainAdventures": r"You gain ([0-9,]+) Adventures",
    "gainEffect": r"<td valign=center class=effect>You acquire an effect: <b>(.*?)</b><br>\(duration: ([0-9,]+) Adventures\)</td>",
    # Store patterns.
    "storeInventory": r'<tr class="deets" rel="([0-9]+)" after="([0-9]+)">(.*?)<b>(.*?)</b></td><td valign="center" align="center">([0-9]+)</td(.*?)name="price\[([0-9]+)\]" value="([0-9,]+)"(.*?)name="limit\[[0-9]+\]" value="([0-9]+)"(.*?)cheapest: ([0-9]+)</span>',
    # Adventure patterns.
    "twiddlingThumbs": r"You twiddle your thumbs\.",
    "userShouldNotBeHere": r"(?:>You shouldn't be here\.<)|(?:)>This is not currently available to you\.<",
    "monsterName": r"<span id='monname'>(.*?)<\/span>",
    "choiceIdentifier": r'<input type="?hidden"? name="?whichchoice"? value="?([0-9]+)"?>',
    "choiceName": r"<b>([^<>]+?)<\/b><\/td><\/tr>",
    "noncombatName": r"<center><table><tr><td><center><b>([^<>]+)<\/b><br><img",
    "fightWon": r"<center>You win the fight!<!--WINWINWIN--><p>",
    "fightLost": r"<p>You lose\. +You slink away, dejected and defeated\.<p>",
    "usedBarrel": r"KOMPRESSOR does not smash",
    "noAdventures": r"You're out of adventures",
    # Mall search patterns.
    "mallItemSearchResult": r'<tr class="graybelow(.*?)<\/tr>',
    "mallItemSearchDetails": r'<a[^<>]*href="mallstore\.php\?whichstore=(?P<storeId>[0-9]+)&searchitem=(?P<itemId>[0-9]+)&searchprice=(?P<price>[0-9]+)"><b>(?P<storeName>.*?)<\/b><\/a>[^<>]*<\/td><td[^<>]*>(?P<quantity>[0-9,]+)<\/td><td[^<>]*>(?:&nbsp;)*(?P<limit>[0-9,]*)[^<>]*<\/td>',
    "nextLink": r"\[<a [^>]*start=([0-9]+)[^>]*>next</a>\]",
    "mallItemHeader": r"<tr class=.blackabove. id=.item_([0-9]+)[^0-9]>",
    # Canadia patterns.
    "noAdvInstitue": r">You don't have that many Adventures\.  Take off, eh\?<",
    "invalidAdvInstitute": r">That doesn't make any sense, you hoser\.<",
    # Clan patterns.
    "clanName": r'<a href="clan_hall\.php">([^<>]*)<\/a>',
    "clanCredo": r"<textarea name=newcredo[^<>]*>([^<>]*)</textarea>",
    "clanWebsite": r'<input type=text class=text name=website value="([^"]*)" size=60 maxlength=255>',
    "clanAcceptingApps": r"<p>Your clan is currently accepting applications\.<br>",
    "clanRankContainer": r"<select name=level[0-9]+>(.*?)<\/select>",
    "clanRank": r"<option value=([0-9]+)(?: selected)?>(.*?) \(&deg;([0-9]+)\)<\/option>",
    "clanWhitelistMember": r"""<tr><td><input type=hidden name=(?:player[0-9]+|who) value=[0-9]+><a href='showplayer\.php\?who=(?P<userId>[0-9]+)' class=nounder><b>(?P<userName>[^<>]+)</b> \(#[0-9]+\)<\/a><\/td><td>(?:<select.*?<option value=(?P<clanRankId>[0-9]+) selected>.*?<\/select>|(?P<clanRankName>[^<>]+))<\/td><td>(?:<input type=text class=text size=[0-9]+ name=title[0-9]+ value=")?(?P<clanTitle>[^<>]*)(?:">)?<\/td>""",
    # Search player Patterns
    "searchPlayers": r'showplayer\.php\?who=([0-9]+)">([^<]*)<\/a>',
    # Bounty Hunter Hunter patterns.
    "easyBountyAvailable": r'<input type=hidden name=action value=takelow><input class=button type=submit value="I\'ll Get These">',
    "hardBountyAvailable": r'<input type=hidden name=action value=takehigh><input class=button type=submit value="I\'ll Get These">',
    "specialBountyAvailable": r'<input type=hidden name=action value=takespecial><input class=button type=submit value="I\'ll Get These">',
    "easyBountyActive": r'<input class=button type=submit value="I Give Up!"><input type=hidden name=action value=giveup_low>',
    "hardBountyActive": r'<input class=button type=submit value="I Give Up!"><input type=hidden name=action value=giveup_high>',
    "specialBountyActive": r'<input class=button type=submit value="I Give Up!"><input type=hidden name=action value=giveup_special>',
    "bountyChosen": r"Come back when you've gotten the goods",
    # Sept 2013 Mall interface patterns
    "dontHaveThatManyInStore": "You don't have that many in your store.",
    "itemTakenSuccessfully": "You acquire",
    "mallPriceNotUpdated": "Nothing updated",
    # Trade related patterns
    "traderIgnoringUs": r"<td>You can't make an offer to a player who has placed you on his or her ignore list\.",
    "traderIsInRoninHC": r"<td>That player cannot receive Meat or items from other players\.",
    "traderHasNotEnoughMeat": r"<td>You don't have that much Meat\.",
    "traderHasNotEnoughItems": r"<td>You don't have enough of one of the items you're trying to send.",
    "traderBannedFromChat": r"<td>You can't send offers while you're banned from the chat\.",
    "tradeSentSuccessfully": r"<td>Your trade offer has been sent\.",
    "tradeResponseSentSuccessfully": r"Pending Responses \(Outgoing\)",
}
