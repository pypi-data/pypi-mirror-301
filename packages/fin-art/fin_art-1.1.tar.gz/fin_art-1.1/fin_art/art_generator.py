import tqdm
# Отключаем вывод прогресс-баров tqdm
tqdm.tqdm.__init__ = lambda *args, **kwargs: None

import warnings
# Отключаем предупреждения
warnings.filterwarnings("ignore")

# Отключаем логи для библиотеки transformers
from transformers import logging
logging.set_verbosity_error()

# Отключаем логи для библиотеки diffusers
from diffusers import logging
logging.set_verbosity_error()

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from diffusers import StableDiffusionPipeline
import matplotlib.pyplot as plt

class ImageGenerator:
    LORA_PATHS = {
        "pixel": "madvasik/pixel-art-lora",
        "ink": "madvasik/ink-art-lora",
        "cyberpunk": "madvasik/cyberpunk-lora",
        "lego": "madvasik/lego-lora",
        "glasssculpture": "madvasik/glasssculpture-lora"
    }

    def __init__(self, model_name='k1tub/gpt2_prompts', 
                 tokenizer_name='distilbert/distilgpt2', 
                 stable_diff_model='stable-diffusion-v1-5/stable-diffusion-v1-5',
                 lora_type='pixel', 
                 device='cuda'):
        # Сохраняем параметры
        self.device = device

        # Проверяем, что выбранный lora_type допустим
        if lora_type not in self.LORA_PATHS:
            raise ValueError(f"Invalid LoRA type: {lora_type}. Choose from {list(self.LORA_PATHS.keys())}")

        # Инициализируем GPT-2 модель и токенизатор
        self.tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token  # Устанавливаем pad_token как eos_token
        self.model = GPT2LMHeadModel.from_pretrained(model_name).to(device)

        # Инициализируем пайплайн Stable Diffusion
        self.text2img_pipe = StableDiffusionPipeline.from_pretrained(
            stable_diff_model, torch_dtype=torch.float16, safety_checker=True
        ).to(device)

        # Загружаем выбранные веса LoRA
        self.load_lora_weights(lora_type)

    def load_lora_weights(self, lora_type):
        """Загружает LoRA веса на основе выбранного типа."""
        lora_path = self.LORA_PATHS[lora_type]
        print(f"Loading LoRA weights: {lora_path}")
        self.text2img_pipe.load_lora_weights(lora_path)

    def improve_with_gpt(self, input_prompt):
        """Улучшает входной промт с помощью GPT-2."""
        input_ids = self.tokenizer.encode(input_prompt, return_tensors="pt").to(self.device)
        attention_mask = torch.ones(input_ids.shape, device=self.device)

        out = self.model.generate(input_ids, attention_mask=attention_mask, 
                                  max_length=70, num_return_sequences=1, 
                                  pad_token_id=self.tokenizer.eos_token_id)
        improved_prompt = self.tokenizer.decode(out[0], skip_special_tokens=True)
        return improved_prompt

    def generate_images(self, input_prompt, num_images=1, num_inference_steps=100, 
                        show_prompt=False, improve_prompt=False):
        """Генерирует изображения на основе текста, с возможным улучшением промта."""
        if improve_prompt:
            print(f"Original prompt: {input_prompt}")
            input_prompt = self.improve_with_gpt(input_prompt)
            print(f"Improved prompt: {input_prompt}")

        # Преобразуем вводный текст в тензоры
        input_ids = self.tokenizer.encode(input_prompt, return_tensors="pt").to(self.device)
        attention_mask = torch.ones(input_ids.shape, device=self.device)

        # Генерация промтов на основе GPT-2
        prompts = []
        for _ in range(num_images):
            out = self.model.generate(input_ids, attention_mask=attention_mask, 
                                      max_length=70, num_return_sequences=1, 
                                      pad_token_id=self.tokenizer.eos_token_id)
            generated_text = self.tokenizer.decode(out[0], skip_special_tokens=True)
            prompts.append(generated_text)

        # Генерация изображений с помощью Stable Diffusion
        images = []
        for prompt in prompts:
            image = self.text2img_pipe(prompt, num_inference_steps=num_inference_steps).images[0]
            images.append((image, prompt))

        # Отображаем каждое изображение
        for img, prompt in images:
            if show_prompt:
                print(f"Generated prompt: {prompt}")
            plt.figure(figsize=(6, 6))
            plt.imshow(img)
            plt.axis("off")
            plt.show()
