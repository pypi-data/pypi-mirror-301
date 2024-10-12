from setuptools import setup, find_packages

# Read the content of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name="Labelme2YOLO9",
    version="0.1",
    description="Labelme2YOLO9 is a powerful tool for converting LabelMe's JSON dataset to YOLO9  format.",
    author="Ashwin, Purushothamadhas",
    author_email="p.ashwin79@gmail.com",
    url="https://github.com/Ashwin2929/labelme2yolo9",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'opencv-python',
        'Pillow',
        'numpy',
        'tqdm',
        # add other dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
