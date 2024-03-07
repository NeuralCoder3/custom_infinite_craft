import util

print("Combinations:")
for key in util.combinations:
    elements = util.destruct_key(key)
    if elements is None:
        print(f"Invalid key: {key}")
        continue
    element1, element2 = elements
    combined,_ = util.lookup(element1,element2)
    print(f"  {element1} + {element2} = {combined}")
        
print("")
print("Elements:")
elements = util.all_elements()
for element in sorted(elements):
    print("  "+element)
print("")
print(f"{len(elements)} unique elements.")
print(f"{len(util.combinations)} combinations.")