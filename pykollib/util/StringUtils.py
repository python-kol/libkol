import html.entities
import re


def htmlEntityEncode(text):
    for k, v in list(html.entities.codepoint2name.items()):
        text = text.replace(chr(k).encode("utf-8"), "&%s;" % v)
    return text


def htmlEntityDecode(text):
    for k, v in list(html.entities.name2codepoint.items()):
        text = text.replace("&%s;" % k, chr(v).encode("utf-8"))
    return text


def htmlRemoveTags(text):
    return re.sub(r"<[^>]*?>", "", text)
