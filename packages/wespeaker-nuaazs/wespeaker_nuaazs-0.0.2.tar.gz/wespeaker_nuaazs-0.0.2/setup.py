from setuptools import setup, find_packages
import os
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requirements = [
    "tqdm",
    "kaldiio",
    "torch>=1.12.0",
    "torchaudio>=0.12.0"
]

setup(
    name="wespeaker-nuaazs",
    install_requires=requirements,
    version="0.0.2",
    author="Sheng Zhao",
    author_email="zhaosheng@nuaa.edu.cn",
    description="Speaker Embedding",
    long_description=open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "wespeaker = wespeaker_nuaazs.cli.speaker:main",
        ]
    },
)


