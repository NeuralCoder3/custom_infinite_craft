import networks
config = networks.config
util = networks.util

networks.init()


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
    combined = networks.combine(element1,element2)
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
    # e.g. curl -X POST -H "Content-Type: application/json" -d '{"generate_image":true,"element1":"fire","element2":"water"}' http://localhost:5000/combine_post
    data = request.json
    element1 = data["element1"]
    element2 = data["element2"]
    generate_image = data.get("generate_image")
    if generate_image is None:
        generate_image = True
    combined, image, new = networks.combine(element1,element2, generate=True, image=generate_image, debug=True)
    if combined is None:
        return jsonify({"error":"combination not found"})
    return jsonify({"combined":combined, "image":image, "new":new})

# expose the image folder
# TODO: serve separately to avoid blocking the server when generating
@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory(config.image_folder, path)

# for testing (debug mode)
app.run(port=PORT)
    