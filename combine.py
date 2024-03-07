from llama_cpp import Llama
from diffusers import AutoPipelineForText2Image
import torch
import os
import sys
import shelve
from PIL import Image

path = "."
model = "mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf"
system_prompt = """
You combine words according to their meaning. 
Avoid having the result be the same as one of the inputs. 
Try to generate general words. 
Be creative. 
Keep the words simple. 
Above all, always answer with a singular word or phrase delimited by quotes.
"""
system_prompt = system_prompt.replace("\n"," ").replace("  "," ").strip()
combinations_file = "combinations"

image_model = "stabilityai/sdxl-turbo"
image_modifier = "concept art, design, icon"
image_negative_prompt = "lowres, cropped, worst quality"
# ordered in priority
endings = ["png", "jpg"]
image_folder = "images"
image_enabled = True

model_path = os.path.join(path,model)
if not os.path.exists(model_path):
    print(f"Model file not found at {model_path}. Please download the model file first.")
    sys.exit(1)

print("Loading models...")
print("Loading llama...")
llm = Llama(model_path=model_path, chat_format="llama-2",verbose=False) 
if image_enabled:
    print("Loading SDXL...")
    image_pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float32, variant="fp16")
else:
    image_pipe = None

combinations = shelve.open(combinations_file)

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
    
def get_image(element, generate=True, debug=False):
    filename = element.replace(" ","_")
    for ending in endings:
        path = os.path.join(image_folder,f"{filename}.{ending}")
        if os.path.exists(path):
            return path
    if not generate or not image_enabled:
        return None
    prompt = f"{element}, {image_modifier}"
    path = os.path.join(image_folder,f"{filename}.{endings[0]}")
    if debug:
        print(f"Generating image for {element}")
    image = image_pipe(prompt=prompt, negative_prompt=image_negative_prompt, num_inference_steps=1, guidance_scale=0.0).images[0]
    image.save(path)
    return path

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

def combine(element1,element2, generate=True, image=True, debug=False, annotations=None):
    """Combine two elements into a new element

    Args:
        element1 (str): First word to combine
        element2 (str): Second word to combine
        generate (bool, optional): Generate a new combination if not found. Defaults to True.
        image (bool, optional): Generate an image if none is present (and generate is set). Defaults to True.
        debug (bool, optional): Print debug information. Defaults to False.
        annotations (dict, optional): Annotations for the generation (e.g. weaker model). Defaults to None.

    Returns:
        str: Combined word
        str: Path to image
        bool: True if the word was newly generated
    """
    element1, element2 = sorted([sanitize(element) for element in [element1,element2]])
    
    generate_image = generate and image
    combined, _ = lookup(element1,element2)
    if combined is not None:
        path = get_image(combined, generate=generate_image)
        return combined, path, False
    if not generate:
        return None, None, False
        
    if debug:
        print(f"Combining {element1} and {element2}")
        
    try:
        response = llm.create_chat_completion(
            messages = [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"\"{element1}\" + \"{element2}\" = ?"
                },
            ],
            max_tokens=32,
            stop=["</s>", "\n"],
        )
        
        combined = response["choices"][0]["message"]["content"]
        # extract from quotes
        if '"' in combined:
            combined = combined.split('"')[1]
        else:
            combined = combined.strip().split(" ")[0]
        combined = sanitize(combined)
        
        combinations[tuple] = combined
        combinations.sync()
    except Exception as e:
        print(f"Error combining {element1} and {element2}: {e}")
        print("Response:",response)
        return None, None, False
    
    if debug:
        print(f"Result: {combined}")
    
    path = get_image(combined, generate=generate_image, debug=debug)
    return combined, path, True



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
        # print(f"{word} + {element} = ", end="", flush=True)
        print(f"Generating {word} + {element}...")
        combined, path, new = combine(word,element, generate=True, image=True, debug=False)
        new_word = combined not in found
        # twice the start for the image generation overwrite
        print(f"{word} + {element} = {combined}{' (new)' if new else ''}")
        if new_word:
            newly_found.append(combined)

    found.update(newly_found)
    queue.extend(newly_found)

sys.exit(0)




print("Some example combinations:")
for element1, element2 in [
    ("fire", "water"),
    ("fire", "steam"),
    ("steam", "steam"),
    ("water", "water"),
    ("water", "steam"),
    ("steam", "water"),
    ("harry potter", "goblin"),
    ("lord of the rings", "goblin"),
]:
    combined = combine(element1,element2)
    print(f"{element1} + {element2} = {combined}")

# example results
# fire + water = steam
# fire + steam = vapor
# steam + steam = pressure
# water + water = ponds
# water + steam = boiled water
# steam + water = boiled
# harry potter + goblin = gringotts
# lord of the rings + goblin = goblin's master


print("Starting server...")
PORT = 5000
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

@app.route('/combine_post', methods=['POST'])
def combine_route_post():
    # e.g. curl -X POST -H "Content-Type: application/json" -d '{"element1":"fire","element2":"water"}' http://localhost:5000/combine_post
    data = request.json
    element1 = data["element1"]
    element2 = data["element2"]
    generate_image = data.get("generate_image")
    if generate_image is None:
        generate_image = True
    combined, image, new = combine(element1,element2, generate=True, image=generate_image, debug=True)
    if combined is None:
        return jsonify({"error":"combination not found"})
    return jsonify({"combined":combined, "image":image, "new":new})

# @app.route('/combine_get', methods=['GET'])
# def combine_route_get():
#     # e.g. http://localhost:5000/combine?element1=fire&element2=water
#     # warning: long generation time might time out
#     # generally use POST instead
#     element1 = request.args.get('element1')
#     element2 = request.args.get('element2')
#     generate = request.args.get('generate')
#     if generate is None:
#         generate = False
#     combined, image, new = combine(element1,element2, generate=generate)
#     if combined is None:
#         return jsonify({"error":"combination not found"})
#     return jsonify({"combined":combined})

# expose the image folder
@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory(image_folder, path)

# for testing (debug mode)
app.run(port=PORT)
    
combinations.close()