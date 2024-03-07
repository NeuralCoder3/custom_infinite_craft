import os

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

model_path = os.path.join(path,model)
