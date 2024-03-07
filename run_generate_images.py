import networks

networks.init(load_llm=False, load_image=True)

elements = networks.util.all_elements()
elements = sorted(elements)

for element in elements:
    print(f"Generating {element}...")
    _ = networks.get_image(element, generate=True, debug=False)
    