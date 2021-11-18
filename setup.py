from setuptools import find_namespace_packages, setup

with open("README.md") as f:
    readme = f.read()

setup(
    name="openfor",
    version="0.1.0",
    description="all-in-one forensics",
    author="Opulence",
    author_email="openforr",
    url="https://github.com/jurelou/openfor",
    packages=["openfor"],
    entry_points={
        "console_scripts": [
            "openfor_cli=openfor.cli:cli"
        ]
    },
    install_requires=[
        "click==8.0.3",
        "celery==5.2.0",
        "dynaconf==3.1.7",
        "docker==5.0.3",
        "loguru==0.5.3",
        "python-magic==0.4.24"
    ],
    extras_require={
        'dev': []
    },
    python_requires=">=3.8.*, <4",
)