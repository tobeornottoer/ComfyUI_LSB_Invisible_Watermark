import transformers
from torchvision import transforms
import torch
from PIL import Image
import numpy as np


class LsbWatermark:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",{"label":"图像"}),
                "watermark": ("STRING", {
                    "multiline": False,
                    "default": "this is a watermark!!"
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "lsb_encode"
    CATEGORY = "水印"

    def lsb_encode(self, images, watermark):
        results = []
        for image in images:
            i = 255. * image.cpu().numpy()

            image_np_array = np.clip(i, 0, 255).astype(np.uint8)
            image_pil = Image.fromarray(image_np_array)

            width, height = image_pil.size
            binary_message = ''.join(format(ord(char), '08b') for char in watermark)
            index = 0
            for y in range(height):
                for x in range(width):
                    if index >= len(binary_message):
                        break
                    pixel = image_np_array[y, x]
                    for i in range(3):
                        if index < len(binary_message):
                            new_bit = int(binary_message[index])
                            pixel[i] = pixel[i] & ~1 | new_bit
                            index += 1
                        else:
                            break
                    image_np_array[y, x] = pixel
                if index >= len(binary_message):
                    break 

            pil_image = Image.fromarray(image_np_array)
            result_image_np = np.array(pil_image).astype(np.float32) / 255.0
            result_image_tensor = torch.from_numpy(result_image_np)[None,]
            results.append(result_image_tensor)

        return (results[0],)




NODE_CLASS_MAPPINGS = {
    "LsbWatermark": LsbWatermark,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LsbWatermark": "LSB水印嵌入",
}
