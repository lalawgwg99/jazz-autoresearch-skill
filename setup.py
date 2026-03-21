from setuptools import setup, find_packages

setup(
    name="jazz-autoresearch",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0",
        "pandas",
        "matplotlib",
    ],
    entry_points={
        "console_scripts": [
            "autoresearch=cli.main:main",
        ],
    },
)
