# Do not import this file via from -> globals will not work
import util
config = util.config

from llama_cpp import Llama
from diffusers import AutoPipelineForText2Image
import torch
import os
import sys

llm = None
image_pipe = None

def init(load_llm=True, load_image=True):
    global image_pipe
    global llm

    print("Loading models...")
    if load_llm:
        print("Loading llama...")
        if not os.path.exists(config.model_path):
            print(f"Model file not found at {config.model_path}. Please download the model file first.")
            sys.exit(1)
        llm = Llama(model_path=config.model_path, chat_format="llama-2",verbose=False) 
    if load_image:
        print("Loading SDXL...")
        image_pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float32, variant="fp16")
        # image_pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16")
        # image_pipe.enable_attention_slicing()
        # image_pipe.to("cuda")
        
def get_image(element, generate=True, debug=False):
    filename = element.replace(" ","_")
    for ending in config.endings:
        path = os.path.join(config.image_folder,f"{filename}.{ending}")
        if os.path.exists(path):
            return path
    if not generate or image_pipe is None:
        return None
    prompt = f"{element}, {config.image_modifier}"
    path = os.path.join(config.image_folder,f"{filename}.{config.endings[0]}")
    if debug:
        print(f"Generating image for {element}")
    image = image_pipe(prompt=prompt, negative_prompt=config.image_negative_prompt, num_inference_steps=1, guidance_scale=0.0).images[0]
    image.save(path)
    return path


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
    element1, element2 = sorted([util.sanitize(element) for element in [element1,element2]])
    
    generate_image = generate and image
    combined, _ = util.lookup(element1,element2)
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
                {"role": "system", "content": config.system_prompt},
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
        combined = util.sanitize(combined)
        
        util.insert(element1,element2,combined,None)
    except Exception as e:
        print(f"Error combining {element1} and {element2}: {e}")
        print("Response:",response)
        return None, None, False
    
    if debug:
        print(f"Result: {combined}")
    
    path = get_image(combined, generate=generate_image, debug=debug)
    return combined, path, True