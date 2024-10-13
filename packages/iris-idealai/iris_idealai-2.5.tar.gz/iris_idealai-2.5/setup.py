from setuptools import setup, find_packages

setup(
    name="iris_idealai",
    version="2.5",
    packages=find_packages(),
    install_requires=[
        "google-generativeai",
        "pillow", 
        "requests", 
    ],
    description="A module to interact with Iris developed by Ideal AI",
    author="Ideal AI",
    author_email="idealai@gmail.com",
    url="https://idealai.netlify.app",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
