import networks

generate_images = False
networks.init(load_image=generate_images)

# combine every word with every earlier word
queue = ["fire", "water", "earth", "air"]
found = set()
it = 0
while True:
    it += 1
    if len(queue) == 0:
        print("Queue empty")
        break
    word = queue.pop(0)
    newly_found = []
    found.add(word)
    for element in found:
        print(f"Generating {word} + {element}...", flush=True)
        combined, path, new = networks.combine(word,element, generate=True, image=generate_images, debug=False)
        new_word = combined not in found
        # twice the start for the image generation overwrite
        print(f"{word} + {element} = {combined}{' (new)' if new else ''}")
        if new_word:
            newly_found.append(combined)

    found.update(newly_found)
    queue.extend(newly_found)