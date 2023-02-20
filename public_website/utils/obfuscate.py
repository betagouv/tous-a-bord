import re

def obfuscate_email(input:str):
    PATTERN_EMAIL = "^([a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*)@([a-zA-Z0-9.]+)$"
    search = re.search(PATTERN_EMAIL, input)
    if(search is None):
        return "".join(map(lambda _: "*", list(input)))
    identifier = search[1]
    domain = search[2]
    obfuscated_identifier = "".join(map(lambda _: "*", list(identifier)))
    return obfuscated_identifier + "@"+domain
