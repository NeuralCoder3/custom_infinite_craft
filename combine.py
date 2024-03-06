from llama_cpp import Llama
import os
import sys
import shelve

path = "."
model = "mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf"
system_prompt = "You combine words according to their meaning. Avoid having the result be the same as one of the inputs. Try to generate general words. Be creative. Keep the words simple. Above all, always answer with a singular word or phrase delimited by quotes."


model_path = os.path.join(path,model)
if not os.path.exists(model_path):
    print(f"Model file not found at {model_path}. Please download the model file first.")
    sys.exit(1)

llm = Llama(model_path=model_path, chat_format="llama-2",verbose=False) 

combinations = shelve.open("combinations")

def sanitize(element):
    element = element.lower()
    element = element.replace("_"," ")
    allowed = "abcdefghijklmnopqrstuvwxyz- 0123456789"
    element = "".join([c for c in element if c in allowed])
    element = element.strip()
    return element
    

def combine(element1,element2):
    element1, element2 = sorted([sanitize(element) for element in [element1,element2]])
    tuple = f"[{element1}]_[{element2}]"
    if tuple in combinations:
        return combinations[tuple]
        
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
    return combined

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
    combined = combine(element1,element2)
    return jsonify({"combined":combined})

@app.route('/combine_get', methods=['GET'])
def combine_route_get():
    # e.g. http://localhost:5000/combine?element1=fire&element2=water
    # warning: long generation time might time out
    # generally use POST instead
    element1 = request.args.get('element1')
    element2 = request.args.get('element2')
    combined = combine(element1,element2)
    return jsonify({"combined":combined})

# for testing (debug mode)
app.run(port=PORT)
    
combinations.close()







# for element1, element2 in [
#     ("fire", "water"),
#     ("fire", "steam"),
#     ("steam", "steam"),
#     ("water", "water"),
#     ("water", "steam"),
#     ("steam", "water"),
#     ("harry potter", "goblin"),
#     ("lord of the rings", "goblin"),
# ]:
#     response = llm.create_chat_completion(
#         messages = [
#             {"role": "system", "content": "You combine words according to their meaning. Avoid having the result be the same as one of the inputs. Keep the words simple. Above all, always answer with a singular word or phrase delimited by quotes."},
#             {
#                 "role": "user",
#                 "content": f"\"{element1}\" + \"{element2}\" = ?"
#             },
#         ],
#         max_tokens=32,
#         stop=["</s>", "\n"],
#     )
    
#     combined = response["choices"][0]["message"]["content"].strip()
#     # remove things in parentheses
#     # combined = combined.split("(")[0].strip()
#     # extract from quotes
#     combined = combined.split('"')[1]

#     print(f"{element1} + {element2} = {combined}")
    

# {'id': 'chatcmpl-4d06e928-db59-4df4-ada3-4aae84daac17', 'object': 'chat.completion', 'created': 1709748419, 'model': './mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf', 'choices': [{'index': 0, 'message': {'role': 'assistant', 'content': " Once upon a time, in the high Andes mountains of Peru, there was a group of wild llamas who lived freely and happily in the vast grasslands. These llamas were known for their beautiful, thick wool coats that came in a variety of colors - from creamy white to rich chocolate brown, and even speckled grey. They were also admired for their long, powerful legs and necks, which allowed them to reach the tastiest leaves and shrubs on the tallest hillsides.\n\nThe leader of the herd was a wise and gentle llama named Lucho. He was a magnificent creature, with a thick, shimmering coat of gold and a regal bearing that commanded respect from all who met him. Lucho was not only strong and brave, but he was also kind-hearted and always looked out for the well-being of his herd.\n\nOne day, while the llamas were grazing in the fields, they noticed a group of humans approaching from afar. The llamas had seen humans before, but these ones seemed different - they wore strange clothes and carried strange objects that the llamas had never seen before. Lucho knew that he had to protect his herd from any potential danger, so he called out to them in their unique, melodic language, warning them to stay away.\n\nBut the humans did not understand the llama's language, and they continued to approach. Lucho realized that he needed to find a way to communicate with these strange creatures. He decided to use his most valuable asset - his wool. Lucho carefully selected some of the finest strands from his golden coat and wove them into a beautiful, intricate pattern.\n\nWhen the humans saw the stunning creation, they were amazed. They had never seen anything like it before. The llamas' unique language had finally been understood, and the ice was broken. The humans and llamas began to communicate, and Lucho learned that these humans were not a threat at all. In fact, they had come to offer the llamas a gift - a new home where they would be protected from predators and cared for by humans who appreciated their beauty and grace.\n\nLucho was hesitant at first, but he knew that this was"}, 'finish_reason': 'length'}], 'usage': {'prompt_tokens': 32, 'completion_tokens': 480, 'total_tokens': 512}}
