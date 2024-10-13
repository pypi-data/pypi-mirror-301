from re import search, sub, Match


def match(pattern: str, string: str, group: int = 0) -> str:
    match: Match = search(pattern, string)
    try:
        return match.group(group) if match else ""
    except IndexError:
        return ""


def replace(regex: str, replace_with: str, text: str) -> str:
    return sub(regex, replace_with, text)
