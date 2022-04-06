from setuptools import find_namespace_packages, setup
from setuptools import find_namespace_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name="dino",
    version="0.1.0",
    description="all-in-one forensics",
    author="Dino",
    author_email="dino",
    url="https://github.com/jurelou/dino",
    # packages=find_namespace_packages(include=['openfor', 'openfor.*']),
    entry_points={
        # "console_scripts": [
        #     "openfor_cli=openfor.cli:cli"
        # ]
    },
    install_requires=[
        "dynaconf==3.1.7",
        "prefect==1.2.0"
    ],
    extras_require={
        'dev': []
    },
    python_requires=">=3.8.*, <4",
)