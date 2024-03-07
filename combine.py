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
    element = element.replace("_"," ")
    allowed = "abcdefghijklmnopqrstuvwxyz- 0123456789"
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

def combine(element1,element2, generate=True, image=True, debug=False):
    element1, element2 = sorted([sanitize(element) for element in [element1,element2]])
    tuple = f"[{element1}]_[{element2}]"
    generate_image = generate and image
    if tuple in combinations:
        path = get_image(combinations[tuple], generate=generate_image)
        return combinations[tuple], path
    if not generate:
        return None, None
        
    if debug:
        print(f"Combining {element1} and {element2}")
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
    combined = combined.split('"')[1]
    combined = sanitize(combined)
    
    combinations[tuple] = combined
    combinations.sync()
    
    if debug:
        print(f"Result: {combined}")
    
    path = get_image(combined, generate=generate_image, debug=debug)
    return combined, path








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
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/combine_post', methods=['POST'])
def combine_route_post():
    # e.g. curl -X POST -H "Content-Type: application/json" -d '{"element1":"fire","element2":"water"}' http://localhost:5000/combine_post
    data = request.json
    element1 = data["element1"]
    element2 = data["element2"]
    combined = combine(element1,element2, generate=True, image=True, debug=True)
    return jsonify({"combined":combined})

@app.route('/combine_get', methods=['GET'])
def combine_route_get():
    # e.g. http://localhost:5000/combine?element1=fire&element2=water
    # warning: long generation time might time out
    # generally use POST instead
    element1 = request.args.get('element1')
    element2 = request.args.get('element2')
    generate = request.args.get('generate')
    if generate is None:
        generate = False
    combined = combine(element1,element2, generate=generate)
    if combined is None:
        return jsonify({"error":"combination not found"})
    return jsonify({"combined":combined})

# for testing (debug mode)
app.run(port=PORT)
    
combinations.close()