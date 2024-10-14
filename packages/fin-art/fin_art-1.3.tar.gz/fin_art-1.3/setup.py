from setuptools import setup, find_packages

setup(
    name="fin_art",  
    version="1.3", 
    description="A module for generating pixel style images",
    author="madvasik",  
    author_email="ma2sic@yandex.ru",  
    packages=find_packages(), 
    python_requires=">=3.6",  
    install_requires=[  
        "torch",
        "transformers",
        "diffusers",
        "matplotlib",
        "peft"
    ],
)