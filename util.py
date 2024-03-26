import config
import shelve
import atexit
import re

combinations = shelve.open(config.combinations_file)
elements = set()
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
    if element+"s" in elements:
        element = element+"s"
    if element[-1] == "s" and element[:-1] in elements:
        element = element[:-1]
    return element

def format_name(element1,element2,op="+"):
    if op == "+":
        return f"[{element1}]_[{element2}]"
    return f"[{element1}]_[{element2}]_{op}"

def lookup(element1,element2, op="+"):
    tuple = format_name(element1,element2,op)
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
    
# [element1]_[element2]_op 
# the _op is optional
key_pattern = re.compile(r"\[([^\]]+)\]_\[([^\]]+)\](?:_(.+))?")
def destruct_key(key):
    match = key_pattern.match(key)
    if match:
        # e1,e2 = match.groups()
        e1 = match.group(1)
        e2 = match.group(2)
        op = match.group(3)
        if op is None:
            op = "+"
        return e1,e2,op
    else:
        return None
    
# remove all elements that do not follow the pattern
def clean_elements():
    for key in list(combinations.keys()):
        res = destruct_key(key)
        if res is None:
            del combinations[key]
    combinations.sync()
    
# clean_elements()
    
def all_elements():
    elements = set()
    for key in combinations:
        e1,e2,op = destruct_key(key)
        elements.add(e1)
        elements.add(e2)
        combined,_ = lookup(e1,e2,op)
        elements.add(combined)
    return elements

elements.update(all_elements())

def insert(element1,element2,combined,op="+", annotations=None):
    tup = format_name(element1,element2,op)
    combinations[tup] = (combined,annotations)
    combinations.sync()
    elements.add(combined)