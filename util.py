import config
import shelve
import atexit
import re

combinations = shelve.open(config.combinations_file)
atexit.register(combinations.close)

def sanitize(element):
    element = element.lower()
    allowed = "abcdefghijklmnopqrstuvwxyz- 0123456789"
    substitute = [
        ("_"," "),
        ("ä","ae"),
        ("ö","oe"),
        ("ü","ue"),
        ("ß","ss"),
        ("é","e"),
        ("è","e"),
        ("ê","e"),
        ("à","a"),
        ("â","a"),
        ("ô","o"),
        ("û","u"),
        ("î","i"),
        ("ï","i"),
        ("ç","c"),
        ("œ","oe"),
        ("æ","ae"),
    ]
    for a,b in substitute:
        element = element.replace(a,b)
    element = "".join([c for c in element if c in allowed])
    element = element.strip()
    return element

def lookup(element1,element2):
    tuple = f"[{element1}]_[{element2}]"
    if tuple not in combinations:
        return None, None
    res = combinations[tuple]
    if isinstance(res, str):
        combined = res
        annotations = None
    else:
        combined = res[0]
        annotations = res[1]
    return combined, annotations


def insert(element1,element2,combined,annotations=None):
    tup = f"[{element1}]_[{element2}]"
    combinations[tup] = (combined,annotations)
    combinations.sync()
    
key_pattern = re.compile(r"\[([^\]]+)\]_\[([^\]]+)\]")
def destruct_key(key):
    match = key_pattern.match(key)
    if match:
        e1,e2 = match.groups()
        return e1,e2
    else:
        return None
    
def all_elements():
    elements = set()
    for key in combinations:
        e1,e2 = destruct_key(key)
        elements.add(e1)
        elements.add(e2)
        combined,_ = lookup(e1,e2)
        elements.add(combined)
    return elements