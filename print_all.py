import shelve
import re

pattern = re.compile(r"\[([^\]]+)\]_\[([^\]]+)\]")
with shelve.open("combinations") as combinations:
    for key in combinations:
        match = pattern.match(key)
        if match:
            element1, element2 = match.groups()
            print(f"{element1} + {element2} = {combinations[key]}")
        else:
            print(f"Invalid key: {key}")